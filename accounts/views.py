from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import artist_required, client_required, staff_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from django.contrib.auth.views import PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from django.utils.http import urlsafe_base64_decode

from django.contrib import messages
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from .models import User, Profile, Artist, Client
from .forms import ArtistSignupForm, ClientSignupForm, ArtistProfileForm, ClientProfileForm
from artist.models import Work



class SignupView(TemplateView):
    template_name = 'accounts/signup.html'


class ArtistSignupView(CreateView):
    model = User
    form_class = ArtistSignupForm
    template_name = 'accounts/signup_form.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next') or 'profile_edit_artist'
        return resolve_url(next_url)

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Artist'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        # 회원가입과 동시에 로그인
        auth_login(self.request, user)
        messages.info(self.request, 'my page 내용을 모두 작성해 주시기 바랍니다.')
        return redirect(self.get_success_url())

class ClientSignupView(CreateView):
    model = User
    form_class = ClientSignupForm
    template_name = 'accounts/signup_client_form.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next') or 'profile_edit_client'
        return resolve_url(next_url)

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = '일반회원'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        # 회원가입과 동시에 로그인
        auth_login(self.request, user)
        return redirect(self.get_success_url())

@login_required
def profile(request):
    user = request.user
    works = Work.objects.all()
    last_work = None

    if user.is_artist:
        artist = get_object_or_404(Artist, user=user)
        works = Work.objects.filter(artist=artist)
        if works:
            last_work = works.order_by('-created_at')[0]
        template_name = 'accounts/artist_profile.html'
    else:
        user = user
        template_name = 'accounts/client_profile.html'

    return render(request, template_name, {'user': user, 'works': works, 'last_work': last_work, })


class ProfileUpdateView(UpdateView, LoginRequiredMixin):
    model = Profile
    def get_form_class(self):
        if self.request.user.is_artist:
            form_class = ArtistProfileForm
        else:
            form_class = ClientProfileForm
        return form_class
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        messages.info(self.request, '내용이 수정되었습니다.')
        form.save()
        return super().form_valid(form)

profile_edit = ProfileUpdateView.as_view(template_name='accounts/profile_client_form.html')
profile_edit_client = ProfileUpdateView.as_view(template_name='accounts/profile_client_form.html')
profile_edit_artist = ProfileUpdateView.as_view()


class RequestLoginViaUrlView(PasswordResetView):
    template_name = 'accounts/request_login_via_url_form.html'
    title = '이메일 인증을 통한 로그인'
    email_template_name = 'accounts/login_via_url.html'
    success_url = settings.LOGIN_URL

    def form_valid(self, form):
        if form.cleaned_data['email'] in [i.email for i in User.objects.all()]:
            messages.info(self.request, '로그인 링크 주소를 메일로 보내드렸습니다.')
        else:
            messages.info(self.request, '등록되지 않은 이메일입니다.')
        return super().form_valid(form)

def login_via_url(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        raise Http404

    if default_token_generator.check_token(current_user, token):
        auth_login(request, current_user) # 로그인 처리
        messages.info(request, '로그인이 승인되었습니다.')
        return redirect('home')

    messages.error(request, '로그인이 거부되었습니다.')
    return redirect('home')


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.info(self.request, '비밀번호가 변경되었습니다.')
        return super().form_valid(form)

class MyPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        if form.cleaned_data['email'] in [i.email for i in User.objects.all()]:
            messages.info(self.request, '비밀번호 변경 메일을 발송했습니다.')
        else:
            messages.info(self.request, '등록되지 않은 이메일입니다.')
        return super().form_valid(form)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.info(self.request, '비밀번호 재설정을 완료했습니다.')
        return super().form_valid(form)
