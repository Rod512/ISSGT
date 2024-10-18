from django.db import models
from django.utils import timezone
from django.urls import reverse

class HomeBlog(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80, unique=True)
    published_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='photos/blog')

    class Meta:
        ordering = ['-published_date'] 

    def __str__(self):
        return self.title  

    def get_absolute_url(self):
        return reverse('blog_post_detail', args=[self.slug]) 



