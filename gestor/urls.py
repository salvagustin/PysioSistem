from django.urls import path
from . import views


urlpatterns = [
    #path('salir/', views.salir, name='salir'),
    path('get_chart/',views.get_chart, name='get_chart'),
    path('get_chart2/',views.get_chart2, name='get_chart2'),
    path('get_chart3/',views.get_chart3, name='get_chart3'),
    path('get_chart4/',views.get_chart4, name='get_chart4'),
    path('get_chart5/',views.get_chart5, name='get_chart5')

    #path('', views.index, name='inicio')
]