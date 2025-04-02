from django.urls import path
from . import views
from .views import contact_messages, read_message, delete_message


urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_post/<slug:slug>/', views.edit_post, name='edit_post'),
    path('delete_blog/<slug:slug>/', views.delete_post, name='delete_blog'),
    path('edit_book/<int:book_id>/', views.edit_books, name='edit_book'),
    path('delete_book/<int:book_id>', views.delete_books, name='delete_book'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword/', views.resetPassword, name='resetpassword'),
    path('change_password/', views.change_password, name="change_password"),
    path('messages/', contact_messages, name='contact_messages'),
    path('messages/read/<int:message_id>/', read_message, name='read_message'),
    path('messages/delete/<int:message_id>/', delete_message, name='delete_message'),
]
