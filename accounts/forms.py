from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from django.db import transaction

from django import forms
from .models import User, Category, Client, Artist, Profile


class ArtistSignupForm(UserCreationForm):
    #name = forms.CharField(max_length=20, required=True)
    # 이메일 로그인을 위한 폼 정의
    main_fields = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].validators = [validate_email]
        self.fields['username'].help_text = _('이메일을 입력해 주세요.')
        self.fields['username'].label = _('Email')
        self.fields['main_fields'].label = '주요 분야'
        self.fields['main_fields'].help_text = '주로 활동하시는 분야를 선택해주세요.(복수선택 가능)'

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_artist = True
        user.email = user.username
        user.save()
        artist = Artist.objects.create(user=user)
        artist.main_fields.add(*self.cleaned_data.get('main_fields'))
        return user

    class Meta(UserCreationForm.Meta):
        model = User


class ClientSignupForm(UserCreationForm):
    # 이메일 로그인을 위한 폼 정의
    interests = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].validators = [validate_email]
        self.fields['username'].help_text = _('Enter Email Format.')
        self.fields['username'].label = _('Email')
        self.fields['interests'].label = '관심분야'
        self.fields['interests'].help_text = '(복수선택 가능)'


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.email = user.username
        user.save()
        client = Client.objects.create(user=user)
        client.interests.add(*self.cleaned_data.get('interests'))
        return user

    class Meta(UserCreationForm.Meta):
        model = User


class ArtistProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('name', 'location', 'education', 'birthYear', 'bio', 'singleEvent', 'GroupEvent', 'website_url', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].help_text = '이름을 반드시 입력해 주세요.'


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].help_text = '이름을 반드시 입력해 주세요.'


class MyAuthenticationForm(AuthenticationForm):
    class Meta:
        fields = ('email')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].validators = [validate_email]
        self.fields['username'].help_text = _('Enter Email Format.')
        self.fields['username'].label = _('Email')
