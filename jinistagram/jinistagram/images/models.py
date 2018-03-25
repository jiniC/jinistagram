from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):
    # 최초 생성
    created_at = models.DateTimeField(auto_now_add=True)
    # 새로고침
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Image(TimeStampedModel):
    file = models.ImageField()
    location = models.CharField(max_length=140)
    cpation = models.TextField()

class Comment(TimeStampedModel):
    message = models.TextField()