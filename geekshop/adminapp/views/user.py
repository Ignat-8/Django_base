from django.shortcuts import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from authapp.models import ShopUser


def check_is_superuser(user):
    if not user.is_superuser:
        raise PermissionDenied
    else:
        return True


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    
    @method_decorator(user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/создание'
        return context


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        return context


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    def form_valid(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:  # сначала меняем статус
            self.object.is_active = False
            self.object.save()
        else:
            self.object.delete()  # во второй раз удаляем
        return HttpResponseRedirect(self.get_success_url())
