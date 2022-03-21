from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class CustomAuthentication(ModelBackend):
    """ authenticate against settings.AUTH_USER_MODEL 
		# override default authentication to allow user to log in with national_id or username
    """
    def authenticate(self, request, **kwargs):
        return super().authenticate(request, **kwargs)
