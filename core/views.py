from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse

# Create your views here.
# def index(request):
#   return redirect('/agenda')
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('senha')
        usuario = authenticate(username = username, password = password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "USUÁRIO OU SENHA INVÁLIDO")
    return redirect('/')

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now()  - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__gt=data_atual)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            Evento.objects.filter(id=id_evento).update(titulo=titulo,
                                                        data_evento= data_evento,
                                                        descricao= descricao,
                                                        usuario=usuario)
        else:
            Evento.objects.create(titulo=titulo,
                                data_evento= data_evento,
                                descricao= descricao,
                                usuario=usuario)
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

@login_required(login_url='/login/')
def json_lista_evento(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(evento), safe=False)