from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from farm.models import Farm
from farming.models import FarmingSeason

from .forms import FarmTaskForm
from .models import FarmTask
from .utils import parse_to_checkbox


@login_required(login_url="/account/login/")
def task_home_view(request):

    tasks = FarmTask.objects.all()

    if request.method == "POST":
        filter_name = request.POST.get("filter-name")
        search_term = request.POST.get("search")

        if filter_name == "status":
            filters = Q(status=search_term)
        elif filter_name == "farm":
            filters = Q(farm=search_term)
        else:
            filters = Q(farming_season=search_term)

        try:
            tasks = FarmTask.objects.select_related("farm", "farming_season").filter(
                filters
            )
        except ValueError:
            messages.error(
                request, "Make sure the filter name matches with the search term"
            )

    context = {
        "tasks": tasks,
        "form": FarmTaskForm(),
        "farms": Farm.objects.all(),
        "seasons": FarmingSeason.objects.all(),
    }
    return render(request, "task/index.html", context)


@login_required(login_url="/account/login/")
def add_task(request):
    if request.method == "POST":
        form = FarmTaskForm(request.POST)
        if form.is_valid():
            farm_task = form.save(commit=False)
            name = farm_task.name
            farm_task.created_by = request.user
            farm_task.objectives = parse_to_checkbox(request.POST.get("objectives"))
            form.save()
            form.save_m2m()  # save m2m fields

            messages.success(request, f""" "{name}" Task added successfully""")
            return redirect("task:home")
        else:
            messages.error(request, form.errors.as_text())

    context = {"form": FarmTaskForm()}
    return render(request, "task/add-task.html", context)


def filter_task(request, status):

    if str(status).lower() in ["ongoing", "pending", "complete", "cancelled"]:
        tasks = FarmTask.objects.filter(status=status)
    else:
        messages.error(
            request,
            'No tasks are available with that status. options: "ongoing","pending", "complete", "cancelled"',
        )
        return redirect("task:home")

    context = {
        "tasks": tasks,
        "form": FarmTaskForm(),
        "farms": Farm.objects.all(),
        "seasons": FarmingSeason.objects.all(),
    }
    return render(request, "task/index.html", context)


@login_required(login_url="/account/login/")
def edit_task(request, pk):

    task = get_object_or_404(FarmTask, pk=pk)

    if request.method == "POST" or request.is_ajax():
        form = FarmTaskForm(request.POST or None, instance=task)

        if form.is_valid():
            name = request.POST.get("name")
            form.save()
            messages.success(request, f' "{name}" updated successfully')
            return redirect("task:home")
        else:
            messages.error(request, form.errors.as_text())

    context = {
        "form": FarmTaskForm(instance=task),
        "objectives": task.objectives,
        "task_id": task.id,
    }

    return render(request, "task/edit-task.html", context)


@login_required(login_url="/account/login/")
def delete_task(request, pk):
    try:
        task = get_object_or_404(FarmTask, pk=pk)
        name = task.name
        task.delete()

        messages.success(request, f' "{name}" deleted successfully"')
    except FarmTask.DoesNotExist:
        messages.error(request, "Farm Task with that id does not exist")

    return redirect("task:home")
