from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('index'))
        else:
            return render(request, 'login.html', {'error_message': 'Неправильные логин и пароль'})
    else:
        return render(request, 'login.html')
