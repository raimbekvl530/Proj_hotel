from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Редирект на главную страницу инвентаря
            return redirect('index')  # Изменено с 'panel' на 'index'
        else:
            messages.error(request, "Неправильный логин или пароль")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # пароли совпадают?
        if password1 != password2:
            messages.error(request, "Пароли не совпадают")
            return render(request, "accounts/register.html")

        # существует ли пользователь?
        if User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь с таким именем уже существует")
            return render(request, "accounts/register.html")

        try:
            # создаём пользователя
            user = User.objects.create_user(
                username=username,
                password=password1
            )

            # добавляем роль user (с проверкой существования группы)
            try:
                group = Group.objects.get(name="user")
            except Group.DoesNotExist:
                # Если группы нет, создаем
                group = Group.objects.create(name="user")
            
            user.groups.add(group)

            # АВТОМАТИЧЕСКИ ВХОДИМ ПОСЛЕ РЕГИСТРАЦИИ
            login(request, user)
            messages.success(request, "Регистрация успешна!")
            return redirect("index")  # Редирект на главную

        except IntegrityError:
            messages.error(request, "Ошибка: такое имя уже занято.")
            return render(request, "accounts/register.html")

    return render(request, "accounts/register.html")


@login_required
def admin_panel(request):
    # Если нужно, можно оставить отдельную панель
    # Или перенаправить на index если панель не нужна
    return render(request, 'accounts/panel.html')


@login_required
def profile_view(request):
    # Дополнительная страница профиля если нужно
    return render(request, 'accounts/profile.html')