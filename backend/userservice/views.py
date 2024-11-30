from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView, UpdateView, DeleteView
from .forms import IzinForm, GirisFormu
from django.contrib import messages

from .models import Izin


class IzinFormView(FormView, LoginRequiredMixin):
    template_name = 'izin.html'
    form_class = IzinForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(IzinFormView, self).get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {"calisan": self.request.user}
        return kwargs

    # This method is called when the form is valid (on successful submission)
    def form_valid(self, form):
        # Save the form and associate the object with the user if needed
        object = form.save()  # Saving the form (assuming you have a save method)

        messages.success(self.request, "Object created successfully!")  # Success message

        # Render the same template with the object and the success message
        return render(self.request, 'izin.html', {'form': form, 'object': object})

    # Optionally, you can override `form_invalid` to handle invalid form submissions
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True  # Redirect logged-in users away from login page
    authentication_form = GirisFormu

class CustomLogoutView(LogoutView):
    template_name = "logout.html"

class IzinListView(LoginRequiredMixin, ListView):
    model = Izin
    template_name = 'dashboard.html'  # Your template
    context_object_name = 'izin_objects'  # Name of the variable in the template
    paginate_by = 10  # Optional: Pagination if you have many records

    def get_queryset(self):
        # Fetch only the Izin objects related to the logged-in user
        return Izin.objects.filter(calisan_id=self.request.user.pk)

class IzinUpdateView(UpdateView):
    model = Izin
    form_class = IzinForm
    template_name = 'edit_izin.html'
    context_object_name = 'izin'
    success_url = reverse_lazy('dashboard')  # Redirect to the list page after successful edit

    def get_object(self, queryset=None):
        izin = Izin.objects.get(id=self.kwargs['izin_id'])
        print(f"Fetched Izin with ID: {izin.id}, Baslangic: {izin.izin_baslangic}")
        return izin

    def get_form_kwargs(self):
        """
        Pass the instance to the form for editing.
        """
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()  # Pass the current object instance
        return kwargs


class IzinDeleteView(DeleteView):
    model = Izin
    template_name = 'izin_confirm_delete.html'  # Optional: Add a confirmation page
    success_url = reverse_lazy('dashboard')  # Redirect after deletion


