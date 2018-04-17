from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status # django status code
from . import models, serializers

class Feed(APIView):
    def get(self, request, format=None):
        user = request.user
        # 유저가 팔로잉하는 유저들
        following_users = user.following.all()
        image_list = []
        for following_user in following_users:
            # 유저가 팔로잉하는 유저들의 이미지
            user_images = following_user.images.all()[:2] # 2개의 이미지만
            # user_images = following_users.images.all()
            for image in user_images:
                image_list.append(image)
        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)
        # print(sorted_list)
        serializer = serializers.ImageSerializer(sorted_list, many=True)
        return Response(serializer.data)

class LikeImage(APIView):
    # 데이터베이스에서 뭐가 변하면(http request보낼 수 있는건) post, put요청 (현재는 임시로 get)
    def post(self, request, image_id, format=None):
        user = request.user
        # 이미지 찾기
        try:
            found_image=models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
           #  return Response(status=404)
           return Response(status=status.HTTP_404_NOT_FOUND)
            # return 하면 function은 종료
        # like
        try:
            preexisting_like=models.Like.objects.get(
                creator=user,
                image=found_image
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        #unlike
        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )
            new_like.save()
            return Response(status=status.HTTP_201_CREATED)

class UnLikeImage(APIView):
    def delete(self, request, image_id, format=None):
        user = request.user
        try:
            preexisiting_like = models.Like.objects.get(
                creator=user,
                image__id=image_id
            )
            preexisiting_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Like.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

class CommentOnImage(APIView):
    def post(self, request, image_id, format=None):
        user = request.user
        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=user, image=found_image)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Comment(APIView):
    def delete(self, request, comment_id, format=None):
        user=request.user
        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)