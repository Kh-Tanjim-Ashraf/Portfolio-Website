from django.contrib import admin
from .models import Category, Tag, Post, PostLike, PostLikeViewCount, Comment


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(PostLikeViewCount)
admin.site.register(Comment)