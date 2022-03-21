from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from account.models import Farmer

from .forms import FarmForm, SoilForm
from .models import Farm, Soil


@login_required(login_url='/account/login/')
def farm_home_view(request):

    if request.method == 'POST':
        
        if request.user.has_perm("add_farm"):
            form = FarmForm(request.POST)
            
            if form.is_valid():
                farmer = Farmer.objects.get(login_id=request.user)
                farm = form.save(commit=False)
                print("FARMER,", farmer)
                farm.farmer_id = farmer
                farm.save()
                messages.success(request, "New farm added successfully")
                return redirect("farm:farm-home")
        else:
            messages.error(request,"Only admins and managers can add farm details")
    
    farms = Farm.objects.all()

    form = FarmForm()
    context = {"farms": farms, "form": form}
    return render(request, "farm/farm-detail.html", context)


@login_required(login_url='/account/login/')
def edit_farm(request, pk):

    if request.method == "POST":
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = get_object_or_404(Farm, pk=pk)
            farm.name = form.cleaned_data['name']
            farm.location = form.cleaned_data['location']
            farm.area = form.cleaned_data['area']
            farm.area_unit = form.cleaned_data['area_unit']

            name = farm.name
            farm.save()
            messages.success(request, f"Farm details for {name} updated")
            return redirect("farm:farm-home")

    # if a get request
    try:
        farm = get_object_or_404(Farm, pk=pk)
    except (farm.DoesNotExist, Http404) as err:
        messages.error(request, "Farm with Farm ID pk does not exit")
        return redirect("farm:farm-detail")

    # populate the form with this modal data
    form = FarmForm(instance=farm)

    context = {"form": form, 'pk': pk}
    return render(request, 'farm/edit-farm.html', context)

@require_POST
@login_required(login_url='/account/login/')
def delete_farm(request, pk):
    """ delete farm with id == pk """
    try:
        delete = request.POST.get('delete', None)
        if delete:
            farm = get_object_or_404(Farm, pk=pk)
            name = farm.name
            farm.delete()
            messages.success(request, f"Farm {name} deleted successfully")
        else:
            messages.info(request,"If you want to delete the record, make sure the checkbox is checked")
        
        return redirect("farm:farm-home")
    except farm.DoesNotExist:
        messages.error(request, "Farm with that Farm ID does not exit")
        return redirect("farm:farm-home")


def soil_detail(request):
    """
        retrieve all soil details
    """
    if request.method == "GET":
        soils = Soil.objects.all()

    if request.method == 'POST':
        form = SoilForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "New soil details added successfully")
            return redirect('farm:soil-detail')
    
    form = SoilForm()
    context = {"soils": soils, "form": form}
    return render(request, "farm/soil-detail.html", context)


def edit_soil_detail(request, pk):

    if request.method == "POST":
        form = SoilForm(request.POST)

        if form.is_valid():
            soil = get_object_or_404(Soil, pk=pk)

            soil.pH = form.cleaned_data['pH']
            soil.color = form.cleaned_data['color']
            soil.texture = form.cleaned_data['texture']
            soil.structure = form.cleaned_data['structure']
            soil.depth = form.cleaned_data['depth']
            soil.testing_date = form.cleaned_data['testing_date']
            soil.last_testing_date = form.cleaned_data['last_testing_date']
            soil.next_testing_date = form.cleaned_data['next_testing_date']
            soil.status = form.cleaned_data['status']
            soil.notes = form.cleaned_data['notes']
            soil.farm_id = form.cleaned_data['farm_id']
            soil.save()
            
            messages.success(request, f"Soil details updated successfully")
            return redirect("farm:soil-detail")

    # if a GET request
    try:
        soil = get_object_or_404(Soil, pk=pk)
    except (soil.DoesNotExist, Http404):
        messages.error(request, "Soil with that ID does not exit")
        return redirect("farm:soil-detail")

    # populate the form with this modal data
    form = SoilForm(instance=soil)

    context = {"form": form, 'pk': pk}
    return render(request, 'farm/edit-soil.html', context)

@require_POST
def delete_soil(request, pk):
    try:
        delete = request.POST.get('delete', None)
        msg = ""
        if delete:
            soil_qs = get_object_or_404(Soil, pk=pk)
            soil_qs.delete()
            messages.success(request,  f"Soil deleted successfully")
        else:
            messages.info(request, _("If you want to delete the record, make sure the checkbox is checked"))
        
        return redirect("farm:soil-detail")
    except soil_qs.DoesNotExist:
        messages.error(request, "Soil with that Soil ID does not exit")
        return redirect("farm:soil-detail")