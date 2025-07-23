from django import forms
from .models import SlideImage

class SlideImageForm(forms.ModelForm):
    class Meta:
        model = SlideImage
        fields = ['title', 'image_file']
