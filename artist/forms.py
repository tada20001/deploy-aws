from django import forms
from .models import Work
from accounts.models import Category


class WorkForm(forms.ModelForm):

    class Meta:
        model = Work
        fields = ('title', 'video', 'description', 'tags', 'category', 'image1', 'image2', 'image3', 'image4', 'image5')
        help_texts = {
            'title': '3 글자이상 입력해 주세요.',
            'video': '링크 주소를 입력 해주세요.',
            'category': '위의 항목 중 하나만 선택해 주세요.',
        }
        widgets = {
            'description': forms.Textarea(),
            'category': forms.CheckboxSelectMultiple()
        }
