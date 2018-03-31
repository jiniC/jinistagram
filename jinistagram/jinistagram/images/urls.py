from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        regex=r'^all/$', # 정규식
        view=views.ListAllImages.as_view(),
        name='list'
    ),
    url(
        regex=r'^comments/$', # 정규식
        view=views.ListAllComments.as_view(),
        name='list'
    ),
    url(
        regex=r'^likes/$', # 정규식
        view=views.ListAllLikes.as_view(),
        name='list'
    ),
]
