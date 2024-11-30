from email.policy import default

from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Izin


class IzinForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.pop("initial", {})
        super(IzinForm, self).__init__(*args, **kwargs)

        # Set the initial value for the "calisan" field
        self.fields["calisan"].initial = initial.get("calisan")

        # Optionally set the value in the instance for use in clean()
        if self.instance:
            self.instance.calisan = initial.get("calisan")
        self.fields["calisan"].required = False

    class Meta:
        model = Izin
        fields = ['izin_baslangic', 'izin_bitis', 'gerekce', 'zaruri',"calisan"]
        widgets = {
            'izin_baslangic': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'izin_bitis': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gerekce': forms.TextInput(attrs={'class': 'form-control'}),
            'zaruri': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "calisan": forms.HiddenInput(attrs={'type': 'hidden'})
        }



class GirisFormu(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kullanıcı Adı'}),
        label="Kullanıcı Adı"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Şifre'}),
        label="Şifre"
    )