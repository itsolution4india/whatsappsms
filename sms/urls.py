from django.urls import path
from django.contrib import admin
from smsapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path("admin/", admin.site.urls),
    path("", views.user_login, name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("send-sms/", views.Send_Sms, name="send-sms"),
    path('reports/', views.Reports, name='reports'),
    #path('download_report/<int:report_id>/',views.download_campaign_report, name='report_download'),
    path('download_report/<int:report_id>/', views.download_campaign_report, name='report_download'),
    path('campaign/', views.Campaign, name='campaign'),
    #path('campaign/delete/<str:template_id>/', views.delete_campaign, name='delete_campaign'),
    path('media_upload/', views.upload_media, name='upload_media'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path("reset-password/", views.initiate_password_reset, name="initiate_password_reset"),
    path("otp-verification/<str:email>/<str:token>/",views.verify_otp,name="otp_verification"),
    path("change-password/<str:email>/<str:token>/",views.change_password, name="change_password"),
    # path('facebook-sdk/',views.facebook_sdk_view, name='facebook_sdk'), # Pending 
    
 
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
