from django.contrib import admin

from .models import FarmingSeason, FarmingStage, Crop

admin.site.register(Crop)
admin.site.register(FarmingSeason)
admin.site.register(FarmingStage)
