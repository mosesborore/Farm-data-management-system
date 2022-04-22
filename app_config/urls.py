from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("account.urls", namespace="account")),
    path("farm/", include("farm.urls", namespace="farm")),
    path("farming/", include("farming.urls", namespace="farming")),
    path("input/", include("input.urls", namespace="input")),
    path("task/", include("task.urls", namespace="task")),
    path("weather/", include("weather.urls", namespace="weather")),
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
]

if settings.DEBUG:
    # import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += [
    #     path("__debug__/", include(debug_toolbar.urls)),
    # ]
