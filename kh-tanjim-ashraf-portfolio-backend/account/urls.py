from django.urls import path
from .views import Login, OwnerInfo
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', view=Login.as_view()),
    path('refresh/', view=TokenRefreshView.as_view()),
    path('me/', view=OwnerInfo.as_view()),
]