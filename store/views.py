from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django import forms


def category(request, foo):
    # replacing the space in the category name from this 'cell phone' to cell-phone
    foo = foo.replace('-', '')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})

    except Category.DoesNotExist:
        messages.error(request, "This Category does't exist...")
        return redirect('home')


@login_required
def home(request):
    user = request.user
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products, 'user': user})


# biew product individualy
@login_required
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def about(request):
    return render(request, 'about.html', {})


# login User registration
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You Have seccusfuly logged In')

            return redirect('home')
        else:
            messages.error(request, 'There was an error please try again')
            return redirect('login')
    else:
        return render(request, 'login.html', {})

# logout user


def logout_user(request):
    logout(request)
    messages.success(request, 'You are logged Out')
    return redirect('login')

# User registration


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in the new user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, 'There was a problem registering. Please check your input.')
            return redirect('home')
        else:
            messages.error(
                request, 'There was a problem registering. Please check your input.')
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
