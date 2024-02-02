from rest_framework import serializers, viewsets
from blog.models import Tag, Post, Comment
from blango_auth.models import User

#Custom Fields
class TagField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
          return self.get_queryset().get_or_create(value=data.lower())[0]
        except (TypeError, ValueError):
          self.fail(f"Tag value {data} is invalid")


#Serializers
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'user_permissions']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
    creator = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), 
                                                 lookup_field='email', view_name='api_user_detail')

class PostSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(lookup_field='email', 
                                                 view_name='api_user_detail', default=serializers.CurrentUserDefault(), read_only=True)
                                                #queryset=User.objects.all(), 
    tags  =  TagField(slug_field='value', many=True, queryset=Tag.objects.all())
    class Meta:
        model = Post
        fields = '__all__'
        readonly = ["modified_at", "created_at"]
    


class PostDetailSerializer(PostSerializer):
    comments = CommentSerializer(many=True)

    def update(self, instance, validated_data):
        comments =  validated_data.pop("comments")
        instance = super(PostDetailSerializer, self).update(instance, validated_data)
        for comment_data in comments:
            if comment_data.get('id'):
                # comment already exists
                continue
            comment = Comment(**comment_data)
            comment.creator = self.context['request'].user
            comment.content_object = instance
            comment.save()
        return instance
    





