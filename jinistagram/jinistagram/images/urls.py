from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        regex=r'^all/$', # 정규식
        view=views.ListAllImages.as_view(),
        name='list'
    ),
]
