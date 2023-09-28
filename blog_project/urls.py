"""
URL configuration for blog_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from blog_app.views import *

urlpatterns = [
    path("admin/", admin.site.urls),

    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('create-post/', create_post, name='create_post'),
    path('get-all-posts/', get_all_posts, name='get_all_posts'),
    path('get-post/<int:ID>', get_post, name='get_post'),
    path('update-post/<int:ID>', update_post, name='update_post'),
    path('delete-post/<int:ID>', delete_post, name='delete_post'),

]
