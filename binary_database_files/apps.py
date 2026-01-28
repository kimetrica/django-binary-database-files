from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Error, register


class DatabaseFilesAppConfig(AppConfig):
    """AppConfig to make binary_database_files compatible with app loading"""

    name = "binary_database_files"
    label = "binary_database_files"
    verbose_name = "django-binary-database-files"


@register()
def check_settings(app_configs, **kwargs):
    errors = []
    if not settings.MEDIA_ROOT and settings.DATABASE_FILES_URL_METHOD_NAME == "URL_METHOD_1":
        errors.append(
            Error(
                "MEDIA_ROOT is not defined, yet you are using URL_METHOD_1 which serves media files from the filesystem.",
                hint="If you intend to only serve files from the database, use URL_METHOD_2.",
                id="binary_database_files.E001",
            )
        )
    if not settings.MEDIA_ROOT and settings.DB_FILES_AUTO_EXPORT_DB_TO_FS:
        errors.append(
            Error(
                "MEDIA_ROOT is not defined, yet you are using DB_FILES_AUTO_EXPORT_DB_TO_FS which copies media files from the filesystem.",
                hint="If you intend to only serve files from the database, set DB_FILES_AUTO_EXPORT_DB_TO_FS to False.",
                id="binary_database_files.E002",
            )
        )
    return errors