from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status # django status code
from . import models, serializers
from jinistagram.notifications import views as notification_views

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
            # 이전에 좋아요한 오브젝트 발견하면 수정하지않음
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        # unlike
        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )
            # 이전에 좋아요 하지않음 오브젝트 발견하면 수정
            new_like.save()
            # create notification for like
            notification_views.create_notification(user, found_image.creator, 'like', found_image)
            return Response(status=status.HTTP_201_CREATED)

class UnLikeImage(APIView):
    def delete(self, request, image_id, format=None):
        user = request.user
        # like 찾기
        try:
            preexisiting_like = models.Like.objects.get(
                creator=user,
                image__id=image_id
            )
            # 이전에 좋아요 있는 오브젝트 발견하면 수정
            preexisiting_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # unlike 찾기
        except models.Like.DoesNotExist:
            # 이전에 좋아요 없는 오브젝트 발견하면 수정하지않음
            return Response(status=status.HTTP_304_NOT_MODIFIED)

class CommentOnImage(APIView):
    def post(self, request, image_id, format=None):
        user = request.user
       
        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CommentSerializer(data=request.data)
         # comment notification
        notification_views.create_notification(user, found_image.creator, 'comment', found_image, serializer.data['message'])
        # serializer.data['message'] = request.data['message']
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

class Search(APIView):
    def get(self, request, format=None):
        # print(request.query_params)
        # hashtags = request.query_params.get('hashtags', None)
        # print(hashtags) # terminal 창에 찍힘 (http://localhost:8000/images/search/?hashtags=busy)
        # 해시태그가 배열로 들어감
        hashtags = request.query_params.get('hashtags', None)
        if hashtags is not None:
            hashtags = hashtags.split(",")
            # print(hashtags
            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()
            # deep relationship 검색하는 방법
            # tags__name, tags__name__in, tags__name__contains(대소문자구분), tags__name__exact(대소문자구분),tags__name__iexact(대소문자구분 no)
            serializer = serializers.CountImageSerializer(images, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ModerateComments(APIView):
    # images/3/comments/6
    def delete(self, request, image_id, comment_id, format=None):
        user = request.user # 댓글 관리할 유저
        try:
            comment_to_delete = models.Comment.objects.get(id=comment_id, image__id=image_id, image__creator=user)
            comment_to_delete.delete()
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)