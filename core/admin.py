from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'id_user', 'profileimg', 'bio', 'location']
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'image', 'caption', 'no_of_likes', 'created_at']
    
@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_id', 'username']
    
@admin.register(FollowersCount)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ["id", "follower", "user"]