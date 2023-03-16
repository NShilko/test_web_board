from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, View
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.core.mail import send_mail
import secrets
from publication.models import Profile

from .forms import CustomUserCreationForm, ValidationEmailForm


class SignUpView(View):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('account_activation_sent')
    template_name = 'sign/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            User = form.save(request, commit=False)
            User.is_active = False
            User.username = form.cleaned_data['username']
            User.email = form.cleaned_data['email']
            User.set_password(form.cleaned_data['password1'])
            User.save()
            confirmation_code = secrets.token_urlsafe(6)
            Profile.objects.create(user_id=User.pk, confirmation_code=confirmation_code)
            subject = 'Подтверждение адреса электронной почты'
            html_message = render_to_string('sign/acc_activate_email.html', {
                'user': User,
                'confirmation_code': confirmation_code,
                'link': User.pk,
            })
            plain_message = strip_tags(html_message)
            from_email = 'help@psymphony.ru'
            to_email = form.data['email']
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
            return redirect('confirm_email', user_id=User.pk)
        return render(request, self.template_name, {'form': form})


class ConfirmEmailView(CreateView):
    form_class = ValidationEmailForm
    model = User
    template_name = 'sign/account_activation_sent.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author_id = self.request.user.id
        self.object.save()
        return super().form_valid(form)


def ConfirmEmailView(request, user_id):
    code = Profile.objects.get(user_id=user_id)
    if request.method == 'POST':
        form = ValidationEmailForm(request.POST)
        if form.is_valid():
            if code.confirmation_code == form.data['confirmation_code']:
                cur_user = User.objects.get(pk=user_id)
                cur_user.is_active = True
                basic_group = Group.objects.get(name='common')
                user = User.objects.get(pk=user_id)
                basic_group.user_set.add(user)
                cur_user.save()
                return redirect('code_correct')
            else:
                return redirect('code_invalid')
    else:
        form = ValidationEmailForm()
    return render(request, 'sign/account_activation_sent.html', {'form': form})


def CodeCorrect(request):
    return render(request, 'sign/account_activation_correct.html')


def CodeInvalid(request):
    return render(request, 'sign/account_activation_invalid.html')
