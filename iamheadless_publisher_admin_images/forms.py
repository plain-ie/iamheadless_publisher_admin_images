from django import forms
from django.forms import formset_factory


class ImageContentForm(forms.Form):
    language = forms.CharField(initial='', max_length=255, widget=forms.widgets.HiddenInput())
    title = forms.CharField(initial='', max_length=255)
    summary = forms.CharField(widget=forms.widgets.Textarea(attrs={'readability': 'true'}))
    file_name = forms.CharField(required=False, disabled=True)
    file = forms.FileField(required=False)


ImageContentFormSet = formset_factory(ImageContentForm, extra=0)


class ImageForm(forms.Form):
    pass
