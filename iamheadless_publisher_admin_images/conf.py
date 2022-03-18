from .apps import IamheadlessPublisherAdminImagesConfig as AppConfig


class Settings:

    APP_NAME = AppConfig.name
    ITEM_TYPE = 'images'

    URLNAME_CREATE_ITEM = f'admin-create-{ITEM_TYPE}'
    URLNAME_DELETE_ITEM = f'admin-delete-{ITEM_TYPE}'
    URLNAME_RETRIEVE_UPDATE_ITEM = f'admin-edit-{ITEM_TYPE}'

    RETRIEVE_TEMPLATE = 'iamheadless_publisher_admin/pages/item.html'

    @property
    def FORM_TEMPLATE(self):
        return f'{self.APP_NAME}/form.html'

    def __getattr__(self, name):
        return getattr(dj_settings, name)


settings = Settings()
