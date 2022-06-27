from django.urls import path, include
from django.views.generic import TemplateView

from users import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    
    path('sing_up/<uidb64>/<token>', views.SingUpView.as_view()),

    path(
        'sing_up/',
        TemplateView.as_view(template_name='users/sing_up.html'),
        name='sing_up'),
]