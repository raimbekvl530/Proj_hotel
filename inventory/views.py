from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def sklad(request):
    return render(request, "sklad.html")

def suppliers(request):
    return render(request, "suppliers.html")

def supply(request):
    return render(request, "supply.html")
