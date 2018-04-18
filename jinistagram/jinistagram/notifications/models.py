from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from jinistagram.users import models as user_models
from jinistagram.images import models as image_models

@python_2_unicode_compatible
class Notification(image_models.TimeStampedModel):
    TYPE_CHOICES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow')
    )
    creator = models.ForeignKey(user_models.User, related_name='creator')
    to = models.ForeignKey(user_models.User, related_name='to')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    image = models.ForeignKey(image_models.Image, null=True, blank=True)