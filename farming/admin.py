from django.contrib import admin

from .models import Crop, FarmingSeason, FarmingStage

admin.site.register(Crop)
admin.site.register(FarmingSeason)
admin.site.register(FarmingStage)
