from django.contrib import admin

from blog.models import Post, Comment
from .models import Profile

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)