from django.db import models
from jinistagram.users import models as user_models # User 불러오기

# Create your models here.
class TimeStampedModel(models.Model):
    # 최초 생성
    created_at = models.DateTimeField(auto_now_add=True)
    # 새로고침
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Image(TimeStampedModel):
    """ Image Model """
    file = models.ImageField()
    location = models.CharField(max_length=140)
    cpation = models.TextField()
    creator = models.ForeignKey(user_models.User, null=True)

class Comment(TimeStampedModel):
    """ Comment Model """
    message = models.TextField()
    creator = models.ForeignKey(user_models.User, null=True)
    image = models.ForeignKey(Image, null=True)

class Like(TimeStampedModel):
    """ Like Model """
    creator = models.ForeignKey(user_models.User, null=True)
    image = models.ForeignKey(Image, null=True)