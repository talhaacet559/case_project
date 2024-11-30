from django.urls import path
from .views import IzinFormView, CustomLoginView, CustomLogoutView, IzinListView, IzinUpdateView, IzinDeleteView

urlpatterns = [
    path("izinform/", IzinFormView.as_view(), name= 'izinform'),
    path("login/", CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path("dashboard/", IzinListView.as_view(), name='dashboard'),
    path('izin/edit/<int:izin_id>/', IzinUpdateView.as_view(), name='edit_izin'),
    path('izin/delete/<int:pk>/', IzinDeleteView.as_view(), name='izin_delete'),
    path("", CustomLoginView.as_view()),
]