from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name="blogs"),
    path('blogs/<slug:slug>/', views.single_blog, name='single_blog'),
]
