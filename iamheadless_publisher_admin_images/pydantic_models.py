import uuid

from typing import List, Optional

from django.core.exceptions import ValidationError
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from iamheadless_publisher_admin.pydantic_models import BaseItemPydanticModel, BaseItemDataPydanticModel, BaseItemContentsPydanticModel
from iamheadless_file_handling import utils as iamheadless_file_handling_utils

from .conf import settings
from . import forms


PREFIX_CONTENTS_FORMSET = 'contents_formset'


class ImageContentPydanticModel(BaseItemContentsPydanticModel):
    title: str
    language: str
    summary: Optional[str]
    file_name: str


class ImageDataPydanticModel(BaseItemDataPydanticModel):
    contents: List[ImageContentPydanticModel]


class ImagePydanticModel(BaseItemPydanticModel):

    _content_model = ImageContentPydanticModel
    _data_model = ImageDataPydanticModel
    _display_name_plural = 'images'
    _display_name_singular = 'image'
    _item_type = settings.ITEM_TYPE
    _project_admin_required = False
    _tenant_required = True

    data: ImageDataPydanticModel

    @property
    def TITLE(self):
        _data = self.DATA
        _contents = _data.get('data', {}).get('contents', [])
        _display_content = ImagePydanticModel.get_display_content(_contents, self._primary_language)
        return _display_content['title']

    @property
    def EDIT_URL(self):

        _data = self.DATA

        project_id = _data.get('project', None)
        tenant_id = _data.get('tenant', None)
        item_id = _data.get('id', None)

        return reverse(
            settings.URLNAME_RETRIEVE_UPDATE_ITEM,
            kwargs={
                'project_id': project_id,
                'tenant_id': tenant_id,
                'item_id': item_id
            }
        )

    @property
    def FILE_NAME(self):
        _data = self.DATA
        _contents = _data.get('data', {}).get('contents', [])
        _display_content = ImagePydanticModel.get_display_content(_contents, self._primary_language)
        return _display_content['file_name']

    #

    @classmethod
    def viewsets(cls):
        return [
            f'{settings.APP_NAME}.viewsets.ImageCreateViewSet',
            f'{settings.APP_NAME}.viewsets.ImageDeleteViewSet',
            f'{settings.APP_NAME}.viewsets.ImageRetrieveUpdateViewSet',
        ]

    @classmethod
    def get_item_type(cls, data):
        return data['item_type']

    @classmethod
    def render_form(
            cls,
            request,
            initial_data
            ):

        initial_item = initial_data.get('data', {})
        initial_contents = initial_data.get('data', {}).get('contents', [])
        if initial_contents == []:
            initial_contents = [{'language': cls._primary_language}]

        content_formset = forms.ImageContentFormSet(initial=initial_contents, prefix=PREFIX_CONTENTS_FORMSET)
        form = forms.ImageForm(initial=initial_item)

        if request.method == 'POST':
            content_formset = forms.ImageContentFormSet(request.POST, initial=initial_contents, prefix=PREFIX_CONTENTS_FORMSET)
            form = forms.ImageForm(request.POST, initial=initial_item)

        return render_to_string(
            settings.FORM_TEMPLATE,
            context={
                'content_formset': content_formset,
                'form': form,
            }
        )

    @classmethod
    def validate_form(
            cls,
            request,
            initial_data
            ):

        data = {}
        if request.method == 'POST':
            data = request.POST

        initial_item = initial_data.get('data', {})
        initial_contents = initial_data.get('data', {}).get('contents', [])

        content_formset = forms.ImageContentFormSet(request.POST, initial=initial_contents, prefix=PREFIX_CONTENTS_FORMSET)
        form = forms.ImageForm(request.POST, initial=initial_item)

        valid = []

        valid.append(content_formset.is_valid())
        valid.append(form.is_valid())

        if False in valid:
            raise ValidationError(_('Form is invalid'))

        validated_data =  {
            'data': form.cleaned_data,
        }

        contents = content_formset.cleaned_data

        validated_data['data']['contents'] = content_formset.cleaned_data

        return validated_data

    @classmethod
    def pre_create(cls, request, validated_data):
        tenant_id = iamheadless_publisher_admin_utils.get_request_tenant_id(request)
        for index, file in enumerate(request.FILES.items(), start=0):
            file_index = file[0].replace(f'{PREFIX_CONTENTS_FORMSET}-', '')
            file_index = file_index.replace(f'-file', '')
            file_index = int(file_index)
            try:
                validated_data['data']['contents'][file_index]['file_name'] = iamheadless_file_handling_utils.get_file_name(tenant_id, file[1].name)
            except IndexError:
                pass
        return validated_data

    @classmethod
    def pre_update(cls, request, validated_data):
        return cls.pre_create(request, validated_data)

    #

    @classmethod
    def post_create(cls, request, validated_data):
        for index, file in enumerate(request.FILES.items(), start=0):
            file_index = file[0].replace(f'{PREFIX_CONTENTS_FORMSET}-', '')
            file_index = file_index.replace(f'-file', '')
            file_index = int(file_index)
            file_name = validated_data['data']['contents'][file_index]['file_name']
            upload_file(file[1].read(), file_name)
        return validated_data

    @classmethod
    def post_update(cls, request, validated_data):
        return cls.post_create(request, validated_data)

    @classmethod
    def post_delete(cls, request, validated_data):
        contents = validated_data['data']['contents']
        for content in contents:
            delete_file(content['file_name'])
        return validated_data


def upload_file(file, file_name):
    file_handling = iamheadless_file_handling_utils.get_file_handling_backend()
    file_handling.upload(file, file_name)


def delete_file(file_name):
    file_handling = iamheadless_file_handling_utils.get_file_handling_backend()
    file_handling.remove(file_name)
