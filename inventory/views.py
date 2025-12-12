# inventory/views.py
from django.shortcuts import render, redirect
from .models import Product, Supplier, Supply
from accounts.decorators import allowed_roles
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

@login_required
def index(request):
    # Получаем статистику для главной страницы
    total_products = Product.objects.count()
    low_stock_count = Product.objects.filter(quantity__lt=10).count()
    total_suppliers = Supplier.objects.count()
    
    return render(request, "index.html", {
        "total_products": total_products,
        "low_stock_count": low_stock_count,
        "total_suppliers": total_suppliers
    })

@login_required
@allowed_roles(['admin', 'manager', 'user'])
def sklad(request):
    products = Product.objects.all().order_by('name')
    recent_supplies = Supply.objects.all().order_by('-date')[:10]  # Последние 10 поставок
    
    low_stock = products.filter(quantity__lt=10)
    
    return render(request, "sklad.html", {
        "products": products,
        "recent_supplies": recent_supplies,
        "low_stock": low_stock,
        "low_threshold": 10
    })

@login_required
@allowed_roles(['admin', 'manager'])
def suppliers(request):
    suppliers = Supplier.objects.all().order_by('name')
    return render(request, "suppliers.html", {
        "suppliers": suppliers
    })

@login_required
@allowed_roles(['admin', 'manager'])
def supply(request):
    if request.method == "POST":
        try:
            product_id = request.POST.get("product")
            supplier_id = request.POST.get("supplier")
            qty = int(request.POST.get("quantity", 0))
            supply_date = request.POST.get("supply_date")
            
            if qty <= 0:
                messages.error(request, "Количество должно быть больше 0")
                return redirect('supply')
            
            product = Product.objects.get(id=product_id)
            supplier = Supplier.objects.get(id=supplier_id)

            # Создаём запись о поставке с указанием пользователя
            supply = Supply.objects.create(
                product=product,
                supplier=supplier,
                quantity=qty,
                created_by=request.user
            )
            
            # Устанавливаем дату из формы, если она есть
            if supply_date:
                try:
                    supply.date = datetime.strptime(supply_date, '%Y-%m-%dT%H:%M')
                    supply.save()
                except ValueError:
                    pass  # Оставляем текущую дату если ошибка

            # Обновляем количество на складе
            product.quantity += qty
            product.save()

            messages.success(request, f"Поставка {product.name} ({qty} ед.) успешно оформлена!")
            return redirect("supply")
            
        except (ValueError, Product.DoesNotExist, Supplier.DoesNotExist) as e:
            messages.error(request, f"Ошибка: {str(e)}")
            return redirect('supply')

    # GET запрос - показываем форму
    products = Product.objects.all().order_by('name')
    suppliers = Supplier.objects.all().order_by('name')
    
    # Получаем статистику
    today = timezone.now().date()
    today_supplies = Supply.objects.filter(date__date=today).count()
    recent_supplies = Supply.objects.all().order_by('-date')[:5]
    all_supplies = Supply.objects.all().order_by('-date')[:20]
    
    # Текущая дата и время для формы
    current_datetime = timezone.now().strftime('%Y-%m-%dT%H:%M')
    
    return render(request, "supply.html", {
        "products": products,
        "suppliers": suppliers,
        "today_supplies": today_supplies,
        "recent_supplies": recent_supplies,
        "all_supplies": all_supplies,
        "current_datetime": current_datetime
    })

@login_required
@allowed_roles(['admin', 'manager'])
def decrease_product(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            if product.quantity > 0:
                product.quantity -= 1
                product.save()
                messages.success(request, f"Списана 1 единица товара '{product.name}'. Остаток: {product.quantity}")
            else:
                messages.warning(request, f"Товар '{product.name}' отсутствует на складе")
        except Product.DoesNotExist:
            messages.error(request, "Товар не найден")
    
    return redirect('sklad')

@login_required
@allowed_roles(['admin', 'manager'])
def add_supplier(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            phone = request.POST.get("phone", "").strip()
            address = request.POST.get("address", "").strip()
            
            if not name:
                messages.error(request, "Название поставщика обязательно")
                return redirect('suppliers')
            
            # Проверяем, не существует ли уже поставщик с таким именем
            if Supplier.objects.filter(name=name).exists():
                messages.warning(request, f"Поставщик с именем '{name}' уже существует")
                return redirect('suppliers')
            
            Supplier.objects.create(
                name=name,
                phone=phone if phone else None,
                address=address if address else None
            )
            
            messages.success(request, f"Поставщик '{name}' успешно добавлен!")
            
        except Exception as e:
            messages.error(request, f"Ошибка при добавлении: {str(e)}")
    
    return redirect('suppliers')

@login_required
@allowed_roles(['admin', 'manager'])
def edit_supplier(request, supplier_id):
    if request.method == "POST":
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            supplier.name = request.POST.get("name")
            supplier.phone = request.POST.get("phone", "").strip()
            supplier.address = request.POST.get("address", "").strip()
            supplier.save()
            
            messages.success(request, f"Поставщик '{supplier.name}' обновлен!")
            
        except Supplier.DoesNotExist:
            messages.error(request, "Поставщик не найден")
        except Exception as e:
            messages.error(request, f"Ошибка при редактировании: {str(e)}")
    
    return redirect('suppliers')

@login_required
@allowed_roles(['admin', 'manager'])
def delete_supplier(request, supplier_id):
    if request.method == "POST":
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            supplier_name = supplier.name
            supplier.delete()
            
            messages.success(request, f"Поставщик '{supplier_name}' удален!")
            
        except Supplier.DoesNotExist:
            messages.error(request, "Поставщик не найден")
        except Exception as e:
            messages.error(request, f"Ошибка при удалении: {str(e)}")
    
    return redirect('suppliers')

@login_required
@allowed_roles(['admin', 'manager'])
def add_product(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            initial_quantity = int(request.POST.get("initial_quantity", 0))
            
            if not name:
                messages.error(request, "Название товара обязательно")
                return redirect('supply')
            
            # Проверяем, не существует ли уже товар с таким именем
            if Product.objects.filter(name=name).exists():
                messages.warning(request, f"Товар с именем '{name}' уже существует")
                return redirect('supply')
            
            Product.objects.create(
                name=name,
                quantity=initial_quantity
            )
            
            messages.success(request, f"Товар '{name}' успешно добавлен!")
            
        except Exception as e:
            messages.error(request, f"Ошибка: {str(e)}")
    
    return redirect('supply')