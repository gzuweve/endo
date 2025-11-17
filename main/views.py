import json
from datetime import date
from idlelib.macosx import preferTabsPreferenceWarning

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from main.forms import RegistrationForm, LoginForm
from main.models import Order, Status


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
    user = request.user
    user_id = user.id
    pending_orders = (Order.objects
              .filter(user=user)  # или .filter(customer=request.user)
              .filter(status=Status.NOTDONE)
              .select_related('material'))  # если есть M2M/related set
    for i in range(len(pending_orders)):
        if pending_orders[i].deadline < date.today():
            pending_orders[i].outofdeadline = True
        else:
            pending_orders[i].outofdeadline = False
    in_progress_orders = (Order.objects
              .filter(user=user)  # или .filter(customer=request.user)
              .filter(status=Status.INWORK)
              .select_related('material'))
    for i in range(len(in_progress_orders)):
        if in_progress_orders[i].deadline < date.today():
            in_progress_orders[i].outofdeadline = True
        else:
            in_progress_orders[i].outofdeadline = False

    print(in_progress_orders)
    completed_orders = (Order.objects
              .filter(user=user)  # или .filter(customer=request.user)
              .filter(status=Status.DONE)
              .select_related('material'))
    print(completed_orders)
    return render(request, "home.html", {'pending_orders': pending_orders,
                                         "in_progress_orders": in_progress_orders, "completed_orders": completed_orders})

def order_detail(request, id):
    # Получаем заказ или возвращаем 404 если не найден
    order = get_object_or_404(Order, id=id)

    # Проверяем просрочен ли дедлайн
    is_overdue = order.deadline < date.today() if order.deadline else False

    # Дополнительная информация для контекста
    context = {
        'order': order,
        'is_overdue': is_overdue,
        'now': timezone.now(),
    }

    return render(request, "order_detail.html", context)


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
                print(username, password)
        else:
            messages.error(request, 'Неверные данные, пожалуйста, исправьте ошибки в форме!')
            print(form.errors.as_text())
    else:
        form = LoginForm()


    return render(request, "login.html",{'form': form})

def forgotpassword(request):
    return render(request, "forgotpassword.html")

def settings (request):
    return render(request, "settings.html")


@csrf_exempt
def update_status(request, id):
    if request.method == 'PATCH':
        data = json.loads(request.body)
        status = data["status"]

        order = get_object_or_404(Order, id=id)
        order.status = status
        order.save()
        return JsonResponse({"success": True, "status": status})




