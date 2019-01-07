from django import forms

class ContactForm(forms.Form):
    firstname = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "First Name", 'id': 'firstname'}))
    lastname = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Last Name", 'id': 'lastname'}))
    phone = forms.RegexField(required=True,
        regex = r'010[1-9]\d{6,7}',
        help_text='휴대폰 번호를 입력해 주세요.',
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone', 'id': 'phonenumber'})
    )
    email = forms.EmailField(required=True,
        widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'id': 'email'})
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'}),
        help_text='Write here your message!'
    )
    source = forms.CharField(
        max_length=50,
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        firstname = cleaned_data.get('firstname')
        lastname = cleaned_data.get('lastname')
        phone = cleaned_data.get('phone')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not firstname and not lastname and not email and not phone and not message:
            raise forms.ValidationError('아래의 항목 모두 입력되어야 합니다.')
