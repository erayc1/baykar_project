from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name='index'),
    path('user-rent-data/', views.user_rent_data, name='user_rent_data'),
    path("admin-login/", views.admin_login, name='admin_login'),
    path("sign-up/", views.signUp, name='sign_up'),
    path("api/sign-up/", views.user_signUp_api, name='sign_up_api'),
    path("login/", views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path("api/login/", views.user_login_api, name='login_api'),
    path("api/add-rent-record/", views.add_rent_record, name='add_rent_record'),
    path("admin-home/", views.admin_home, name='admin_home'),
    path("admin-iha-add/", views.admin_iha_add, name='admin_iha_add'),
    path("api/admin-login/", views.admin_login_api, name='admin_login_api'),
    path('logout/', views.admin_logout, name='logout_admin'),
    path('admin-register/', views.admin_register, name='admin_register'),
    path("api/admin-register/", views.admin_register_api, name='admin_register_api'),
    path('users-data/', views.users_data, name='users_data'),
    path('iha-data/', views.iha_data, name='iha_data'),
    path('rent-data/', views.rent_data, name='rent_data'),
    path('api/admin-ihaAdd/', views.admin_iha_add_api, name='admin_ihaAdd_api'),
    path('api/delete-rent-record/', views.delete_rent_record, name='delete_rent_record'),
    path('api/update-rent-record/', views.update_rent_record, name='update_rent_record'),
    path('api/get-all-ihas/', views.get_all_ihas, name='get_all_ihas'),
    path('api/update-iha/', views.update_iha, name='update_iha'),
    path('api/delete-iha/', views.delete_iha, name='delete_iha'),


]
