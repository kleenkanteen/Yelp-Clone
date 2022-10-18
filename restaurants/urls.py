from django.urls import path

from restaurants.views import RestaurantList, CreateRestaurantView, UpdateRestaurantView, AddRestaurantCommentView, \
    LikeRestaurantView, CreateBlogView, AddGalleryImageView, LikeBlogView

app_name = 'restaurant'

urlpatterns = [
    # path('/', None, name=''),
    path('all/', RestaurantList.as_view(), name='list-restaurants'),
    path('create/', CreateRestaurantView.as_view(), name='add-restaurant'),
    path('update/', UpdateRestaurantView.as_view(), name='update-restaurant'),
    path('<int:id>/add-img/', AddGalleryImageView.as_view(), name='add-gallery'),
    path('<int:id>/comment/', AddRestaurantCommentView.as_view(), name='add-comment'),
    path('<int:id>/like/', LikeRestaurantView.as_view(), name='add-like'),
    path('<int:id>/blog/', CreateBlogView.as_view(), name='add-blog'),
    path('<int:id>/blog/<int:blogid>/like/', LikeBlogView.as_view(), name='like-blog'),

]