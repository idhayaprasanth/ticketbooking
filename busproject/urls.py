"""busproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from busapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from busapp.views import ( 
    change_password, change_email, change_username
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('name/',views.busdetails, name="name"),
    path("logout", views.logout_request, name="logout"),
    path('login/', views.login_request,name="login"),
    path('searchbar/',views.searchbar,name='searchbar'),
    path('searchbar1/',views.searchbar1,name='searchbar1'),                     
    path("signup/", views.signup, name="signup"),
    path('front/',views.front),
    path('create/', views.create, name='create'),
    path('qr-code-decoder/', views.qrcode_decoder, name='qrcode_decoder' ),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),
    path('success/', views.success, name='success'),
    path('pay_id/',views.pay_id,name='pay_id'),
    path('get_payments/',views.get_payments,name='get_payments'),
    path('timetable/',views.timetable,name='timetable'),
    path('analysis/',views.bus_data_analysis,name="bus_data_analysis"),

     # Password Reset URLs (Django Built-in Views)
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),

    # Change Credentials
    path("change_password/", change_password, name="change_password"),
    path("change_email/", change_email, name="change_email"),
    path("change_username/", change_username, name="change_username"),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

