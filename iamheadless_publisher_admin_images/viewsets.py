from django.shortcuts import reverse
from django.urls import path

from iamheadless_publisher_admin.viewsets.base import (
    BaseItemCreateViewSet,
    BaseItemDeleteViewSet,
    BaseItemRetrieveUpdateViewSet,
)

from .conf import settings
from . import pydantic_models


PYDANTIC_MODEL = pydantic_models.ImagePydanticModel


class ImageCreateViewSet(BaseItemCreateViewSet):

    pydantic_model = PYDANTIC_MODEL
    item_type = pydantic_model._item_type
    urlname = settings.URLNAME_CREATE_ITEM
    template = settings.RETRIEVE_TEMPLATE

    #

    def get_retrieve_url(self, item_id):
        return reverse(
            settings.URLNAME_RETRIEVE_UPDATE_ITEM,
            kwargs={
                'project_id': self.get_project_id(),
                'tenant_id': self.get_tenant_id(),
                'item_id': item_id
            }
        )

    #

    @classmethod
    def get_route(cls, prefix=''):
        path_pattern = rf'{prefix}'
        path_pattern += r'projects/<str:project_id>/'
        path_pattern += r'tenants/<str:tenant_id>/'
        path_pattern += rf'item-types/{cls.item_type}/'
        return path(path_pattern, cls.as_view(), name=cls.urlname)

    @classmethod
    def get_urlpatterns(cls, prefix=''):
        route = cls.get_route(prefix=prefix)
        if route is not None:
            return [route, ]
        return []


class ImageRetrieveUpdateViewSet(BaseItemRetrieveUpdateViewSet):

    pydantic_model = PYDANTIC_MODEL
    item_type = pydantic_model._item_type
    urlname = settings.URLNAME_RETRIEVE_UPDATE_ITEM
    template = settings.RETRIEVE_TEMPLATE

    @classmethod
    def get_route(cls, prefix=''):
        path_pattern = rf'{prefix}'
        path_pattern += r'projects/<str:project_id>/'
        path_pattern += r'tenants/<str:tenant_id>/'
        path_pattern += rf'item-types/{cls.item_type}/'
        path_pattern += r'items/<str:item_id>/'
        return path(path_pattern, cls.as_view(), name=cls.urlname)

    def get_delete_url(self):
        return reverse(
            settings.URLNAME_DELETE_ITEM,
            kwargs={
                'project_id': self.get_project_id(),
                'tenant_id': self.get_tenant_id(),
                'item_id': self.get_item_id()
            }
        )

    def get_preview_url(self):
        return '#'

    def get_create_url(self):
        return reverse(
            settings.URLNAME_CREATE_ITEM,
            kwargs={
                'project_id': self.get_project_id(),
                'tenant_id': self.get_tenant_id(),
            }
        )


class ImageDeleteViewSet(BaseItemDeleteViewSet):

    pydantic_model = PYDANTIC_MODEL
    item_type = pydantic_model._item_type
    urlname = settings.URLNAME_DELETE_ITEM

    @classmethod
    def get_route(cls, prefix=''):
        path_pattern = rf'{prefix}'
        path_pattern += r'projects/<str:project_id>/'
        path_pattern += r'tenants/<str:tenant_id>/'
        path_pattern += rf'item-types/{cls.item_type}/'
        path_pattern += r'items/<str:item_id>/'
        path_pattern += r'delete/'
        return path(path_pattern, cls.as_view(), name=cls.urlname)
