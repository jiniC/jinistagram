from rest_framework import serializers
from . import models
from jinistagram.users import models as user_models

class ExploreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'profile_image',
            'username',
            'name'
        )