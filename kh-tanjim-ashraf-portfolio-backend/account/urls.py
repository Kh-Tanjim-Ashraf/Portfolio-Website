from django.urls import path
from .views import Login
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', view=Login.as_view()),
    path('refresh/', view=TokenRefreshView.as_view()),
]