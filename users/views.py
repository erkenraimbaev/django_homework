
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from users.utils import generate_password


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if self.form_valid:
            new_user = form.save()
            code = new_user.email_confirm_key
            send_mail(
                subject='Успешная регистрация!',
                message=f'Вы зарегистрированы! Ваш код для подтверждения: {code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]
            )
            new_user.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def confirm_email(request):
    if request.method == 'POST':
        verif_code = request.POST.get('email_confirm_key')
        user = User.objects.get(email_confirm_key=verif_code)

        if user.email_confirm_key == verif_code:
            user.email_is_confirmed = True
            user.is_authenticated = True
            user.save()
            return redirect(reverse('users:login'))
    else:
        return render(request, 'users/verification_form.html')


def generate_new_password(request):
    new_password = generate_password()
    send_mail(
        subject='Вы сменили пароль!',
        message=f'Вaш новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:home'))
