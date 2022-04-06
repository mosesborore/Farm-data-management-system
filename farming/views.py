from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CropForm, FarmingSeasonForm
from .models import Crop, FarmingSeason, FarmingStage


def home(request):

    if request.method == "POST":
        form = FarmingSeasonForm(request.POST)
        if form.is_valid():
            name = request.POST.get("name")
            form.save()
            messages.success(request, f' "{name}" season added successfully')

    seasons = FarmingSeason.objects.all()

    context = {"seasons": seasons, "form": FarmingSeasonForm}
    return render(request, "farming/index.html", context)


def edit_season(request, pk):
    season = get_object_or_404(FarmingSeason, pk=pk)

    if request.method == "POST":
        form = FarmingSeasonForm(request.POST or None, instance=season)
        if form.is_valid():
            form.save()
            messages.success(request, "Season data updated successfully")

            return redirect("farming:home")
        else:
            messages.error(request, form.errors.as_text)

    context = {"form": FarmingSeasonForm(instance=season), "pk": season.pk}

    return render(request, "farming/edit-season.html", context)


@require_POST
def delete_season(request, pk):
    try:
        delete = request.POST.get("delete")
        if delete:
            season = get_object_or_404(FarmingSeason, pk=pk)
            name = season.name
            season.delete()
            messages.success(request, f'"{name}" deleted successfully')
        else:
            messages.info(
                request,
                "If you want to delete the season, make sure the checkbox is checked",
            )
    except FarmingSeason.DoesNotExist:
        messages.error(request, "Season does not exist")

    return redirect("farming:home")


def crop_list(request):
    crops = Crop.objects.prefetch_related("crops").annotate(
        planted_times=Count("crops")
    )

    if request.method == "POST":
        form = CropForm(request.POST)
        if form.is_valid():
            name = request.POST.get("name")
            form.save()
            messages.success(request, f' "{name}" season added successfully')
        else:
            messages.error(request, form.errors.as_text)

    context = {"crops": crops, "form": CropForm()}

    return render(request, "farming/crop-list.html", context)


def edit_crop(request, pk):
    crop = get_object_or_404(Crop, pk=pk)

    if request.method == "POST":
        form = CropForm(request.POST or None, instance=crop)
        if form.is_valid():
            form.save()
            messages.success(request, "Crop data updated successfully")

            return redirect("farming:crop-list")
        else:
            messages.error(request, form.errors.as_text)

    context = {"form": CropForm(instance=crop), "pk": crop.pk}

    return render(request, "farming/edit-crop.html", context)


@require_POST
def delete_crop(request, pk):
    try:
        delete = request.POST.get("delete")
        if delete:
            crop = get_object_or_404(Crop, pk=pk)
            name = crop.name
            crop.delete()
            messages.success(request, f'"{name}" deleted successfully')
        else:
            messages.info(
                request,
                "If you want to delete the crop, make sure the checkbox is checked",
            )
    except FarmingSeason.DoesNotExist:
        messages.error(request, "Crop does not exist")

    return redirect("farming:crop-list")
