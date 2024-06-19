"""Views do django."""
from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, reverse
from django.views.generic import ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import Criarcontaform, HomepageForm
from .models import Filme, Usuario

# Create your views here.
class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = HomepageForm

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('filme:homefilme')
        return super().get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        email = self.request.POST.get('email')
        usuario = Usuario.objects.filter(email=email)
        if usuario:
            return reverse('filme:login')
        return reverse('filme:criaconta')


class Homefilme(LoginRequiredMixin, ListView):
    template_name = 'homefilmes.html'
    model = Filme


class Detalhefilme(LoginRequiredMixin, DetailView):
    template_name = 'detalhesfilmes.html'
    model = Filme

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(Detalhefilme, self).get_context_data(**kwargs)
        filmes_relacionado = Filme.objects.filter(
            categoria=self.get_object().categoria
        )[0:4]
        context['filmes_relacionados'] = filmes_relacionado
        return context


class Pesquisarfilmes(LoginRequiredMixin, ListView):
    template_name = 'pesquisarfilmes.html'
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(
                titulo__icontains=termo_pesquisa
            )
            return object_list
        else:
            return None


class Editarperfil(LoginRequiredMixin, UpdateView):
    template_name = 'editar_perfil.html'
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self) -> str:
        return reverse('filme:homefilme')


class Criaconta(FormView):
    template_name = 'criaconta.html'
    form_class = Criarcontaform

    def form_valid(self, form: Any) -> HttpResponse:
        form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('filme:login')
