import pandas as pd
import requests
import json
import string
import random

from django.http import HttpResponse
from django.http import JsonResponse
from faker import Faker

from test_project.response import JsonUnicodeResponse
from . import tools as t


def index(request):
    return HttpResponse("Hello, world!! Select: <br>1. <a href='http://127.0.0.1:5000/get_profile'>Get profile</a><br>" +
                        "2. <a href='http://127.0.0.1:5000/get_libs'>Get libs</a><br>" +
                        "3. <a href='http://127.0.0.1:5000/get_avg_wh'>Get average height and weight</a>")


def get_profile(request):
    """Get name and mail from profile"""

    fake = Faker(['it_IT', 'en_US', 'uk_UA'])

    profile_list = [fake.profile(fields=['name', 'mail']) for _ in range(100)]
    return JsonUnicodeResponse({"profiles": profile_list})


def get_lib(request):
    """Get libraries in requirements.txt"""

    libs_list = [line.strip() for line in open('requirements.txt', 'r')]
    return JsonResponse({"libs": libs_list})


def get_avg_wh(request):

    """Get student's average height and weight """

    hw_df = pd.read_csv('datasets/hw.csv', delimiter=',')
    hw_df.columns = ['index', 'height', 'weight']

    avg_height = int(round(hw_df["height"].mean()))
    avg_weight = int(round(hw_df["weight"].mean()))
    return JsonResponse({"average": {"height": avg_height,
                                          "weight": avg_weight
                                          }})


def get_astronauts(request):

    """Get astronauts"""

    response = requests.get("http://api.open-notify.org/astros.json")
    if response.status_code == 200:
        resp = json.loads(response.text)
        return HttpResponse(f"Astronauts number: {resp['number']}")
    else:
        return HttpResponse(f"Error {response.status_code}")


def get_password(request):

    """

    Password generator that getting two GET parameters: length(length of password)
    and isdigit(bool param that indicate if number exists in password or not).
    Length and isdigit must be numeric and greater than zero.
    Length ranges from 8 to 24.

    Example: length=24&isdigit=0

    """

    length = request.GET.get('length')
    isdigit = request.GET.get('isdigit')

    if length is not None and isdigit is not None:
        is_len_digit = length.isdigit()
        is_dig_digit = isdigit.isdigit()

        if is_dig_digit and is_len_digit:
            length = int(length)
            isdigit = int(isdigit)
            if isdigit not in range(0, 2):
                return HttpResponse('Value isdigit must be 0 or 1')
            if length in range(8, 25):
                generation_symbols = string.ascii_lowercase
                if isdigit == 1:
                    generation_symbols += string.digits
                elif isdigit == 0:
                    generation_symbols = generation_symbols
                return HttpResponse(''.join([random.choice(generation_symbols) for _ in range(length)]))
            else:
                return HttpResponse('Password must be between 0 to 24')
        else:
            return HttpResponse('Error. The value must be numeric and greater than zero.')
    return HttpResponse("Put two GET param: length and isdigit")


def get_customers(request):

    """

    Get customers who live in a given state and city.
    City and state given in two GET param: state and city.

    Example: city=New%20York&state=NY

    """

    city = request.GET.get('city')
    state = request.GET.get('state')
    if city is not None and state is not None:

        query = "SELECT FirstName, LastName, Email, Phone FROM customers WHERE City = ? AND State = ?"
        customers = t.execute_query(query, (city, state))
        customers = '<br>'.join([str(customer) for customer in customers])
        return HttpResponse(customers)
    return HttpResponse("Put two GET param: city and state ")


def get_customers_number(request):

    """Get number of customers"""

    query = "SELECT DISTINCT count(FirstName) FROM customers"
    customers_number = t.execute_query(query)
    customers_number = f'<br>The number of customers: {customers_number[0][0]}'
    return HttpResponse(customers_number)


def get_company_rev(request):

    """Get company rev"""

    query = "SELECT SUM(UnitPrice*Quantity) AS 'rev' FROM invoice_items"
    rev = t.execute_query(query)
    rev = f'<br>The company rev: {rev[0][0]}'
    return HttpResponse(rev)


def get_invoices(request):

    """

    Get invoices that received in a given city and country.
    Сity and country given in two GET param: city and country.

    Example: city=Oslo&country=Norway

    """

    city = request.GET.get('city')
    country = request.GET.get('country')
    if city is not None and country is not None:

        query = "SELECT InvoiceDate, BillingAddress, BillingCity, BillingState, BillingCountry, BillingPostalCode, " \
                "Total FROM invoices WHERE BillingCity=? AND BillingCountry=? "
        invoices = t.execute_query(query, (city, country))
        return JsonResponse({"invoices": invoices})
    return HttpResponse("Put two GET param: city and country ")



