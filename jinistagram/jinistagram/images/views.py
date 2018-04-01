from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers

class ListAllImages(APIView):
    def get(self, request, format=None):
        all_images = models.Image.objects.all()
        serializer = serializers.ImageSerializer(all_images, many=True)
        return Response(data=serializer.data) # serializer 는 변하는 것

class ListAllComments(APIView):
    def get(self, request, format=None):
        # print(request.user.id) 페이지 로딩하는 user id
        # 페이지 로딩하는 user가 쓴 댓글만 (내가 쓴 댓글 보기)
        user_id = request.user.id
        all_comments = models.Comment.objects.filter(creator=user_id)
        # 모든 댓글 보기
        # all_comments = models.Comment.objects.all()
        serializer = serializers.CommentSerializer(all_comments, many=True)
        return Response(data=serializer.data)

class ListAllLikes(APIView):
    def get(self, request, format=None):
        all_likes = models.Like.objects.all()
        serializer = serializers.LikeSerializer(all_likes, many=True)
        return Response(data=serializer.data)