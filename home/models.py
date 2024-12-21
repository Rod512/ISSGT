from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    slug = models.SlugField(unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class HomeBlog(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="blogs", verbose_name="Category")  # Blog category
    slug = models.SlugField(unique=True, verbose_name="Slug")  # URL-friendly slug for each blog
    blog_name = models.CharField(max_length=100,  blank=True, null=True, unique=True)
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Published Date")  # When the blog is published
    image = models.ImageField(upload_to='photos/blogs', blank=True, null=True, verbose_name="Image")  # Blog image
    is_featured = models.BooleanField(default=False, verbose_name="Featured")  # Whether the blog is featured
    content = models.TextField(verbose_name="Content")  # Full content of the blog post
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blogs", verbose_name="Author", default=1)  

    class Meta:
        verbose_name = 'HomeBlog'
        verbose_name_plural = 'Home Blogs'

    def __str__(self):
        return f"{self.category.name} - {self.slug}"

    def get_absolute_url(self):
        return f"/blogs/{self.slug}/"
