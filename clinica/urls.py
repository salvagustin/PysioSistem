from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from gestor.views import *
from gestor import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestor.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', inicio),
    path('inicio/', inicio),
    path('estadisticas/', estadisticas),
    path('dashboard/', dashboard, name='dashboard'),
    path('historia/', views.historia, name='historia'),
    
    #DIRECCION DOCTORES
    path('doctores/', views.lista_doctores, name='lista_doctores'),
    path('agregardoctor/', views.crear_doctor, name='crear_doctor'),
    path('editardoctor/<int:pk>/', views.editar_doctor, name='editar_doctor'),
    path('eliminardoctor/<int:pk>/', views.eliminar_doctor, name='eliminar_doctor'),

    #DIRECCION PACIENTES
    path('pacientes/', ListaPacientes, name='ListaPacientes'),
    path('agregarpaciente/', crear_paciente, name='crear_paciente'),
    path('editarpaciente/<int:pk>/', editar_paciente, name='editar_paciente'),
    path('eliminarpaciente/<int:pk>/', eliminar_paciente, name='eliminar_paciente'),
    path('historial/<int:pk>/', paciente_historial, name='paciente_historial'),
    path('historialid/<int:pk>/', paciente_historialid, name='paciente_historialid'),
    path('buscarpaciente/<name>/', buscar_paciente, name='buscar_paciente'),
    path('buscarpacienteindex/<str:name>/', buscar_paciente_index, name='buscar_paciente_index'),
    #DIRECCION CONSULTAS
    path('consultas/', ListaConsultas, name='ListaConsultas'),
    path('agregarconsulta/', crear_consulta, name='crear_consulta'),
   # path('agregarconsultapaciente/', crear_consulta2),#Esta url es para agregar una consulta desde el perfil del paciente
    path('editarconsulta/<int:pk>/', editar_consulta, name='editar_consulta'),
    path('eliminarconsulta/<int:pk>/', eliminar_consulta,   name='eliminar_consulta'),
    path('buscarconsulta/<name>',buscar_consulta, name='buscar_consulta'),
    #DIRECCION CITAS
    path('citas/', ListaCitas, name='ListaCitas'),
    path('agregarcita/', crear_cita, name='crear_cita'),
    path('editarcita/<int:pk>/', editar_cita, name='editar_cita'),
    path('eliminarcita/<int:pk>/', eliminar_cita, name='eliminar_cita'),
    path('buscarsemana/<int:numano>/<int:numse>/', buscar_semana, name='buscar_semana'),
    
    
    #DIRECCION RECETAS
    path('recetas/', ListaRecetas, name='ListaRecetas'),
    path('agregarreceta/', crear_receta, name='crear_receta'),
    path('editarreceta/<int:pk>/', editar_receta, name='editar_receta'),
    path('eliminarreceta/<int:pk>/', eliminar_receta, name='eliminar_receta'),
    path('buscarreceta/<name>',buscar_receta, name='buscar_receta'),
    path('imprimirreceta/<int:pk>/', views.imprimirreceta.as_view(), name='imprimirreceta'),
    
    #DIRECCION EJERCICIOS
    path('ejercicios/', ListaEjercicios, name='ListaEjercicios'),
    path('agregarejercicio/', crear_ejercicio, name='crear_ejercicio'),
    path('editarejercicio/<int:pk>/', editar_ejercicio, name='editar_ejercicio'),
    path('eliminarejercicio/<int:pk>/', eliminar_ejercicio, name='eliminar_ejercicio'),
    path('eliminar-imagen/<int:imagen_id>/', views.eliminar_imagen, name='eliminar_imagen'),


    #DIRECCION CLIENTES
    
    path('citascliente/', agendar_cita, name='agendar_cita'),
    path('ejercicioscliente/', views.ejercicios_cliente, name='ejercicios_cliente'),
    path('api/subcategorias/', views.api_subcategorias, name='api_subcategorias'),
    path('api/ejercicios/', views.api_ejercicios, name='api_ejercicios'),
]   
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)