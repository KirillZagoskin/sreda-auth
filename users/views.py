from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render
from django.views import View

from users.services.authentication.register import get_user_and_check_token


User = get_user_model()

class SingUpView(View):

    def get(self, request, uidb64, token):
        user, check_token = get_user_and_check_token(uidb64, token)
        if user is not None and check_token:
            login(request, user)
        return redirect('sing_up')



    
