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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('name/',views.busdetails),
    path("logout", views.logout_request, name="logout"),
    path('login/', views.login_request),
    path('searchbar/',views.searchbar,name='searchbar'),
    path('searchbar1/',views.searchbar1,name='searchbar1'),                     
    path('signup/',views.signup),
    path('front/',views.front),
    path('create/', views.create, name='create'),
    path('qr-code-decoder/', views.qrcode_decoder, name='qrcode_decoder' ),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),
    path('success/', views.success, name='success'),
    path('pay_id/',views.pay_id,name='pay_id'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

