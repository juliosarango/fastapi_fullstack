import requests
from app.core.config import settings

headers_token = {
    'Authorization': f"Basic {settings.API_AUTHORIZATION}",
}    

def generate_token():
    data = {
        "grant_type": "password",
        "username": settings.API_AUTHORIZATION_USERNAME,
        "password": settings.API_AUTHORIZATION_PASSWORD
    }
        
    response = requests.post(settings.API_URL_TOKENS, headers=headers_token, data=data).json()
    if response.get('refresh_token'):
        return response['refresh_token']
    else:
        raise Exception(response)


def refresh_token(refresh_token):     
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token        
    }
    response = requests.post(settings.API_URL_TOKENS, headers=headers_token, data=data).json()
    if response.get('access_token'):
        return response['access_token']
    else:
        raise Exception(response)
    
def obtener_access_token():
    _refresh_token = generate_token()
    access_token = refresh_token(_refresh_token)
    return access_token


    
def obtener_cotizaciones(data):
    
    access_token = obtener_access_token()
    headers = {
        'Authorization': f"Bearer {access_token}",
    }
        
    response = requests.post(settings.API_URL_COTIZACIONES, headers=headers, json=data).json()    
    if response.get('responseBody'):
        return response['responseBody']
    else:
        raise Exception(response)
    
    
def generar_emisiones(data):
    access_token = obtener_access_token()
        
    headers = {
        'Authorization': f"Bearer {access_token}",
    }
        
    response = requests.post(settings.API_URL_EMISIONES, headers=headers, json=data).json()    
    
    if response:
        return response
    else:
        raise Exception(response)
    

def obtener_emision(id):
    access_token = obtener_access_token()

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    response = requests.get(f"{settings.API_URL_EMISIONES}/{id}", headers=headers).json()

    if response:
        return response
    else:
        raise Exception(response)