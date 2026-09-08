from django.contrib import admin
from .models import Category, Tag, Post, PostLike, PostLikeViewCount, Comment
from rangefilter.filters import NumericRangeFilterBuilder


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug','description']
    list_display_links = ['id','name']



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug']
    list_display_links = ['id','name']
    search_fields = ['id','name','slug']



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','excerpt','category','get_tags','author','is_featured','status','published_at','reading_time']
    list_display_links = ['id','title']
    list_filter = ['status','is_featured']
    search_fields = ['id','title','excerpt','category__name','tag__name','author__username','is_featured','status','published_at','reading_time']

    def get_tags(self, obj):
        return ', '.join([x.name for x in obj.tag.all()])

    get_tags.short_description = 'Tag'



@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['id','post','visitor_id','ip_address']
    list_display_links = ['id','post']
    search_fields = ['id','post__title__icontains','post__slug__icontains','post__excerpt__icontains','visitor_id','ip_address']



@admin.register(PostLikeViewCount)
class PostLikeViewCountAdmin(admin.ModelAdmin):
    list_display = ['id','post','post__status','likes_count','views_count']
    list_display_links = ['id','post']
    list_filter = [
        ('likes_count', NumericRangeFilterBuilder(title='Range: Likes Count')),
        ('views_count', NumericRangeFilterBuilder(title='Range: Views Count')),
        'post__status'
    ]
    search_fields = ['id','post__title','post__slug','likes_count','views_count']



admin.site.register(Comment)