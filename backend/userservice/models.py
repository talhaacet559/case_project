import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import PositiveIntegerField

from .enums import IzinStatus
from django.utils.timezone import now



class Calisan(AbstractUser):
    departman = models.CharField(max_length=100, blank=True)
    izin_hakki = models.PositiveIntegerField(default=15)
    kullanilan_izin = models.PositiveIntegerField(default=0)
    sonraki_dönem_kullanilan_izin = models.PositiveIntegerField(default=0)
    izinli = models.BooleanField(default=False)
    izin_ceza =PositiveIntegerField(default=0)
    gec_biriken = models.IntegerField(default=0)


class Izin(models.Model):
    calisan: Calisan = models.ForeignKey(
        Calisan,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    izin_baslangic = models.DateField(default=now)
    izin_bitis = models.DateField(default=now() + datetime.timedelta(1))
    zaruri = models.BooleanField(default=False)
    gerekce = models.CharField(max_length=255, blank=True)
    onay = models.CharField(max_length=255, choices=IzinStatus.choices(), default=IzinStatus.INITIATED,
                            auto_created=True)
    olusturulma_zamani = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return (
            f"{self.olusturulma_zamani} -- {self.calisan} {self.izin_baslangic}-{self.izin_bitis} "
            f"{abs((self.izin_baslangic - self.izin_bitis).days)} gün")

    def clean(self, **kwargs):
        diff = abs(self.izin_baslangic - self.izin_bitis)
        if self.izin_bitis < self.izin_baslangic:
            raise ValidationError("Bitiş günü başlangıçtan sonra olmalıdır.")
        if (self.calisan.izin_hakki - self.calisan.kullanilan_izin) < diff.days:
            raise ValidationError("Yetersiz izin günü.")
        overlapping_izinler = Izin.objects.filter(
            calisan=self.calisan,
            izin_bitis__gte=self.izin_baslangic,
            izin_baslangic__lte=self.izin_bitis,
        )
        if self.pk:
            overlapping_izinler = overlapping_izinler.exclude(pk=self.pk)
        if overlapping_izinler.exists():
            raise ValidationError("Belirtilen tarihlerde çakışan başka bir izin bulunuyor."
                                  " Lütfen mevcut izin üzerinden düzenleme yapınız.")
        if self.zaruri and not self.gerekce:
            raise ValidationError("Zaruri izinlerde lütfen gerekçe giriniz.")
        super().clean()

    class Meta:
        verbose_name = "İzin"
        verbose_name_plural = "İzinler"


class CalisanGiris(models.Model):
    calisan = models.ForeignKey(
        Calisan,
        verbose_name='Çalışan',
        on_delete=models.DO_NOTHING
    )
    giris_zamani = models.DateTimeField(verbose_name="Giriş Zamanı")
    ilk_giris = models.BooleanField()
    class Meta:
        verbose_name = "Calisan Giris"
        verbose_name_plural = "Calisan Girisleri"

    def __str__(self):
        etiket = "Mesai Başlangici" if self.ilk_giris else "Giris"
        return f"{self.calisan} -- {self.giris_zamani}--{etiket}"


class Bildirim(models.Model):
    calisan: Calisan = models.ForeignKey(
        Calisan,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    message = models.CharField(max_length=255, default="")
    class Meta:
        verbose_name = "Bildirim"
        verbose_name_plural = "Bildirimler"

    def __str__(self):
        return self.message




