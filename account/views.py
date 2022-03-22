from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render

from .forms import FarmerForm, LoginForm, SignUpForm, WorkerForm
from .models import Farmer, Worker


def redirect_to_login(request):
    """redirects to login page"""
    return redirect("account:login")


def login_view(request):
    if request.user.is_authenticated:
        # messages.info(request, "You've already logged in")
        return redirect("farm:farm-home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # check if the user is a admin
            # if not check if the have Worker account
            if not user.is_admin:
                try:
                    Worker.objects.get(login_id=user)
                except Worker.DoesNotExist:
                    messages.info(
                        request,
                        "Please add information about you in your profile below before proceeding",
                    )
                    return redirect("account:profile")
            else:
                try:
                    Farmer.objects.get(login_id=user)
                except Farmer.DoesNotExist:
                    messages.info(
                        request,
                        "Please add information about you in your profile below before proceeding",
                    )
                    return redirect("account:profile")

            return redirect("farm:farm-home")
        else:
            messages.error(request, "username or password is incorrect")

    form = LoginForm()
    return render(request, "account/login.html", {"form": form})


def logout_view(request):
    # implement to handle POST request only
    logout(request)
    return redirect("account:login")


def signup(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(
                request,
                f"Welcome, Account created successfully for {username}. Please Login",
            )
            # redirect to login
            return redirect("account:login")
        else:
            messages.error(request, form.errors.as_text())
    return render(request, "account/signup.html", {"form": form})


@login_required(login_url="/account/login/")
def profile(request):

    # get the current user
    username = request.user.username
    user_model = get_user_model()

    user = user_model.objects.filter(Q(username__iexact=username)).first()

    if request.method == "POST":

        if user.is_admin or user.is_manager:
            # meaning the form was submitted by user
            # who is admin or manager
            farmer_form = FarmerForm(request.POST)

            if farmer_form.is_valid():
                farmer = Farmer.objects.filter(login_id=user).first()
                if farmer is None:
                    # meaning the user has no farmer account
                    # create new Farmer account
                    farmer = farmer_form.save(commit=False)
                    farmer.login_id = user
                    farmer.save()
                else:
                    # the user has the Farmer details, hence
                    # update the Farmer details
                    farmer.first_name = farmer_form.cleaned_data["first_name"]
                    farmer.last_name = farmer_form.cleaned_data["last_name"]
                    farmer.national_id = farmer_form.cleaned_data["national_id"]
                    farmer.phone_no = farmer_form.cleaned_data["phone_no"]
                    farmer.login_id = user
                    farmer.save()

                messages.success(request, "Profile update successfully")
            else:
                # check out how to display form errors
                messages.error(request, "ERROR")

        else:
            # the user is a worker
            worker_form = WorkerForm(request.POST)

            if worker_form.is_valid():
                worker = Worker.objects.filter(login_id=user).first()
                if worker is None:
                    # meaning the user has no worker account
                    # create new Worker account
                    worker = worker_form.save(commit=False)
                    worker.login_id = user
                    worker.save()
                else:
                    # the user has the Worker details, hence
                    # update the Worker details
                    worker.first_name = worker_form.cleaned_data["first_name"]
                    worker.last_name = worker_form.cleaned_data["last_name"]
                    worker.national_id = worker_form.cleaned_data["national_id"]
                    worker.phone_no = worker_form.cleaned_data["phone_no"]
                    worker.login_id = user
                    worker.save()

                messages.success(request, "Profile update successfully")
            else:
                # check out how to display form errors
                messages.info(request, "ERROR")

    context = {"form": None, "personal_data": None, "title": "Worker"}

    if user.is_admin or user.is_manager:
        try:
            farmer = Farmer.objects.filter(login_id=user).first()
        except Farmer.DoesNotExist:
            farmer = Farmer()
            messages.info(request, "Please add information about you below")

        farmer_form = FarmerForm(instance=farmer)

        context["personal_data"] = farmer
        context["form"] = farmer_form
        context["title"] = "Farmer/manager"
    else:
        try:
            worker = Worker.objects.filter(login_id=user).first()
        except Worker.DoesNotExist:
            worker = Worker()
            messages.info(request, "Please add information about you below")

        # if user.check_password("aura2021"):
        #     print("hello world")

        worker_form = WorkerForm(instance=worker)

        context["personal_data"] = worker
        context["form"] = worker_form
        context["title"] = "Worker"

    return render(request, "account/profile.html", context)
