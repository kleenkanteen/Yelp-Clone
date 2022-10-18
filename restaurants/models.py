from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from accounts.models import CustomUser


# Add a custom search Query function called search
class RestaurantQuerySet(models.query.QuerySet):
    def search(self, query):
        if query:
            query = query.strip()
            return self.filter(Q(name__icontains=query) | Q(location__icontains=query)).distinct()
        return self


# Restaurant Manager to register the search Query function
class RestaurantManager(models.Manager):
    def queryset(self):
        return RestaurantQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.queryset().search(query)


# Menu Model
class Menu(models.Model):
    name = models.CharField(max_length=200, help_text='Enter Restaurant Name', default='Restaurant Name')
    items = models.TextField(help_text='Format - ItemType : {Item : price}, ItemType : {Item : price}, ...',
                             null=True, blank=True)

    # Str Representation for the Menu Model
    def __str__(self):
        return f'{self.name}\'s Menu'

    # Method to get the list of items
    def get_items(self):
        return {"title": self.items.split(' ')[0], "items": self.items.split(':', 1)[1].split(', ')}


# Gallery Model
class Gallery(models.Model):
    name = models.CharField(max_length=200, help_text='Enter Restaurant Name', default='Restaurant')
    image = models.ImageField(upload_to='gallery/', null=True, blank=True)

    # Str Representation for the Gallery Model
    def __str__(self):
        return f'{self.id}: IMG'


# Comment Model
class Comment(models.Model):
    author = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(help_text='Enter your comment')
    created_at = models.DateTimeField(auto_now_add=True)

    # Str Representation for the Comment Model
    def __str__(self):
        return f'{self.id} : {self.author.username}\'s Comment'


# Comment Model
class Blog(models.Model):
    title = models.CharField(max_length=200, help_text="Enter Blogs Title", default="Blog Title")
    description = models.TextField(help_text="Enter Blogs description")
    image = models.ImageField(upload_to='header/', null=True, blank=True)
    likes = models.ManyToManyField(CustomUser, related_name="blog_likes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Str Representation for the Blog Model
    def __str__(self):
        return f'{self.id} : {self.title}\' Blog'

    # Method to return the total number of likes
    def total_likes(self):
        return self.likes.count()


# Restaurant Model
class Restaurant(models.Model):
    owner = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, help_text='Enter Restaurant Name')
    location = models.CharField(max_length=200, null=True, blank=True)
    general_info = models.CharField(max_length=2000, help_text='Enter Restaurant Description')
    followers = models.PositiveIntegerField(default=0)
    fans = models.ManyToManyField(CustomUser, related_name="fans", blank=True)
    likes = models.ManyToManyField(CustomUser, related_name="restaurant_likes", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    postal_code = models.CharField(max_length=7, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)

    menu = models.ForeignKey(to=Menu, on_delete=models.CASCADE, null=True, blank=True)

    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    gallery = models.ManyToManyField(Gallery, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    blogs = models.ManyToManyField(Blog, blank=True)

    objects = RestaurantManager()

    # Order the restaurants by name
    class Meta:
        ordering = ['name']

    # Str Representation for the Restaurant Model
    def __str__(self):
        return f'ID: {self.pk} | {self.name} - {self.general_info}'

    # Method to return the total number of likes
    def total_likes(self):
        return self.likes.count()
