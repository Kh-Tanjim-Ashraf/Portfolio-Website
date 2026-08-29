from django.urls import path, include
from account.views import Profile
from portfolio.views import (
    Skills, 
    SkillDetail, 
    Experiences, 
    ExperienceDetail, 
    Education,
    EducationDetail,
    Projects
)

urlpatterns = [
    path('auth/', include('account.urls')),
    path('profile/', view=Profile.as_view()),   # TODO: Restructure the API url structure by moving the `Profile` model to a separate app called `ProfileDashboard`

    # Skill
    path('skills/', view=Skills.as_view()),
    path('skills/<int:id>/', view=SkillDetail.as_view()),

    # Experience
    path('experiences/', view=Experiences.as_view()),
    path('experiences/<int:id>/', view=ExperienceDetail.as_view()),

    # Education
    path('education/', view=Education.as_view()),
    path('education/<int:id>/', view=EducationDetail.as_view()),

    # Project
    path('projects/', view=Projects.as_view()),
]