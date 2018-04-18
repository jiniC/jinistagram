from rest_framework import serializers
from . import models # images/models.py
from jinistagram.users import models as user_models

class SmallImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = (
            'file',
        )

class CountImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'comment_count',
            'like_count'
        )

class FeedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = (
            'username',
            'profile_image'
        )

class CommentSerializer(serializers.ModelSerializer):
    creator = FeedUserSerializer(read_only=True)
    # image = ImageSerializer() # image = models.ForeignKey(Image, null=True)
    class Meta:
        model = models.Comment
        fields = (
            'id',
            'message',
            'creator'
        )

class LikeSerializer(serializers.ModelSerializer):
    # image = ImageSerializer() # nested serializer
    class Meta:
        model = models.Like
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()
    # class MEta: extra info
    class Meta:
        model = models.Image
        # fields = '__all__'
        fields =  (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            'like_count',
            'creator'
        )