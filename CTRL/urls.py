from CTRL import views
from django.urls import path


urlpatterns = [
    path('', views.login, name='login'),
    path('shift/', views.shift, name='shift'),
    # url(r'shift_page/$', shift, {'templates_name': 'shift_page.html'}),

]

"""
    path('', views.login, name='login'),
    path('shift/', views.shift, name='shift'),
    
"""
