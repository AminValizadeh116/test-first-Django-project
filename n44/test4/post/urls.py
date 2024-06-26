from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView

app_name = "post"

urlpatterns = [
    path('list/', post_list, name='post_list'),
    path('list/<str:category>/', post_list, name='category'),
    path('list/detail/<int:pk>/', post_detail, name='post_detail'),

    path('<int:post_pk>/comment/', comment_view, name='comment'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', log_out, name='logout'),
    path('password-change/', PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(success_url='done'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(success_url='/post/password-reset/complete'), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    path('profile/delete-post/<int:post_id>/', delete_post, name='delete_post'),
    path('profile/edit-post/<int:post_id>/', edit_post, name='edit_post'),
    path('profile/create-post/', create_post, name='create_post'),
    path('profile/account/', create_account, name='create_account'),
]
