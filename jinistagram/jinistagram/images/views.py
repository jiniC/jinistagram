from rest_framework.views import APIView
from rest_framework.response import Response
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
    # 데이터베이스에서 뭐가 변하면 post요청 (현재는 임시로 get)
    def get(self, request, image_id, format=None):
        print(image_id)
        return Response(status=200)