from django.shortcuts import render

from .serializers import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

from .models import *


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        hashed_password = make_password(request.data['password'])
        user, created = User.objects.get_or_create(
            username=request.data['username'],
            defaults={
                "password": hashed_password,
            }
        )
        if created:
            user.save()
            return Response({'message': 'User registered Successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'User already exists'}, status=status.HTTP_302_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key, 'message': 'Logged In'}, status=status.HTTP_200_OK)

    return Response({'message': 'Invalid Data'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    token = Token.objects.get(user=request.user)
    token.delete()
    logout(request)

    return Response({'message': 'Logged Out'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    user = request.user

    title = request.data.get("title")
    content = request.data.get("content")
    new_post = BlogPost.objects.create(
        title=title,
        content=content,
        author=user,
    )

    return Response({'message': 'New Post Created.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_posts(request):
    blog_posts = BlogPost.objects.all()

    serializer = BlogPostSerializer(blog_posts, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_post(request, ID):
    blog_post = BlogPost.objects.filter(id=ID)
    if blog_post:
        serializer = BlogPostSerializer(blog_post[0])

        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_post(request, ID):
    blog_post = BlogPost.objects.filter(id=ID, author=request.user)

    if blog_post:
        if request.data.get('title'):
            blog_post[0].title = request.data.get('title')
        if request.data.get('content'):
            blog_post[0].content = request.data.get('content')
        blog_post[0].save()

        return Response({"message": "Post updated."}, status=status.HTTP_200_OK)

    else:
        return Response({"message": "Post not found OR The post you are seeking is not yours."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_post(request, ID):
    blog_post = BlogPost.objects.filter(id=ID, author=request.user)

    if blog_post:
        blog_post[0].delete()

        return Response({"message": "Post deleted."}, status=status.HTTP_200_OK)

    else:
        return Response({"message": "Post not found OR The post you are seeking is not yours."}, status=status.HTTP_404_NOT_FOUND)
