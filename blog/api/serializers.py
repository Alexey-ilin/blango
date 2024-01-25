from rest_framework import serializers, viewsets
import blango_auth
from blog.models import Tag, Post
from blango_auth.models import User

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = "__all_"
    

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['']
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email']


