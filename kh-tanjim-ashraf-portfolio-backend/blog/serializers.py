from rest_framework import serializers
from .models import Post, Category, Tag
from django.contrib.auth import get_user_model


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



class PostsSerializer(serializers.ModelSerializer):
    # Use it when the client application only needs the reference ID to stitch data together on the frontend, avoiding the performance overhead of joining and serialization of nested object details.

    class Meta:
        model = Post
        fields = ['title','slug','excerpt','content_html','cover_image','category','tag','author','status','published_at','reading_time','is_featured']

    # Only executes on GET request
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Mutate the data representation to make the Read-operations light-weight for the client application by giving back only the name of the records along with their identifiers.
        # Therefore, I defined `CategoryMinimalSerializer` with the minimal version of the `Category` model
        representation['category'] = CategoryMinimalSerializer(instance=instance.category).data
        representation['tag'] = TagMinimalSerializer(instance=instance.tag.all(), many=True).data
        representation['author'] = UserMinimalSerializer(instance=instance.author).data

        return representation