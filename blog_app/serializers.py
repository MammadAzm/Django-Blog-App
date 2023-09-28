from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'content', 'author', 'pub_date')
