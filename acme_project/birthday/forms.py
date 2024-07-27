# birthday/forms.py
from django import forms

from .models import Birthday

from django.core.exceptions import ValidationError
from django.core.mail import send_mail

# Множество с именами участников Ливерпульской четвёрки.
BEATLES = {"Джон Леннон", "Пол Маккартни", "Джордж Харрисон", "Ринго Старр"}


class BirthdayForm(forms.ModelForm):
    class Meta:
        model = Birthday
        fields = ("first_name", "last_name", "birthday", "image")
        widgets = {"birthday": forms.DateInput(attrs={"type": "date"})}

    def clean_first_name(self):
        # Получаем значение имени из словаря очищенных данных.
        first_name = self.cleaned_data["first_name"]
        # Разбиваем полученную строку по пробелам
        # и возвращаем только первое имя.
        return first_name.split()[0]

    def clean(self):
        super().clean()
        # Получаем имя и фамилию из очищенных полей формы.
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        # Проверяем вхождение сочетания имени и фамилии во множество имён.
        if f"{first_name} {last_name}" in BEATLES:
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                "Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!"
            )
