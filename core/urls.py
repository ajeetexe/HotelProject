"""core URL Configuration

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
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register_user,name='register'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('forget-password/send-mail/',views.send_mail,name='forget-password'),
    path('forget-password/check-mail/<data>/',views.check_mail,name='check-mail'),
    path('forget-password/set-password/',views.set_password,name='set-password'),
    path('special-package/',views.special_package,name = 'special-package'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('restraunt/',views.restraunt,name='restraunt'),
    path('gallery/hotels/',views.gallery_hotel,name='hotel'),
    path('gallery/rooms/',views.gallery_rooms,name='rooms'),
    path('roomview/<check_in>&<check_out>/',views.room_view,name='room-view'),
    path('booking/<room_id>/<checkin>&<checkout>/',views.booking,name='booking'),
    path('profile/',views.profile,name='profile'),
    path('payment/<booking_id>/',views.payment,name='payment'),
    path('term-and-condition/',views.term_condition,name='term-conditon'),
    path('profile/know-more/<booking_id>',views.know_more,name='know-more'),
    path('admin/', admin.site.urls),
    path('payment/receipt/<p_id>/<status>/',views.payment_receipt,name='payment-receipt'),
    path('special-package/check/',views.check_avaiblity,name='check'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
