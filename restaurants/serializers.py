from collections import OrderedDict

from rest_framework import serializers
from .models import Restaurant, Comment, Blog, Gallery


# Restaurant Serializer
class RestaurantSerializer(serializers.ModelSerializer):
    # owner = serializers.CharField(source='owner.id', read_only=True)

    # Define the meta attributes for the serializer to reference
    class Meta:
        model = Restaurant
        fields = '__all__'
        depth = 2

    # Reformat the outputted json
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        owner = representation['owner']
        representation['owner'] = OrderedDict([
            ('id', owner.get('id')),
            ('username', owner.get('username')),
            ('email', owner.get('email'))
        ])

        likes = representation['likes']
        likes_updated = []
        for like in likes:
            likes_updated.append(
                OrderedDict([
                    ('id', like.get('id')),
                    ('username', like.get('username')),
                    ('email', like.get('email'))
                ])
            )
        representation['likes'] = likes_updated

        for comment in representation['comments']:
            author = comment['author']
            author = OrderedDict([
                ('id', author.get('id')),
                ('username', author.get('username')),
                ('email', author.get('email'))
            ])
            comment['author'] = author


        blogs = representation['blogs']
        # blogs_updated = []
        for blog in blogs:
            likes = blog['likes']
            user_updated = []
            for user in likes:
                user_updated.append(
                    OrderedDict([
                        ('id', user.get('id')),
                        ('username', user.get('username')),
                        ('email', user.get('email'))
                    ])
                )
            blog['likes'] = user_updated
            
            # blogs_updated.append(likes)
        # representation['blogs'] = blogs_updated
        
            


        # updated_blogs = []
        # for blog in blogs_likes:
        #     likes_updated = []
        #     for like in blog:
        #         print(blog[like])
        #         # likes_updated.append(OrderedDict([
        #         #     ('id', blog[like].get('id')),
        #         #     ('username', blog[like].get('username')),
        #         #     ('email', blog[like].get('email'))
        #         # ]))

        #     updated_blogs.append(likes_updated)

        # representation['blogs'] = updated_blogs

        return representation

    # Create a restaurant
    def create(self, validated_data):
        return super().create(validated_data | {"owner": self.context['request'].user})


# Gallery Serializer
class GallerySerializer(serializers.ModelSerializer):

    # Define the meta attributes for the serializer to reference
    class Meta:
        model = Gallery
        fields = '__all__'


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):

    # Define the meta attributes for the serializer to reference
    class Meta:
        model = Comment
        fields = ['text']

    # Create a comment
    def create(self, validated_data):
        return super().create(validated_data | {"author": self.context['request'].user})


# Like Serializer
class LikeSerializer(serializers.ModelSerializer):

    # Define the meta attributes for the serializer to reference
    class Meta:
        model = Restaurant
        fields = []


class BlogSerializer(serializers.ModelSerializer):

    # Define the meta attributes for the serializer to reference
    class Meta:
        model = Blog
        fields = ['title', 'description', 'image']


# Like Serializer
class BlogLikeSerializer(serializers.ModelSerializer):

    # Define the meta attributes for the serializer to reference
    class Meta:
        model = Blog
        fields = []

