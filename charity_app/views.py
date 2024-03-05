
from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from charity_app.forms import LoginForm, UserForm
from django.contrib.auth import login, logout

from charity_app.models import Institution, Donation, User, Category


# Create your views here.

class LandingPageView(View):
    def get(self, request):
        institution = Donation.objects.values('institution').annotate(dcount=Count('institution')).count()
        quantity = Donation.objects.values('institution').aggregate(Sum('quantity'))
        foundation = Institution.objects.filter(type='F')
        organization = Institution.objects.filter(type='O')
        collection = Institution.objects.filter(type='Z')



        ctx = {
            "institution": institution,
            "quantity": quantity['quantity__sum'],
            "foundation": foundation,
            "organization": organization,
            "collection": collection
        }

        return render(request, "index.html", ctx)


class AddDonationView(View):
    def get(self, request):
        category = Category.objects.all()
        institution = Institution.objects.all()

        ctx = {
            "category": category,
            "institution": institution,
        }

        if not request.user.is_authenticated:
            return redirect('login')

        return render(request, "form.html", ctx)

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/'


    def form_valid(self, form):
        email = form.user
        login(self.request, email)
        return super().form_valid(form)

    def form_invalid(self, form):
        if not User.objects.filter(email=self.request.POST['email']):
            return redirect('register')
        return super().form_invalid(form)



def logout_view(request):
    logout(request)
    return redirect('/')


class RegisterView(FormView):

    template_name = "register.html"
    form_class = UserForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        first_name = form.cleaned_data.get("name")
        last_name = form.cleaned_data.get("surname")
        new_user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        new_user.save()
        return super().form_valid(form)
