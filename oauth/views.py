from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.

import requests
import json

from ccp.settings import CLIENT_ID, CLIENT_SECRET, REDIRECTION_URL
from .models import UserCodeChefAuth


def fetch_data(request, url):

    access_token = request.user.usercodechefauth.access_token
    headers_for_data = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    response_for_data = {}
    response_for_data = requests.get(url, headers = headers_for_data)

    if response_for_data.json()['status'] == 'error':
        # fetch new access_token
        refresh_token = request.user.usercodechefauth.refresh_token
        headers_for_access_token = {
            'content-Type': 'application/json',
        }
        data_for_access_token = '{"grant_type":"refresh_token" ,"refresh_token":"'+ refresh_token +'", "client_id":"'+ CLIENT_ID +'","client_secret":"'+ CLIENT_SECRET +'"}'
        response_for_access_token = requests.post('https://api.codechef.com/oauth/token', headers = headers_for_access_token, data = data_for_access_token)
        
        # save the new access_token and refresh_token received
        request.user.usercodechefauth.access_token = response_for_access_token.json()['result']['data']['access_data']
        request.user.usercodechefauth.refresh_token = response_for_access_token.json()['result']['data']['refresh_data']
        request.user.usercodechefauth.save()

        # try to fetch the data required again with the new access_token
        access_token = request.user.usercodechefauth.access_token
        headers_for_data = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }    
        response_for_data = requests.get(url, headers = headers_for_data)
        if response_for_data.json()['status'] == 'error':
            return HttpResponse('Error! Please try again later!')
    
    # return the fetched data in JSON format
    return response_for_data.json()


def success(request):

    authorisation_code = request.GET['code']
    headers = {
        'content-Type': 'application/json',
    }
    data = '{"grant_type": "authorization_code","code":"' + authorisation_code + '","client_id":"'+ CLIENT_ID +'","client_secret":"' + CLIENT_SECRET + '","redirect_uri":"' + REDIRECTION_URL + '/oauth/success"}'
    response = requests.post('https://api.codechef.com/oauth/token', headers = headers, data = data)
    print(response.json())
    response_data = response.json()['result']['data']
    access_token = response_data['access_token']

    # fetch the user's CodeChef username 
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get('https://api.codechef.com/users/me', headers = headers)
    data = response.json()['result']['data']['content']
    username = data['username']
    
    print(response_data)
    # store the username alongwith the access_token and refresh_token in the database
    try:
        user = User.objects.get(username = username)
        # user.usercodechefauth.extra_data = str(json.dumps(response_data))
        user.usercodechefauth.access_token = response_data['access_token']
        user.usercodechefauth.refresh_token = response_data['refresh_token']
        user.usercodechefauth.save()
    except User.DoesNotExist:
        user = User()
        user.username = username
        user.save()
        cuser = UserCodeChefAuth()
        cuser.user = user
        cuser.access_token = response_data['access_token']
        cuser.refresh_token = response_data['refresh_token']
        cuser.save()

    # authenticate and login the user and redirect to homepage ('/')    
    login(request, user)
    return redirect('/')

