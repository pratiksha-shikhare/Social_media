from django.contrib import admin
from .models import Profile, Post, LikePost

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
    
    