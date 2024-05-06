from django.urls import path, include
from django.contrib import admin
from smsapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.user_login, name="login"),
    path("send-sms/", views.Send_Sms, name="send-sms"),
    path('reports/', views.Reports, name='reports'),
    path('campaign/', views.Campaign, name='campaign'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path("reset-password/", views.initiate_password_reset, name="initiate_password_reset"),
    path("otp-verification/<str:email>/<str:token>/",views.verify_otp,name="otp_verification"),
    path("change-password/<str:email>/<str:token>/",views.change_password, name="change_password"),
 
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)