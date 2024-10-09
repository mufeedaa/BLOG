from django.conf import settings
from django.urls import path
from .views import home, sign_in, registration, forgotpassword, resetpassword, otp, error_page
from django.conf.urls.static import static

urlpatterns = [
     path('', home, name='site_home'),
     path('login/', sign_in, name='site_login'),
     path('registration/', registration, name='site_registration'),
     path('forgotpassword/', forgotpassword, name='site_forgotpassword'),
     path('resetpassword/', resetpassword, name='site_resetpassword'),
     path('otp/', otp, name='site_otp'),
     path('404/', error_page, name='site_errorpage')
]  

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    