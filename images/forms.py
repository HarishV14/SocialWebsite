from django import forms

from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {'url': forms.HiddenInput,} #attribute is hidded type=hidden

    # this external validation to the that url should only extension in the jpg and jpeg
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url  

    """Overide save Method
    normal save() method to save the current model instance to the database and return the object 
    will override the save() method of your form in order to retrieve the given image and save it
    """
    def save(self, force_insert=False,
        force_update=False,commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        # download image from the given URL
        response = request.urlopen(image_url) #open the url and download the image
        
        """image.image.save(): Saves the downloaded image data to the image field of the model. 
                               It uses image_name as the file name.
           ContentFile(response.read()) wraps the image data into a file-like object, allowing 
                                        it to be saved to the model field.
           save=False ensures that the model is not yet committed to the database."""
        image.image.save(image_name,ContentFile(response.read()),save=False) 

        if commit:
            image.save()
        return image
