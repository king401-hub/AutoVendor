from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
  path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
      path('about/', views.about, name='about'),
        path('cars/', views.cars, name='cars'),
          path('blog/', views.blog, name='blog'),
          path('privacypolicy/', views.privacypolicy, name='privacypolicy'),
          path('termsandconditions/', views.termsandconditions, name='termsandconditions'),
            path('contact/', views.contact, name='contact'),
              path('feature/', views.feature, name='feature'),
                path('service/', views.service, name='service'),
                  path('team/', views.team, name='team'),
                  path('car_list/', views.car_list, name='car_list'),
                    path('testimonial/', views.testimonial, name='testimonial'),
                    path('register/', views.register, name='register'),
                    path('password_reset/', views.password_reset, name='password_reset'),
                            path('password_reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
                                    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
                                            path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),
                                            path('inspect/', views.inspect, name='inspect'),
                                                 path('service/', views.service, name='service'),
                                                 path('sell_car/', views.sell_car, name='sell_car'),
                                                 path('user_profile/update/', views.user_profile_update, name='user_profile_update'),

  path('dashboard/', views.dashboard, name='dashboard'),
  path('my_cars/', views.my_cars, name='my_cars'),
  path('chats/', views.chats, name='chats'),
  path('receipts/', views.receipts, name='receipts'),
  path('settings/', views.settings, name='settings'),


]

from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.settings_view, name='settings'),
    path('settings/profile/update/', views.user_profile_update, name='user_profile_update'),
    path('settings/notifications/update/', views.update_notification_settings, name='update_notification_settings'),
    path('settings/privacy/update/', views.update_privacy_settings, name='update_privacy_settings'),
    path('settings/account/update/', views.update_account_settings, name='update_account_settings'),
    path('settings/appearance/update/', views.update_appearance_settings, name='update_appearance_settings'),
    path('settings/password/change/', views.change_password, name='change_password'),
]