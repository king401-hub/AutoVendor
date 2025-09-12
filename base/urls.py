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
    # ✅ views.home must be a callable (a function)

]
