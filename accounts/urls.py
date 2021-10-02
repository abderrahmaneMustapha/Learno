from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from . import views
from  django.conf import settings

from rest_framework import routers
router = routers.DefaultRouter()
router.register('students', views.StudentView)


urlpatterns = [
    #rest api urls
    path('api-students/', include(router.urls)),

    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('', views.home, name='home'),
    #account views
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('oauth/', include('social_django.urls', namespace='social')),  # <--
    path('accounts/', include('django.contrib.auth.urls')),
    #login and logout views
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),


    #Sign up view
    path('accounts/signup/', views.signup, name='signup'),

    #reset password views
    path('accounts/password_change/',auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'),name='password_change'),
    path('accounts/password_change/done/',auth_views. PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),name='password_change_done'),
    path('accounts/password_reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),name='password_reset'),
    path('accounts/password_reset/done/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/ ',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('accounts/reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),


    #quizzes urls
    path('all-quizzes/',views.quizzes_view,name='quizzes'),
    path('all-quizzes/<quiz>',views.stages_view,name='stages'),
    path('all-quizzes/stages/<stage>/',views.questions_view,name='questions'),
    path('all-quizzes/stages/<stage>/stage-result/<stage_result>/',views.stage_result_view,name='stage_result'),



    # other users profiles and raking urls
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('profile/<user>/', views.profiles, name='user_profile'),

   #email confirmation
   #path('activate/<uidb64>/<token>/',
        #views.activate, name='activate'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
