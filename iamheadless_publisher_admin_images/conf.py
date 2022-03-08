from .apps import IamheadlessPublisherAdminImagesConfig as AppConfig


class Settings:

    APP_NAME = AppConfig.name
    ITEM_TYPE = 'images'

    VAR_FORM_TEMPLATE = f'{VAR_PREFIX}_FORM_TEMPLATE'

    @property
    def FORM_TEMPLATE(self):
        return getattr(
            dj_settings,
            self.VAR_FORM_TEMPLATE,
            f'{self.APP_NAME}/form.html'
        )

    def __getattr__(self, name):
        return getattr(dj_settings, name)


settings = Settings()
