from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_view
from .views import (
    Homepage,
    Homefilme,
    Detalhefilme,
    Pesquisarfilmes,
    Editarperfil,
    Criaconta,
)

app_name = 'filme'
urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('filmes/', Homefilme.as_view(), name='homefilme'),
    path('filmes/<int:pk>', Detalhefilme.as_view(), name='detalhesfilmes'),
    path('pesquisa/', Pesquisarfilmes.as_view(), name='pesquisarfilme'),
    path('criaconta/', Criaconta.as_view(), name='criaconta'),
    path(
        'login/',
        auth_view.LoginView.as_view(template_name='login.html'),
        name='login',
    ),
    path(
        'logout_/',
        auth_view.LogoutView.as_view(template_name='logout.html'),
        name='logout',
    ),
    path(
        'editarperfil/<int:pk>',
        Editarperfil.as_view(template_name='editar_perfil.html'),
        name='editar_perfil',
    ),
    path(
        'alterasenha/',
        auth_view.PasswordChangeView.as_view(
            template_name='editar_perfil.html',
            success_url=reverse_lazy('homefilmes'),
        ),
        name='alterasenha',
    ),
]
