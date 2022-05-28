from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from dashboard.awscontroller import AWSController


mcServer = AWSController()


def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            return render(request,"failed.html")
    return render(request,"login.html")

@login_required
def index(request):
    if request.user.is_authenticated:
        context = {
            'user' : request.user.username,
            'estado': mcServer.getState(),
            'statuscode': mcServer.getStatusCode
        }
        return render(request,"dashboard.html",context)
    else:
        return redirect('/login')

@login_required
def encender(request):
    if request.user.is_authenticated and request.method == 'POST':
        mcServer.instance.start()
        return redirect('encendido')
    else:
        return redirect('logout')

@login_required
def apagar(request):
    if request.user.is_authenticated and request.method == 'POST':
        mcServer.instance.stop()
        return redirect('apagado')
    else:
        return redirect('logout')

@login_required
def apagado(request):
    return render(request,'apagado.html')

@login_required
def encendido(request):
    return render(request,'encendido.html')

def logoutpage(request):
    logout(request)
    return redirect('index')