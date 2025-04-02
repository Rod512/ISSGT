from django.db import models

class Books(models.Model):
    book_name = models.CharField(max_length=100)
    book_author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='pdf/books',blank=True, null=True)
    book_image = models.ImageField(upload_to='photos/books', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book_name
    
    class Meta:
        verbose_name = 'Books'
        verbose_name_plural = 'Books'

 
