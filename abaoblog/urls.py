__author__ = 'haoyi'

from django.conf.urls import url
from . import views
from .api import api_view
from .test import test

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^register/$', views.user_register, name='user_register'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),

    # Api link
    url(r'^api_help$', views.api_help, name='help'),
    # login
    url(r'^token$', api_view.token, name='token'),
    # get all post listing
    url(r'^post_list$', api_view.JSONResponse.api_post_list, name='api_post_list'),
    # post the list
    url(r'^post_post$', api_view.JSONResponse.api_post, name='api_post'),

    # # tesing
    # url(r'^comment', test.JSONResponse.comment, name='comment'),
    # url(r'^show', test.show, name='show'),

    url(r'^email$', api_view.send_email, name='send'),
]
