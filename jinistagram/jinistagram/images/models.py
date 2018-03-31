from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from jinistagram.users import models as user_models # User 불러오기

# Create your models here.
@python_2_unicode_compatible
class TimeStampedModel(models.Model):
    # 최초 생성
    created_at = models.DateTimeField(auto_now_add=True)
    # 새로고침
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

@python_2_unicode_compatible
class Image(TimeStampedModel):
    """ Image Model """
    id = 1
    file = models.ImageField()
    location = models.CharField(max_length=140)
    caption = models.TextField()
    creator = models.ForeignKey(user_models.User, null=True)
    # image_set = (LOOK IN ALL THE COMMENTS FOR THE ONES THAT HAVE 'IMAGE' = 1)
    def __str__(self):
        return '{} - {}'.format(self.location, self.caption)

@python_2_unicode_compatible
class Comment(TimeStampedModel):
    """ Comment Model """
    message = models.TextField()
    creator = models.ForeignKey(user_models.User, null=True)
    image = models.ForeignKey(Image, null=True, related_name='comments')
    def __str__(self):
        return self.message

@python_2_unicode_compatible
class Like(TimeStampedModel):
    """ Like Model """
    creator = models.ForeignKey(user_models.User, null=True)
    image = models.ForeignKey(Image, null=True, related_name='likes')
    def __str__(self):
        return 'User:{} - Image Caption{}'.format(self.creator.username, self.image.caption)