from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)
from . import models # images/models.py
from jinistagram.users import models as user_models

class SmallImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = (
            'file',
        )

class CountImageSerializer(TaggitSerializer, serializers.ModelSerializer):
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

class ImageSerializer(TaggitSerializer, serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()
    tags = TagListSerializerField()
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
            'creator',
            'tags',
            'created_at'
        )

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = (
            'creator',
        )


class InputImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = (
            'file',
            'location',
            'caption',
        )