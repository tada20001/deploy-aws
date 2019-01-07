from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    is_artist = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)


class Category(models.Model):
    name = models.SlugField(max_length=100, allow_unicode=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'is_artist': True})
    main_fields = models.ManyToManyField(Category, related_name='fields_artists')

    def __str__(self):
        return '[{}] <{}> {}'.format(self.user_id, self.user, self.user.profile.name)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    interests = models.ManyToManyField(Category, related_name='interested_clients', help_text='관심분야를 선택해 주세요.')

    def __str__(self):
        return '[{}] <{}> {}'.format(self.user_id, self.user, self.user.profile.name)


class Profile(models.Model):
    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r, r))

    user = models.OneToOneField(User, on_delete=models.CASCADE) ### 중요!!!!
    name = models.CharField(max_length=100)
    location = models.CharField(_('활동지'), max_length=100, blank=True, null=True)
    education = models.CharField(_('교육'), max_length=100, blank=True, null=True)
    birthYear = models.IntegerField(_('BirthYear'), choices=YEAR_CHOICES, default=datetime.datetime.now().year, blank=True, null=True)
    bio = models.TextField(_('소개'), blank=True, null=True)
    singleEvent = models.TextField(_('개인전'), blank=True, null=True)
    GroupEvent = models.TextField(_('그룹전'), blank=True, null=True)
    website_url = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='profiles/', blank=True)

    def __str__(self):
        return self.name


def on_post_save_for_user(sender, **kwargs):
    if kwargs['created']:
        # 가입시기
        user = kwargs['instance']
        Profile.objects.create(user=user)

        # 환영 이메일 보내기(django-celery-email을 사용하면 이메일 비동기로 빨리 보낼 수 있음, 혹은 yagmail 사용(편리함))
        send_mail(
            '환영합니다.',
            'Here is the messages.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

post_save.connect(on_post_save_for_user, sender=settings.AUTH_USER_MODEL)

# 로그인 중복 막기
class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    session_key = models.CharField(max_length=40, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

def kicked_my_other_sessions(sender, request, user, **kwargs):
    print('kicked my other sessions')
    user.is_user_logged_in = True # 이 객체가 accounts/middleware.py의 KickMiddleware에 그대로 전달

user_logged_in.connect(kicked_my_other_sessions)
