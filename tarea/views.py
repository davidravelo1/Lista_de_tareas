from typing import Any
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy 
from .models import Tarea

class Logueo(LoginView):
    template_name= 'tarea/login.html'
    field = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('pendientes')

class listapendientes(LoginRequiredMixin, ListView):
    model = Tarea
    context_object_name= 'lista_tareas'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tareas'] = context['tareas'].filter(usuario=self.request.user)
        context['count'] = context['tareas'].filter(completo=False).count()
        return context
    
class DetalleTarea(LoginRequiredMixin, DetailView):
    model = Tarea
    context_object_name= 'tarea'

class CrearTarea(LoginRequiredMixin, CreateView):
    model = Tarea
    fields = ['titulo', 'descripcion', 'completo']
    success_url=reverse_lazy('pendientes')

    def val_form(self, form):
        form.instance.usuario = self.request.user
        return super(CrearTarea, self).form_valid(form)

class EditarTarea(LoginRequiredMixin, UpdateView):
    model = Tarea
    fields = ['titulo', 'descripcion', 'completo']
    success_url=reverse_lazy('pendientes')

class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    context_object_name= 'tarea'
    success_url = reverse_lazy('pendientes')
