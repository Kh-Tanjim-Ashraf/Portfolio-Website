from django.contrib import admin
from .models import Category, Tag, Post, PostLike, PostLikeViewCount, Comment


admin.site.register(Category)
admin.site.register(Tag)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','excerpt','category','get_tags','author','is_featured','status','published_at','reading_time']
    list_display_links = ['id','title']

    def get_tags(self, obj):
        return ', '.join([x.name for x in obj.tag.all()])

    get_tags.short_description = 'Tag'

admin.site.register(PostLike)
admin.site.register(PostLikeViewCount)
admin.site.register(Comment)