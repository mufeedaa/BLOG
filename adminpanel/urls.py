from django.conf import settings
from django.urls import path
from .views import (adminhome, admin_sign_in,  userlist, userstatus,user_published_blog, userview,
 hide_comments,show_comments,activeusers, inactiveusers, bloglist, blogstatus,  
  blogview, user_blog_list, user_hidden_blog, resetpassword, admin_sign_out)
from django.conf.urls.static import static

urlpatterns = [
     
     path('', admin_sign_in, name='admin_login'),
     path('adminhome/', adminhome, name='admin_home'),
     path('userlist/', userlist, name='admin_userlist'),
     path('userstatus/<int:user_id>/', userstatus, name='admin_userstatus'),
     path('viewuser/<int:user_id>/', userview, name='admin_viewuser'),
     path('activeusers/', activeusers, name = 'admin_activeusers'),
     path('inactiveusers/', inactiveusers, name = 'admin_inactiveusers'),
     path('bloglist/', bloglist, name='admin_bloglist'),
     path('blogstatus/<int:blog_id>/', blogstatus, name='admin_blogstatus'),
     path('userpublishedblog/<int:user_id>/', user_published_blog, name='admin_publishedblog'),
     path('userbloglist/<int:user_id>/', user_blog_list, name='admin_userbloglist'),
     path('userhiddenblog/<int:user_id>/', user_hidden_blog, name='admin_userhiddenblog'),
#      path('commentstatus/<int:comment_id>/', comment_status, name='admin_commentstatus'),
     path('blogview/<int:blog_id>/', blogview, name='admin_blogview'),
     path('resetpassword/', resetpassword, name='admin_resetpassword'),
     path('hidecomments/<int:comment_id>/', hide_comments, name='admin_hidecomments'),
     path('showcomments/<int:comment_id>/', show_comments, name='admin_showcomments'),
      path('signout/', admin_sign_out, name='admin_signout')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
