from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name="blogs"),
    path('blogs/<slug:slug>/', views.single_blog, name='single_blog'),
    path('<slug:slug>/add-comment/', views.add_comment, name='add_comment'),
]
