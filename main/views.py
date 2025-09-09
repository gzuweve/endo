from idlelib.macosx import preferTabsPreferenceWarning

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from main.forms import RegistrationForm, LoginForm


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            print(form.errors.as_text())
    else:
        form = RegistrationForm()

    return render(request, "registration.html", {'form': form})
@login_required (login_url='login')
def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    messages.success(request, 'Выход из аккаунта прошёл успешно!')
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data.get('remember')
            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)

                messages.success(request, 'Вы вошли в аккаунт!')
                return redirect('home')
            else:
                messages.error(request, 'Неверный логин или пароль.')
                print(form.errors.as_text())
        else:
            messages.error(request, 'Неверные данные, пожалуйста, исправьте ошибки в форме!')
            print(form.errors.as_text())
    else:
        form = LoginForm()


    return render(request, "login.html",{'form': form})

def forgotpassword(request):
    return render(request, "forgotpassword.html")