from django.conf import settings
from django.urls import path
from .views import userhome, viewprofile, editprofile,deleteblog, addblog, editblog, viewblog, edit_comment, delete_comment, myblog, draftblog, publishblog, bloglist,  resetpassword, sign_out
from django.conf.urls.static import static

urlpatterns = [

     path('', userhome, name='user_home'),
     path('viewprofile/', viewprofile, name='user_viewprofile'),
     path('editprofile/', editprofile, name='user_editprofile'),
     path('addblog/', addblog, name='user_addblog'),
     path('editblog/<int:blog_id>/', editblog, name='user_editblog'),
     path('deleteblog/<int:blog_id>/', deleteblog, name='user_deleteblog'),
     path('viewblog/<int:blog_id>/', viewblog, name='user_viewblog'),
     path('myblog/', myblog, name='user_myblog'),
     path('draftblog/', draftblog, name='user_draftblog'),
     path('publishblog/', publishblog, name='user_publishblog'),
     path('bloglist/', bloglist, name='user_bloglist'),
     path('editcomment/<int:comment_id>/', edit_comment, name='user_editcomment'),
     path('deletecomment/<int:comment_id>/', delete_comment, name='user_deletecomment'),
     path('resetpassword', resetpassword, name='user_resetpassword'),  
     path('logout/', sign_out, name = 'logout')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
