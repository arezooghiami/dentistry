from django.contrib import admin
from .models import Tag,Comments,Post
from django.db import models


# class TagsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'tag',)

admin.site.register(Tag)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_id','user_id','text','parent_id')

# admin.site.register(Comments, CommentAdmin)

admin.site.register(Post)