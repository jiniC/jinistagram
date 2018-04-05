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
    def get(self, request, image_id, format=None):
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
            preexisting_like.delete()
            # return Response(status=204) # no content
            return Response(status=status.HTTP_204_NO_CONTENT)
        #unlike
        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )
            new_like.save()
            return Response(status=status.HTTP_201_CREATED)