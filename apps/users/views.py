import logging

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from apps.users.forms import ProfileForm, RegisterForm, UserUpdateForm
from apps.users.models import UserProfile
from apps.users.tokens import email_verification_token


logger = logging.getLogger(__name__)


ATTEMPT_LIMIT = 5
ATTEMPT_TTL = 600


def _attempt_key(request: HttpRequest) -> str:
    ip = request.META.get('REMOTE_ADDR', 'unknown')
    return f"login-attempts:{ip}"


def _send_verification_email(request: HttpRequest, user) -> bool:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    verify_url = request.build_absolute_uri(
        reverse('users:verify_email', kwargs={'uidb64': uid, 'token': token})
    )
    subject = _('Подтверждение email')
    message = render_to_string(
        'emails/verify_email.txt',
        {'user': user, 'verify_url': verify_url},
        request=request,
    )
    try:
        send_mail(subject, message, None, [user.email])
    except Exception:
        logger.exception('Failed to send verification email for user=%s', user.pk)
        return False
    return True


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            if _send_verification_email(request, user):
                messages.success(request, _('Проверьте почту и подтвердите регистрацию.'))
            else:
                messages.error(request, _('Не удалось отправить письмо подтверждения. Попробуйте позже.'))
            return redirect('users:login')
        messages.error(request, _('Исправьте ошибки формы.'))
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    key = _attempt_key(request)
    attempts = cache.get(key, 0)
    next_url = request.GET.get('next') or request.POST.get('next')
    if attempts >= ATTEMPT_LIMIT:
        messages.error(request, _('Слишком много попыток входа. Попробуйте позже.'))
        return render(request, 'users/login.html', {'form': AuthenticationForm(request), 'next': next_url})

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            cache.delete(key)
            return redirect(next_url or 'pages:home')
        username = request.POST.get('username', '')
        if username:
            User = get_user_model()
            if User.objects.filter(username=username, is_active=False).exists():
                messages.error(request, _('Почта не подтверждена. Проверьте письмо.'))
                return render(request, 'users/login.html', {'form': form, 'next': next_url})
        cache.set(key, attempts + 1, ATTEMPT_TTL)
        messages.error(request, _('Неверный логин или пароль.'))
    else:
        form = AuthenticationForm(request)
    return render(request, 'users/login.html', {'form': form, 'next': next_url})


@login_required
def logout_view(request):
    logout(request)
    return redirect('pages:home')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Профиль обновлён.'))
            return redirect('users:profile')
        messages.error(request, _('Исправьте ошибки формы.'))
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(
        request,
        'users/profile.html',
        {'user_form': user_form, 'profile_form': profile_form, 'profile': profile},
    )


def verify_email(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and email_verification_token.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=['is_active'])
        messages.success(request, _('Email подтверждён. Теперь вы можете войти.'))
        return redirect('users:login')

    messages.error(request, _('Ссылка подтверждения недействительна или устарела.'))
    return redirect('users:login')
