from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignUpView, CodeCorrect, CodeInvalid

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('correct/', CodeCorrect, name='code_correct'),
    path('invalid/', CodeInvalid, name='code_invalid'),
]
