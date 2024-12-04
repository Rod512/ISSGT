from django import forms
from .models import Books

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['book_name', 'pdf', 'book_image']

        widgets = {
            'book_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book name'}),
            'pdf': forms.FileInput(attrs={'class': 'form-control'}),
            'book_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
