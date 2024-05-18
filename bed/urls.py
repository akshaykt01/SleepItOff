"""
URL configuration for bed project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')
"""
from django.contrib import admin
from django.urls import path
from bedapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('login', views.log),
    path('signup', views.signup),
    path('contact', views.contact),
    path('feedback', views.feedback),
    path('profile', views.profile),
    path('manage', views.manage),
    path('test', views.test),
    path('warden_bookings', views.warden_bookings),
    path('delete_and_archive_bookings', views.delete_and_archive_bookings),
    path('wardenprofile', views.wardenprofile),
    path('wardenlogin', views.wardenlog),
    path('wardensignup', views.wardensignup),
    path('wardenpasswordreset', views.wardenpasswordreset),
    path('home', views.home),
    path('hostels', views.hostels),
    path('logout', views.logout),
    path('confirm', views.confirm),
    path('allhostels', views.allhostels),
    path('allusers', views.allusers),
    path('allbookings', views.allbookings),
    path('user_bookings', views.user_bookings),
    path('remove', views.remove),
    path('pending', views.pending),
    path('prfimg', views.prfimg),
    path('wprfimg', views.wprfimg),
    path('locselect', views.locselect),
    path('wardenhstl', views.wardenhstl),
    path('hostelupdate', views.hostelupdate),
    path('hstldescription/<a>', views.hstldescription),
    path('about', views.about),
    path('pr', views.pr),
    path('passwordreset', views.passwordreset),
    path('pay/<int:id>', views.pay),
    path('success', views.success),
    path('hostelupdatetrue', views.hostelupdatetrue),
    path('save_room_to_session/', views.save_room_to_session, name='save_room_to_session'),
    path('wardenbookings', views.wardenbookings),
    path('warden_cancelled_bookings', views.warden_cancelled_bookings),
    path('forgot', views.forgot_password, name='forgot'),
    path('reset/<token>',views.reset_password,name='reset_password'),
    path('roomandbed', views.roomandbed),
    path('process_input', views.process_input),
    path('select_bed/<int:room_id>/', views.select_bed, name='select_bed'),
    path('show_rooms/<a>', views.show_rooms),
    path('show-beds/<str:room_number>/', views.show_beds, name='show_beds'),
    path('show-beds/<str:room_id>/payment/<str:bed_number>/', views.payment, name='payment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
