# accounts/decorators.py
from django.shortcuts import redirect
from django.contrib import messages

def allowed_roles(roles=[]):
    """
    Декоратор для проверки ролей пользователя
    Пример использования: @allowed_roles(['admin', 'manager'])
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            if not request.user.is_authenticated:
                messages.error(request, "Требуется авторизация")
                return redirect('login')
            
            # Суперпользователь имеет доступ ко всему
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Проверяем группы пользователя
            user_groups = set(request.user.groups.values_list('name', flat=True))
            allowed_set = set(roles)
            
            if user_groups.intersection(allowed_set):
                return view_func(request, *args, **kwargs)
            
            messages.error(request, f"У вас нет прав для доступа к этой странице. Требуются роли: {', '.join(roles)}")
            return redirect('index')
            
        return wrapper_func
    return decorator

# Сохраняем старые декораторы для обратной совместимости
def admin_required(view_func):
    return allowed_roles(['admin'])(view_func)

def manager_required(view_func):
    return allowed_roles(['admin', 'manager'])(view_func)

def user_required(view_func):
    return allowed_roles(['admin', 'manager', 'user'])(view_func)