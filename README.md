# iamheadless_publisher_admin_images

App to render homepage item type in `iamheadless_publisher_admin` frontend.

## Installation

Requires `iamheadless_publisher_admin`
Requires `iamheadless_publisher_file_handling`

1. install package
2. add `iamheadless_publisher_admin_images` to `INSTALLED_APPS` in `settings.py`
3. add viewsets to `IAMHEADLESS_PUBLISHER_ADMIN_VIEWSET_LIST` in `settings.py`
```
[
    'iamheadless_publisher_admin_images.viewsets.ImageCreateViewSet',
    'iamheadless_publisher_admin_images.viewsets.ImageDeleteViewSet',
    'iamheadless_publisher_admin_images.viewsets.ImageRetrieveUpdateViewSet',
]
```
