from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponseServerError
from aste.models import Puntata
from .forms import *

def main_page(request):
    return render(request, 'index.html')

@login_required
def login(request):
    """
    If users are authenticated, direct them to the main page. Otherwise,
    take them to the login page.
    """
    return render(request, 'index.html', { 'request':request } )

def logout_view(request):
    "Log users out and re-direct them to the main page."
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
            else:
                return HttpResponseServerError('user not valid')
            return HttpResponseRedirect('/login')
        else:
	        return HttpResponseServerError('form not valid')
    elif request.method == 'GET':
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

@login_required
def storico_utente(request):
    bids_list = Puntata.objects.filter(utente=request.user.id)
    return render(request, 'storico.html', { 'bids_list' : bids_list })
