from django.db import models
from shared.models import TimestampMixins
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import uuid
import markdown


User = get_user_model()



class Category(TimestampMixins):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True) # blank=True allows empty form submission
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Tag(TimestampMixins):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True) # blank=True allows empty form submission

    def __str__(self):
            return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Post(TimestampMixins):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
    
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    excerpt = models.CharField(max_length=200)
    '''
    Instead of forcing your server to convert Markdown to HTML every single time a visitor loads a page (which slows down your website), this function converts it exactly once when creating or editing the text. When visitors read your content, your server serves the pre-built content_html field instantly.
    '''
    content_markdown = models.TextField()
    content_html = models.TextField(blank=True, editable=False) # blank=True, editable=False hides it from standard admin forms
    cover_image = models.ImageField(upload_to='blog/post/coverImage')
    # Note: Usually `related_name` is used for reverse lookups. In this scenario, we can access all the records of associated posts from a specific category record through this attribute.
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, related_name='posts')
    tag = models.ManyToManyField(to=Tag, related_name="posts")
    author = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='posts')
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    reading_time = models.PositiveIntegerField(help_text="In minutes — computed from word count, ~200 words/minute", blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.content_markdown:
            self.content_html = markdown.markdown(
                self.content_markdown,
                extensions = ['fenced_code', 'codehilite', 'tables']
            )
        else:
            self.content_html = ""  # If user deleted/emptied the post content, this step makes sure the HTML field is also completely emptied out in the database.

        super().save(*args, **kwargs)



class PostLike(TimestampMixins):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='postLikes')
    visitor_id = models.UUIDField(default=uuid.uuid4)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f'{self.ip_address}; {self.post.title}'



class PostLikeViewCount(TimestampMixins):
    post = models.OneToOneField(to=Post, on_delete=models.CASCADE, related_name='likesNviews')
    likes_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.post.title} -> Like: {self.likes_count}; Views: {self.views_count}'



class Comment(TimestampMixins):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=150)
    email = models.EmailField() # Default max_length=254
    website = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.post}; {self.email}; {self.content[15]}...'