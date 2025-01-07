import time
from datetime import timedelta

from django.contrib.auth import user_logged_in
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import Q, fields, ExpressionWrapper, F, Sum
from django.utils.timezone import now

from .constants import BILDIRIM_MSG_DICT
from .models import Izin, CalisanGiris, Bildirim
from .utils import period_decider


@receiver(post_save, sender=Izin)
def izin_post_save(sender, instance, **kwargs):
    calisan = instance.calisan
    year = period_decider(calisan.date_joined, now())
    start_date = calisan.date_joined.replace(year=year)
    end_date = calisan.date_joined.replace(year=year + 1)
    Izinler = Izin.objects.filter(Q(izin_baslangic__gte=start_date) & Q(izin_bitis__lte=end_date),
                                  calisan_id=calisan.pk).exclude(onay__in=["DENIED", "CANCELLED"])
    days_difference = ExpressionWrapper(
        F('izin_bitis') - F('izin_baslangic'),
        output_field=fields.DurationField()
    )
    kullanilan_izin = (Izinler.annotate(diff_days=days_difference)
                       .aggregate(total_days=Sum('diff_days'))
                       )
    calisan.kullanilan_izin = kullanilan_izin["total_days"].days
    calisan.save()


@receiver(pre_delete, sender=Izin)
def izin_post_delete(sender, instance, **kwargs):
    calisan = instance.calisan
    year = period_decider(calisan.date_joined, now())
    start_date = calisan.date_joined.replace(year=year)
    end_date = calisan.date_joined.replace(year=year + 1)
    Izinler = Izin.objects.filter(Q(izin_baslangic__gte=start_date) & Q(izin_bitis__lte=end_date),
                                  calisan_id=calisan.pk).exclude(onay__in=["DENIED", "CANCELLED"])
    days_difference = ExpressionWrapper(
        F('izin_bitis') - F('izin_baslangic'),
        output_field=fields.DurationField()
    )
    kullanilan_izin = (Izinler.annotate(diff_days=days_difference)
                       .aggregate(total_days=Sum('diff_days'))
                       )
    calisan.kullanilan_izin = (kullanilan_izin["total_days"].days
                               - abs((instance.izin_bitis - instance.izin_baslangic).days))
    calisan.save()


@receiver(user_logged_in)
def on_login(sender, request, user, **kwargs):
    giris_zamani = now()
    baslangic = giris_zamani.replace(hour=8, minute=0, second=0, microsecond=0)
    bitis = giris_zamani.replace(hour=23, minute=59, second=59, microsecond=999999)
    msg = BILDIRIM_MSG_DICT["giris"]
    ilk_giris_kontrol = CalisanGiris.objects.filter(
        calisan=user,
        giris_zamani__range=(baslangic, bitis)
    ).exists()
    giris_nesne = CalisanGiris.objects.create(
        calisan = user,
        giris_zamani = giris_zamani,
        ilk_giris = not ilk_giris_kontrol

    )
    mesai_zamani = giris_zamani.replace(hour=9, minute=0, second=0, microsecond=0)
    gec_sure = abs(giris_zamani - mesai_zamani)
    print("gec_sure:", gec_sure)
    if giris_nesne.ilk_giris and gec_sure > timedelta(minutes=15):
        user.gec_biriken += int(gec_sure.total_seconds() / 60)
        biriken_gun = (user.gec_biriken / 60) / 24
        print("biriken_gun:", biriken_gun)
        msg = BILDIRIM_MSG_DICT["ilk_giris_gec"]
        print()
        if user.gec_biriken / 24 * 60 > 1:
            user.gec_biriken -= biriken_gun*24*60
            user.kullanilan_izin += biriken_gun
            print("kullanilan_izin_son:", user.kullanilan_izin)
            user.save()
    elif giris_nesne.ilk_giris:
        msg = BILDIRIM_MSG_DICT["ilk_giris"]
    Bildirim.objects.create(
        calisan = user,
        message = msg.format(calisan=user, giris=giris_zamani)
    )




