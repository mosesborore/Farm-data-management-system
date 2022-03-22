from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Farmer, Login, Worker

admin.site.site_header = "Farm Data Management Administration"

# UserCreationForm === refer Customizing authentication in Django¶ documentation
# UserChangeForm


# Register your models here.
class LoginAdmin(UserAdmin):
    """admin options  and functionalities"""

    list_display = (
        "username",
        "date_joined",
        "last_login",
        "is_admin",
        "is_manager",
        "is_staff",
        "is_active",
    )
    search_fields = ("username",)
    readonly_fields = ("id", "date_joined", "last_login")

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
                    "avatar",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_manager",
                    "is_active",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "avatar",
                    "password1",
                    "password2",
                    "is_admin",
                    "is_manager",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )


admin.site.register(Login, LoginAdmin)
# since we're not using Django's built-in permissions
# we unregister the Group model from admin
admin.site.unregister(Group)

admin.site.register(Farmer)

admin.site.register(Worker)
