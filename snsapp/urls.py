from django.urls import path
from .views import Home, MyPost, DetailPost,CreatePost


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('mypost/', MyPost.as_view(), name='mypost'),
    path('detail/<int:pk>', DetailPost.as_view(), name='detail'),
    path('create/', CreatePost.as_view(), name='create'),

]
