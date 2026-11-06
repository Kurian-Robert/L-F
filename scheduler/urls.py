from django.urls import path
from .views import claim_scheduler_view, login_view, logout_view

urlpatterns = [
    path("", claim_scheduler_view, name="claim_scheduler"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
