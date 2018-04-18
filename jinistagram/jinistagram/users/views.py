from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from jinistagram.notifications import views as notification_views

class ExploreUsers(APIView):
    def get(self, request, format=None):
        # 인스타그램에서는 머신러닝으로 친구추천뜨지만 현재는 최근가입자5명만 보여짐
        last_five = models.User.objects.all().order_by('-date_joined')[:5]
        serializer = serializers.ListUserSerializer(last_five, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class FollowUser(APIView):
    def post(self, request, user_id, format=None):
        # pass
        user = request.user # 나를 follow 하는사람
        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.following.add(user_to_follow) # many to many 에서 추가
        user.save()
        # follow notification
        notification_views.create_notification(user, user_to_follow, 'follow')
        return Response(status=status.HTTP_200_OK)

class UnFollowUser(APIView):
    def post(self, request, user_id, format=None):
        user = request.user
        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.following.remove(user_to_follow) # many to many 에서 삭제
        user.save()
        return Response(status=status.HTTP_200_OK)

class UserProfile(APIView):
    def get(self, request, username, format=None):
        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.UserProfileSerializer(found_user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class UserFollowers(APIView):
    def get(self, request, username, format=None):
        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_followers = found_user.followers.all()
        serializer = serializers.ListUserSerializer(user_followers, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

# class based view
class UserFollowing(APIView):
    def get(self, request, username, format=None):
        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_following = found_user.following.all()
        serializer = serializers.ListUserSerializer(user_following, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class Search(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('username', None)
        if username is not None:
            users = models.User.objects.filter(username__istartswith=username) # username__icontains
            serializer = serializers.ListUserSerializer(users, many=True, context={"request": request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)