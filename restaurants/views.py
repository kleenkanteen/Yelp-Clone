# Create your views here.
from django.core.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser

from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer, CommentSerializer, LikeSerializer, BlogSerializer, \
    GallerySerializer, BlogLikeSerializer
from notifications.models import Notification
from django.shortcuts import get_object_or_404


# View to list all the restaurants
class RestaurantList(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


# View to create a restaurant post
class CreateRestaurantView(CreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    # def preform_create(self, serializer):
    #     return serializer.save(owner=self.request.user)


class AddGalleryImageView(CreateAPIView):
    serializer_class = GallerySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])
        img = serializer.save(restaurant=restaurant)
        restaurant.gallery.add(img)
        restaurant.save()

        return img


# View to update a restaurant
class UpdateRestaurantView(UpdateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Restaurant.objects.get(owner=self.request.user)


# View to create a comment on a restaurant
class AddRestaurantCommentView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])
        comment = serializer.save(restaurant=restaurant)
        restaurant.comments.add(comment)

        curr = self.request.user
        notif = Notification.objects.create(user=restaurant.owner,
            message=f"{curr.first_name} {curr.last_name} has commented on your "
            f"restaurant {restaurant.name}")

        restaurant.save()


# View to update a blog post so that a user can like it
class LikeRestaurantView(UpdateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])
        if self.request.user in restaurant.likes.all():
            restaurant.likes.remove(self.request.user)
        else:
            restaurant.likes.add(self.request.user)
        restaurant.save()

        curr = self.request.user
        Notification.objects.create(user=restaurant.owner,
        message=f'{curr.first_name} {curr.last_name} has '
        f'liked your restaurant {restaurant.name}')
        return self.request.user


# View to create a blog post that is listed inside the restaurant
class CreateBlogView(CreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])
        if restaurant.owner == self.request.user:
            blog = serializer.save(restaurant=restaurant)
            fans = restaurant.fans.all()
            for fan in fans:
                Notification.objects.create(user=fan.id,
                    message=f'{restaurant.name} has posted a new blog')
            restaurant.blogs.add(blog)
            restaurant.save()
        else:
            raise PermissionDenied()


# View to like a blog post
class LikeBlogView(UpdateAPIView):
    serializer_class = BlogLikeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['id'])

        blog_post = restaurant.blogs.get(pk=self.kwargs['blogid'])
        if self.request.user in blog_post.likes.all():
            blog_post.likes.remove(self.request.user)
        else:
            blog_post.likes.add(self.request.user)
            curr = self.request.user
            Notification.objects.create(user=restaurant.owner.id,
            message=f"{curr.first_name} {curr.last_name} has liked your "
            f"restaurant {restaurant.name}'s blog post about {blog_post.title}")

        blog_post.save()
