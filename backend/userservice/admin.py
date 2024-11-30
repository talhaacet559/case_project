from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import AbstractUser
from django.forms import forms

from .models import Izin, Calisan

class CalisanChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Calisan


class CalisanCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Calisan

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            Calisan.objects.get(username=username)
        except Calisan.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

class CalisanAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(CalisanAdmin, self).__init__(*args, **kwargs)

        abstract_fields = [field.name for field in AbstractUser._meta.fields]
        user_fields = [field.name for field in self.model._meta.fields]

        self.fieldsets += (
            ('Extra fields', {
                'fields': [
                    f for f in user_fields if (
                            f not in abstract_fields and
                            f != self.model._meta.pk.name
                    )
                ],
            }),
        )
    model=Calisan
    list_display = ("username","izin_hakki", "kullanilan_izin")


admin.site.register(Calisan, CalisanAdmin)

@admin.register(Izin)
class IzinAdmin(admin.ModelAdmin):
    pass
