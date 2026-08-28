from django.urls import path, include
from account.views import Profile
from portfolio.views import Skills, SkillDetail

urlpatterns = [
    path('auth/', include('account.urls')),
    path('profile/', view=Profile.as_view()),   # TODO: Restructure the API url structure by moving the `Profile` model to a separate app called `ProfileDashboard`
    path('skills/', view=Skills.as_view()),
    path('skills/<id>/', view=SkillDetail.as_view()),
]