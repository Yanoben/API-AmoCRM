import requests
import os
from dotenv import load_dotenv
from django.shortcuts import render


load_dotenv()

SECRET__KEY = os.environ.get('SECRET__KEY')
ID = os.environ.get('ID')


subdomain = 'yasinabdurakhmanov'
redirect_url = "http://ab19-88-245-198-194.ngrok.io"


def get_auth_code():
    '''GET Authorization Code from Redirect URL'''
    url = f'https://www.amocrm.ru/oauth?response_type=code&client_id={ID}&redirect_uri={redirect_url}&state=state&mode=popup'
    r = requests.get(url)
    try:
        r = requests.head(url, allow_redirects=True)
        return r.url.get('csrf_token')
    except AttributeError:
        print("An exception occurred")


def get_access_token():
    '''GET access_token with auth_code'''
    data = {
            "client_id": ID,
            "client_secret": SECRET__KEY,
            "grant_type": "authorization_code",
            "code": get_auth_code(),
            "redirect_uri": redirect_url
        }
    url = f'https://{subdomain}.amocrm.ru/oauth2/access_token'
    result = requests.post(url, data=data)
    return result.json()


result = get_access_token()
access_token = result.get('access_token')
refresh_token = result.get('refresh_token')
expires_in = result.get('expires_in')
headers = {'Authorization': f'Bearer {access_token}'}

try:
    if expires_in > 0:
        url = f'https://{subdomain}.amocrm.ru/api/v4/contacts'
        response = requests.get(
            url,
            headers={'Authorization': f'Bearer {access_token}'})
    else:
        url = f'https://{subdomain}.amocrm.ru/oauth2/access_token'
        data = {
            "client_id": ID,
            "client_secret": SECRET__KEY,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "redirect_uri": redirect_url
        }
        response = requests.post(url, data=data)
        access_token = response.get('access_token')
        refresh_token = response.get('refresh_token')
        token_type = response.get('token_type')
        expires_in = response.get('expires_in')
except TypeError:
    print('ERROr')


def index(request):
    return render(request, 'index.html')


def form(request):
    '''Get values in template form'''
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        data = {
            'name': name,
            'email': email,
            'phone': phone
        }
        return data


def get_contact_id(data):
    '''Get Contact method(with email or phone)'''
    data = form()
    url = f'https://{subdomain}.amocrm.ru/api/v4/contacts'
    payload = {'key1': data.get('email'), 'key2': data.get('phone')}
    response = requests.get(url, params=payload, headers=headers).json()
    if response:
        id = response.get('id')
        url = f'https://{subdomain}.amocrm.ru/api/v4/contacts/{id}'
        response = requests.patch(url, data=data, headers=headers)
    else:
        response = requests.post(url, data=data, headers=headers)
    url = f'https://{subdomain}.amocrm.ru/api/v4/leads'
    response = requests.post(url, data=data, headers=headers)
