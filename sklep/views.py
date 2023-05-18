from collections import namedtuple
from django.utils import timezone

import psycopg2
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from .models import *
from .forms import RegistrationForm
from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt


def store(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sklep_product")
    columns = [column[0] for column in cursor.description]
    Row = namedtuple('Row', columns)
    products = [Row(*row) for row in cursor.fetchall()]
    context = {'products':products}
    return render(request, 'sklep/store.html', context)


def cart(request):

    if request.user.is_authenticated:
        customer=request.user.customer
        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT *
                    FROM sklep_salesorder 
                    WHERE email_id = %s
                """, [customer.email])
            columns = [column[0] for column in cursor.description]
            Row = namedtuple('Row', columns)
            orders = [Row(*row) for row in cursor.fetchall()]

            sale_order_ids = [order.sale_order_id for order in orders]

            with connection.cursor() as cursor:
                cursor.execute("""
                        SELECT *
                        FROM sklep_salesorderline
                        WHERE sale_order_id_id IN %s
                    """,[tuple(sale_order_ids)])
                columns = [column[0] for column in cursor.description]
                Row = namedtuple('Row', columns)
                items = [Row(*row) for row in cursor.fetchall()]
    else:
        items= []
    context = {'items': items}
    return render(request, 'sklep/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'sklep/checkout.html', context)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        with connection.cursor() as cursor:
            #cursor.execute("SELECT * FROM auth_user WHERE username = %s", [username])
            cursor.execute(
                "SELECT * FROM sklep_customer WHERE user_id = (SELECT id FROM auth_user WHERE username = %s)", [username])
            user_row = cursor.fetchone()

            if user_row is not None:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('store')  # Przekierowanie na stronę po zalogowaniu

        error_message = 'Nieprawidłowa nazwa użytkownika lub hasło.'
        return render(request, 'sklep/login.html', {'error_message': error_message})
    else:
        return render(request, 'sklep/login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            error_message = 'Hasła nie pasują do siebie.'
            return render(request, 'sklep/register.html', {'error_message': error_message})

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        user_id = user.id

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO sklep_customer (user_id, email, first_name, last_name, address) "
                "VALUES (%s, %s, %s, %s, %s)",
                [user_id, email, first_name, last_name, address]
            )

        # Tworzenie nowego użytkownika
        user = authenticate(request, username=email, password=password)
        login(request, user)
        return redirect('store')  # Przekierowanie na stronę po rejestracji
    else:
        return render(request, 'sklep/register.html')











def index(request):
    return HttpResponse("Hello, world. You're at the first page.")
# Create your views here.

def home_view(request):
    # Przykładowe zapytanie SQL do pobrania produktów z bazy danych
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sklep_product")
        products = cursor.fetchall()

    # Przekazanie danych do szablonu
    return render(request, 'home.html', {'products': products})

def product_view(request, product_id):
    # Pobierz dane produktu z bazy danych na podstawie product_id
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM sklep_product WHERE "product_ID"= %s', [product_id])
    columns = [column[0] for column in cursor.description]
    Row = namedtuple('Row', columns)
    product = Row(*cursor.fetchone())

    return render(request, 'product.html', {'product': product})

def registration_viewSQL(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            password = make_password(data['password'])
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO sklep_customer (email, password, first_name, last_name, address) VALUES (%s, %s, %s, %s, %s)', [data['email'], password, data['first_name'], data['last_name'], data['address']])
            return render(request, 'registration_success.html')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def product_info_sql(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sklep_product")
        columns = [column[0] for column in cursor.description]
        Row = namedtuple('Row', columns)
        products = [Row(*row) for row in cursor.fetchall()]
    return render(request, 'product_info.html', {'products': products})