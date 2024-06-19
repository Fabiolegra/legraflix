"""
tem que adiciona no settings do legratube no template > options
"""
from .models import Filme


def lista_filmes_recente(request):
    lista_filmes = Filme.objects.all().order_by('-data_criacao')[0:8]
    return {'lista_filmes_recente': lista_filmes}


def lista_filmes_alta(request):
    lista_filmes = Filme.objects.all().order_by('-visualizacoes')[0:8]
    return {'lista_filmes_alta': lista_filmes}


def filme_destaque(requets):
    if Filme.objects.order_by('-visualizacoes'):
        destaque = Filme.objects.order_by('-visualizacoes')[0]
    else:
        destaque = None
    return {'filme_destaque': destaque}
