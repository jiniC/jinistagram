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
    def get_user(self, username):
        try:
            found_user = models.User.objects.get(username=username)
            return found_user
        except models.User.DoesNotExist:
            return None
    def get(self, request, username, format=None):
        found_user = self.get_user(username)
        if found_user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.UserProfileSerializer(found_user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    def put(self, request, username, format=None):
        user = request.user # 페이지 요청하는 유저
        found_user = self.get_user(username) # 우리가 찾는 유저
        if found_user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif found_user.username != user.username:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = serializers.UserProfileSerializer(
                found_user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class ChangePassword(APIView):
    def put(self, request, username, format=None):
        user = request.user
        if user.username == username:
            current_password = request.data.get('current_password', None)
            if current_password is not None:
                passwords_match = user.check_password(current_password)
                if passwords_match:
                    new_password = request.data.get('new_password', None)
                    if new_password is not None:
                        user.set_password(new_password)
                        user.save()
                        return Response(status=status.HTTP_200_OK)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


                            
        