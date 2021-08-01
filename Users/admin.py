from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register()

# from django.apps import Company


# models = apps.get_models()
# print(models)
# for model in models:
#     #  admin.site.register(model)


from django.apps import apps
# all other models
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
