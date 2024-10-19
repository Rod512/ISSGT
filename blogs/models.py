from django.db import models
from home.models import HomeBlog
# from django.contrib.auth.models import User
from django.conf import settings
 

class Blogs(models.Model):
    Blog_name = models.CharField(max_length=100, unique=True)
    Blog_description = models.TextField()
    Blog_image = models.ImageField(upload_to='photos/blog')
    Blog_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(HomeBlog, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.Blog_name
