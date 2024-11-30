from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import Q, fields, ExpressionWrapper, F, Sum
from django.utils.timezone import now
from .models import Izin
from.utils import period_decider



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
def izin_post_delete(sender,instance,  **kwargs):
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
