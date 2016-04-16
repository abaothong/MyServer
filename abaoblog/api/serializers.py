__author__ = 'haoyi'

from django.forms import widgets
from rest_framework import serializers
from abaoblog.models import Post

class PostSerializers(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title','text')