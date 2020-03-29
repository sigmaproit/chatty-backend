from django.apps import apps
from django.conf import settings


def get_model_from_app_model_name(app_model_name):
    if app_model_name:
        app_model_names_list = app_model_name.split('.')
        return apps.get_model(app_model_names_list[0], app_model_names_list[1])


def get_grouping_entity_from_request(request):
    if settings.CHATY_BASE_GROUPING_ENTITY_FIELD_NAME and hasattr(request,
                                                                  settings.CHATY_BASE_GROUPING_ENTITY_FIELD_NAME):
        return getattr(request, settings.CHATY_BASE_GROUPING_ENTITY_FIELD_NAME)
    return None
