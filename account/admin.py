from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from account.forms import LoginForm

from .models import Farmer, Login, Worker

admin.site.site_header = "Farm Data Management Administration"
admin.site.login_form = LoginForm
admin.site.index_title = "Administration Site"
admin.site.site_title = "Farm Data Management Admin Site"

# UserCreationForm === refer Customizing authentication in Django¶ documentation
# UserChangeForm


# Register your models here.
class LoginAdmin(UserAdmin):
    """admin options  and functionalities"""

    list_display = ("username", "rank")
    search_fields = ("username",)
    readonly_fields = ("id",)

    filter_horizontal = ()
    list_filter = ()

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("rank",)},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "rank"),
            },
        ),
    )


admin.site.register(Login, LoginAdmin)
# since we're not using Django's built-in permissions
# we unregister the Group model from admin
admin.site.unregister(Group)

admin.site.register(Farmer)

admin.site.register(Worker)
