from django import forms
from .models import HomeBlog, Category

class Homeblogform(forms.ModelForm):
    class Meta:
        model = HomeBlog
        fields = ['category', 'slug','blog_name', 'image', 'is_featured', 'content' ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique slug'}),
            'blog_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique name'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your content here'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique slug'}),
        }


# class SearchForm(forms.Form):
#     query = forms.CharField(label="Search", max_length=100, required=True)
