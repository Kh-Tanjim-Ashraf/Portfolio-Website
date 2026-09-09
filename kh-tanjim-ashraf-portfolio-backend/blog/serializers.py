from rest_framework import serializers
from .models import Post, Category, Tag, PostLike, Comment
from django.contrib.auth import get_user_model
import markdown


User = get_user_model()



class CategoryMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','name','slug']



class TagMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id','name']



class UserMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username']



class PostMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id','title','slug']



class PostsSerializer(serializers.ModelSerializer):
    # Note: Use it when the client application only needs the reference ID to stitch data together on the frontend, avoiding the performance overhead of joining and serialization of nested object details.

    # Note: Defining explicitly will make the fields writable, meaning they will accept POST, PUT, and PATCH requests on these fields.
    category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all()
    )
    tag = serializers.PrimaryKeyRelatedField(
        queryset = Tag.objects.all(),
        many = True
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all()
    )

    class Meta:
        model = Post
        fields = ['id','title','slug','excerpt','content_markdown','content_html','cover_image','category','tag','author','status','published_at','reading_time','is_featured']
        read_only_fields = ['id','slug','content_html']

    # Only executes on GET request
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Mutate the data representation to make the Read-operations light-weight for the client application by giving back only the name of the records along with their identifiers.
        # Therefore, I defined `CategoryMinimalSerializer` with the minimal version of the `Category` model
        representation['category'] = CategoryMinimalSerializer(instance=instance.category).data
        representation['tag'] = TagMinimalSerializer(instance=instance.tag.all(), many=True).data
        representation['author'] = UserMinimalSerializer(instance=instance.author).data

        return representation

    # Mutate & Type Casting (Before DRF performs any form-field validations): Since it's suppose to be a form-data, the tag will be received as ['1,2,3']. Intercept the request data to convert the list of single string element into a list of native python integers (IDs) before django performs field-level validation, this method comes into picture
    def to_internal_value(self, data):
        # Check if the request came from a form-data by confirming the existence of attribute of `QueryDict()` object
        if hasattr(data, '_mutable'):
            data = data.copy()

            # Check if the `tag` key-value pair exists
            if 'tag' in data:
                tag_data = data['tag']

                # Check if tag comes in as '1,2,3' format
                if isinstance(tag_data, str):
                    # Convert & set to list of native Python integer instead of string; Using `setlist()` is a standard way to assign a list to a `QueryDict()` object
                    data.setlist('tag', [int(x.strip()) for x in tag_data.split(',') if x.strip()])

        return super().to_internal_value(data)



class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLike
        fields = ['id','post','visitor_id','ip_address']
        read_only_fields = ['id','post','visitor_id']

    # Required for GET request; Display only the ID with necessary field values avoiding multiple nested serialized data
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Mutate the existing field
        representation['post'] = PostMinimalSerializer(instance=instance.post).data

        return representation



class PostRepliesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id','post','name','website','content','is_approved']



class PostCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id','post','name','website','content','is_approved']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Replies will displayed as nested under parents
        representation['replies'] = PostRepliesSerializer(instance=instance.replies.all(), many=True).data

        return representation