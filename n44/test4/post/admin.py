from django.contrib import admin
from .models import *


@ admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_time', 'reading_time', 'author', 'status', 'category']
    list_editable = ['status', 'category']
    list_filter = ['status', 'author', 'category', 'updated_time']
    search_fields = ['title', 'author__username']
    prepopulated_fields = {'slug': ['title']}


@ admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_time', 'writer', 'post']
    search_fields = ['title', 'writer__username']
    list_filter = ['post', 'creation_time']


@ admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_date', 'post']


@ admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'job']
