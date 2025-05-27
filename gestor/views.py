from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from gestor.models import *
from gestor.forms import *
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Sum,Count
from django.db.models.functions import ExtractMonth
from django.db.models.expressions import RawSQL
from django.views.generic import View
from datetime import timedelta, date
from urllib.parse import urlencode
from .utils import render_to_pdf
import datetime
from datetime import datetime, timedelta, date
from decimal import Decimal, InvalidOperation


#OBTENER FECHA ACTUAL Y FORMATEAR SEMANA Y MES ACTUALES
horayfecha = datetime.now()
horaactual = horayfecha.hour
semanaactual = horayfecha.isocalendar().week
anoactual = horayfecha.isocalendar().year
mesactualnumero = horayfecha.strftime("%m").capitalize()


# FUNCION PARA OBTENER EL PRIMER DIA DE LA UNA SEMANA INGRESADA
def first_day_of_iso_week(year, week):
    date = datetime(year, 1, 4)
    
    start_iso_week, start_iso_day = date.isocalendar()[1:3]
    
    weeks_diff = week - start_iso_week
    days_to_monday = timedelta(days=(1-start_iso_day))
    
    return date + days_to_monday + timedelta(weeks=weeks_diff)


##### OBTENER NOMBRE DEL MES
def nombre_mes(mesactualnumero): 
    match mesactualnumero:
            case "01" :
                mesactual ="Enero" 
            case "02":
                mesactual ="Febrero" 
            case "03":
                mesactual ="Marzo"
            case "04" :
                mesactual ="Abril" 
            case "05":
                mesactual ="Mayo" 
            case "06":
                mesactual ="Junio" 
            case "07" :
                mesactual ="Julio" 
            case "08":
                mesactual ="Agosto" 
            case "09":
                mesactual ="Septiembre"
            case "10" :
                mesactual ="Octubre" 
            case "11":
                mesactual ="Noviembre" 
            case "12":
                mesactual ="Diciembre"
   
    return mesactual

#######################################################################
# FUNCION PARA OBTENER LA INFORMACION DEL INDEX

def infohome():
    hoy = horayfecha.date()
    pacientes = Paciente.objects.all()
    citas = Cita.objects.filter(fechacita=hoy)
    consultasdiarias = Consulta.objects.filter(fechaconsulta=hoy).count()
    devengadodiario = Consulta.objects.filter(fechaconsulta=hoy).aggregate(Sum('precioconsulta')).get('precioconsulta__sum')

    if devengadodiario is None:
        devengadodiario = 0

    # Tablas de horarios
    horario = {
        'matutino': {
            '8': '',
            '9': '',
            '10': '',
            '11': ''
        },
        'vespertino': {
            '13': '',
            '14': '',
            '15': '',
            '16': '',
            '17': ''
        }
    }

    # Llenamos el horario con los pacientes correspondientes
    for cita in citas:
        hora = cita.horacita  # CharField
        if hora in horario['matutino']:
            horario['matutino'][hora] = cita.paciente.nombre
        elif hora in horario['vespertino']:
            horario['vespertino'][hora] = cita.paciente.nombre

    data = {
        'proximacita': citas,
        'citashoy': citas.count(),
        'consultashoy': consultasdiarias,
        'devengadohoy': devengadodiario,
        'pacientes': pacientes,
        'horario': horario,
        'mensaje': 0  # Opcional para alertas
    }

    return data

@login_required
def inicio(request):
    data = infohome()
    return render(request, 'index.html', data)

@login_required
def salir(request):
    logout(request)
    return redirect('login.html')

######### FUNCION PARA CREAR EL GRAFICO DE CONTEO DE CONSULTAS
@login_required
def get_chart(request):
    #FOR QUE CONSULTA EL TOTAL DE CONSULTAS POR MES
    conteoconsultas = []
    for i in range(1,13):
        consulta = Consulta.objects.filter(fechaconsulta__month=i).count()
        conteoconsultas.append(consulta)
   
    colors = ['#5470C6']

    chart = {
        'title': {
            'text': 'Consultas por Mes',
            'left': 'center',
            'textStyle': {
                'fontSize': 18,
                'fontWeight': 'bold'
            }
        },
        'color': colors,
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'shadow'  # mejor visual con barras
            }
        },
        'toolbox': {
            'feature': {
                'saveAsImage': {'show': True},
                'dataView': {'show': True, 'readOnly': False},
                'restore': {'show': True}
            },
            'right': 20
        },
        'legend': {
            'data': ['Consultas'],
            'top': '10%'
        },
        'grid': {
            'left': '3%',
            'right': '4%',
            'bottom': '5%',
            'containLabel': True
        },
        'xAxis': [
            {
                'type': "category",
                'data': ["En", "Feb", "Mar", "Ab", "May", "Jun", "Jul", "Ago", "Sept", "Oct", "Nov", "Dec"],
                'axisTick': {'alignWithLabel': True},
                'axisLine': {'lineStyle': {'color': '#aaa'}}
            }
        ],
        'yAxis': [
            {
                'type': "value",
                'axisLine': {'lineStyle': {'color': '#aaa'}},
                'splitLine': {'lineStyle': {'type': 'dashed'}}
            }
        ],
        'series': [
            {
                'name': 'Consultas',
                'type': "bar",
                'barWidth': '60%',
                'data': conteoconsultas,
                'itemStyle': {
                    'borderRadius': [5, 5, 0, 0],
                    'color': {
                        'type': 'linear',
                        'x': 0,
                        'y': 0,
                        'x2': 0,
                        'y2': 1,
                        'colorStops': [
                            {'offset': 0, 'color': '#5470C6'},
                            {'offset': 1, 'color': '#91CC75'}
                        ]
                    }
                },
                'emphasis': {
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowOffsetX': 0,
                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    }
 
    return JsonResponse(chart)


######### FUNCION PARA CREAR EL GRAFICO DE SUMAR DE GANANCIAS POR MES
@login_required
def get_chart2(request):
   
    #FOR QUE CONSULTA EL TOTAL DE DEVENGADO POR MES
    consultatotal=[]
    for i in range(1,13):
        sumadevengado = Consulta.objects.filter(fechaconsulta__month =i).aggregate(Sum('precioconsulta')).get('precioconsulta__sum')
        if sumadevengado == None:
            sumadevengado=0 
        consultatotal.append(sumadevengado)
    colors = ['#73C0DE']  # azul suave para líneas

    chart2 = {
        'title': {
            'text': 'Ganancias Mensuales',
            'left': 'center',
            'textStyle': {
                'fontSize': 18,
                'fontWeight': 'bold'
            }
        },
        'color': colors,
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'line',
                'lineStyle': {
                    'color': '#aaa',
                    'width': 1,
                    'type': 'dashed'
                }
            }
        },
        'toolbox': {
            'feature': {
                'saveAsImage': {'show': True},
                'dataView': {'show': True, 'readOnly': False},
                'restore': {'show': True}
            },
            'right': 20
        },
        'legend': {
            'data': ['Ganancias'],
            'top': '10%'
        },
        'grid': {
            'left': '3%',
            'right': '4%',
            'bottom': '5%',
            'containLabel': True
        },
        'xAxis': [
            {
                'type': "category",
                'data': ["En", "Feb", "Mar", "Ab", "May", "Jun", "Jul", "Ago", "Sept", "Oct", "Nov", "Dec"],
                'axisLine': {'lineStyle': {'color': '#aaa'}}
            }
        ],
        'yAxis': [
            {
                'type': "value",
                'axisLine': {'lineStyle': {'color': '#aaa'}},
                'splitLine': {'lineStyle': {'type': 'dashed'}},
                'axisLabel': {'formatter': '${value}'}
            }
        ],
        'series': [
            {
                'name': 'Ganancias',
                'type': "line",
                'data': consultatotal,
                'smooth': True,
                'symbol': 'circle',
                'symbolSize': 8,
                'lineStyle': {
                    'width': 3
                },
                'areaStyle': {
                    'color': {
                        'type': 'linear',
                        'x': 0,
                        'y': 0,
                        'x2': 0,
                        'y2': 1,
                        'colorStops': [
                            {'offset': 0, 'color': 'rgba(115, 192, 222, 0.5)'},
                            {'offset': 1, 'color': 'rgba(115, 192, 222, 0)'}
                        ]
                    }
                },
                'emphasis': {
                    'focus': 'series',
                    'itemStyle': {
                        'borderWidth': 2,
                        'borderColor': '#3FB1E3',
                        'shadowBlur': 8,
                        'shadowColor': 'rgba(0, 0, 0, 0.3)'
                    }
                }
            }
        ]
    }

    return JsonResponse(chart2)


######### FUNCION PARA CREAR EL GRAFICO DEL HOME
@login_required
def get_chart3(request):
    colors = ['#5470C6', '#91CC75', '#EE6666']
    
    # Consultas: ganancias y conteo por mes
    consulta_por_mes = (Consulta.objects.annotate(mes=ExtractMonth('fechaconsulta')).values('mes').annotate(
                        total_ganancias=Sum('precioconsulta'),total_consultas=Count('idconsulta')))

    # Pacientes: conteo por mes
    paciente_por_mes = (Paciente.objects.annotate(mes=ExtractMonth('fechacreacion')).values('mes')
                        .annotate(total_pacientes=Count('idpaciente')))

    consultatotal = [0] * 12
    conteoconsultas = [0] * 12
    conteopacientes = [0] * 12

    for c in consulta_por_mes:
        index = c['mes'] - 1
        consultatotal[index] = float(c['total_ganancias'] or 0)
        conteoconsultas[index] = int(c['total_consultas'])

    for p in paciente_por_mes:
        index = p['mes'] - 1
        conteopacientes[index] = int(p['total_pacientes'])
    
    chart3 = {
    "color": colors,
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {
            "type": "cross"
        }
    },
    "grid": {
        "right": "20%"
    },
    "toolbox": {
        "feature": {
            "dataView": { "show": True, "readOnly": False },
            "restore": { "show": True },
            "saveAsImage": { "show": True }
        }
    },
    "legend": {
        "data": ["Ganancias", "Consultas", "Pacientes"]
    },
    "xAxis": [
        {
            "type": "category",
            "axisTick": { "alignWithLabel": True },
            "data": ["En", "Feb", "Mar", "Ab", "May", "Jun", "Jul", "Ago", "Sept", "Oct", "Nov", "Dic"]
        }
    ],
    "yAxis": [
        {
            "type": "value",
            "name": "Ganancias",
            "position": "right",
            "alignTicks": True,
            "axisLine": {
                "show": True,
                "lineStyle": { "color": colors[0] }
            },
            "axisLabel": { "formatter": "{value} $" }
        },
        {
            "type": "value",
            "name": "Consultas",
            "position": "right",
            "offset": 80,
            "alignTicks": True,
            "axisLine": {
                "show": True,
                "lineStyle": { "color": colors[1] }
            },
            "axisLabel": { "formatter": "{value}" }
        },
        {
            "type": "value",
            "name": "Pacientes",
            "position": "left",
            "alignTicks": True,
            "axisLine": {
                "show": True,
                "lineStyle": { "color": colors[2] }
            },
            "axisLabel": { "formatter": "{value}" }
        }
    ],
    "series": [
        {
            "name": "Ganancias",
            "type": "bar",
            "data": consultatotal
        },
        {
            "name": "Consultas",
            "type": "bar",
            "yAxisIndex": 1,
            "data": conteoconsultas
        },
        {
            "name": "Pacientes",
            "type": "line",
            "yAxisIndex": 2,
            "data": conteopacientes
        }
    ]
}

    return JsonResponse(chart3)

####### FUNCION PARA CALCULAR LA EDAD DE LOS PACIENTES #####
def calcular_edad(fecha_nacimiento):
    hoy = date.today()
    return hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))


######### FUNCION PARA CREAR EL GRAFICO COMBINADO DE LAS ESTADISTICAS
@login_required
def get_chart4(request):

    pacientes = Paciente.objects.all()
    # Inicializar los rangos
    rango_edad = {
        '1-10 años': 0,
        '11-18 años': 0,
        '19-30 años': 0,
        '31-45 años': 0,
        '46-60 años': 0,
        'Más de 60 años': 0
    }
    # Recorrer pacientes y contar por rango
    for paciente in pacientes:
        if paciente.fecha_nacimiento:
            edad = calcular_edad(paciente.fecha_nacimiento)

            if 1 <= edad <= 10:
                rango_edad['1-10 años'] += 1
            elif 11 <= edad <= 18:
                rango_edad['11-18 años'] += 1
            elif 19 <= edad <= 30:
                rango_edad['19-30 años'] += 1
            elif 31 <= edad <= 45:
                rango_edad['31-45 años'] += 1
            elif 46 <= edad <= 60:
                rango_edad['46-60 años'] += 1
            elif edad > 60:
                rango_edad['Más de 60 años'] += 1
   
    # Preparar datos para el pie chart
    pie_data = [{"name": k, "value": v} for k, v in rango_edad.items()]
    colors = ['#5470C6', '#91CC75', '#EE6666', '#FAC858', '#73C0DE', '#3BA272']

    chart4 = {
         'title': {
            'text': 'Edades de Pacientes',
            'left': 'center',
            'textStyle': {
                'fontSize': 18,
                'fontWeight': 'bold'
            }
        },
        "color": colors,
        "tooltip": {
            "trigger": "item",
            "formatter": "{a} <br/>{b}: {c} ({d}%)"
        },
        "legend": {
            "orient": "vertical",
            "left": "left",
            "data": list(rango_edad.keys())
        },
        "series": [
            {
                "name": "Pacientes",
                "type": "pie",
                "radius": "70%",
                "center": ["50%", "60%"],
                "data": pie_data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)"
                    }
                }
            }
        ]
    }
   
    return JsonResponse(chart4)

######### FUNCION PARA CREAR EL GRAFICO DE LOS 5 PACIENTES CON MAS CONSULTAS
@login_required
def get_chart5(request):
    # Obtener los 5 pacientes con más consultas
    top_pacientes = (
        Consulta.objects.values('paciente__nombre')
        .annotate(total=Count('paciente__idpaciente'))
        .order_by('-total')[:5]
    )

    nombres = [p['paciente__nombre'] for p in top_pacientes]
    cantidades = [p['total'] for p in top_pacientes]

    chart5 = {
        "title": {
            "text": "Top 5 Pacientes con Más Consultas",
            "left": "center",
            "textStyle": {
                "fontSize": 20,
                "fontWeight": "bold",
                "color": "#333"
            }
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow"
            }
        },
        "grid": {
            "left": "5%",
            "right": "5%",
            "bottom": "10%",
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "data": nombres,
            "axisLabel": {
                "interval": 0,
                "rotate": 15,
                "fontSize": 12,
                "color": "#666"
            },
            "axisLine": {
                "lineStyle": {
                    "color": "#ccc"
                }
            }
        },
        "yAxis": {
            "type": "value",
            "name": "Consultas",
            "axisLabel": {
                "color": "#666"
            }
        },
        "series": [{
            "data": cantidades,
            "type": "bar",
            "barWidth": "50%",
            "itemStyle": {
                "color": {
                    "type": "linear",
                    "x": 0,
                    "y": 0,
                    "x2": 0,
                    "y2": 1,
                    "colorStops": [
                        {"offset": 0, "color": "#42a5f5"},
                        {"offset": 1, "color": "#1e88e5"}
                    ]
                },
                "borderRadius": [5, 5, 0, 0]
            },
            "label": {
                "show": True,
                "position": "top",
                "color": "#000",
                "fontSize": 12
            }
        }]
    }

    return JsonResponse(chart5)


#################### ESTADISTICAS ###################################
@login_required
def estadisticas(request):

    #OBTENCION DE LAS FECHAS DE LA SEMANA
    first_day = first_day_of_iso_week(anoactual, semanaactual)
    lunes = first_day.date()
    citasmes = Cita.objects.filter(fechacita__month=mesactualnumero).count()
    consultasmes = Consulta.objects.filter(fechaconsulta__month =mesactualnumero).count()
    devengadomes = Consulta.objects.filter(fechaconsulta__month =mesactualnumero).aggregate(Sum('precioconsulta')).get('precioconsulta__sum')
    
    citasanio = Cita.objects.filter(fechacita__year=anoactual).count()
    consultasanio = Consulta.objects.filter(fechaconsulta__year =anoactual).count()
    devengadoanio = Consulta.objects.filter(fechaconsulta__year =anoactual).aggregate(Sum('precioconsulta')).get('precioconsulta__sum')
    
    pacientesmesactual = Paciente.objects.filter(fechacreacion__month=mesactualnumero).count()
    
    pacientesanio = Paciente.objects.filter(fechacreacion__year=anoactual).count()
    
    totalpacientes = Paciente.objects.count()
    totaldevengado = Consulta.objects.all().aggregate(Sum('precioconsulta')).get('precioconsulta__sum')
    totalcitas = Cita.objects.count()
    totalconsultas = Consulta.objects.count()
    mes = nombre_mes(lunes.strftime("%m").capitalize())
    data = {
        'year':anoactual,
        'devengadomes': devengadomes,
        'consultasmes': consultasmes,
        'mesactual': mes,
        'citasmes': citasmes,
        'pacientesmesactual':pacientesmesactual,
        'pacientesanio':pacientesanio,
        'citasanio':citasanio,
        'consultasanio':consultasanio,
        'devengadoanio':devengadoanio,
        'totalcitas': totalcitas,
        'totalpacientes': totalpacientes,
        'totaldevengado': totaldevengado,
        'totalconsultas': totalconsultas
    }

    return render(request, 'estadisticas.html', data)



########################### CITAS ##############################################

#VISTA PARA LISTAR CITAS
@login_required
def ListaCitas(request):
    # Semana y año actuales
    semanaactual = datetime.now().isocalendar()[1]
    anoactual = datetime.now().year

    pacientes = Paciente.objects.all().order_by('nombre')

    # Día lunes de la semana actual
    first_day = first_day_of_iso_week(anoactual, semanaactual)
    lunes = first_day.date()

    # Fechas de la semana
    fechalunes = lunes.strftime("%d")
    fechamartes = (lunes + timedelta(days=1)).strftime("%d")
    fechamiercoles = (lunes + timedelta(days=2)).strftime("%d")
    fechajueves = (lunes + timedelta(days=3)).strftime("%d")
    fechaviernes = (lunes + timedelta(days=4)).strftime("%d")
    mes = nombre_mes(lunes.strftime("%m"))
    
    # Conteo de citas de la semana
    conteocitas = Cita.objects.filter(
        fechacita__week=semanaactual,
        fechacita__year=anoactual
    ).count()

    # Horas a mostrar
    horas = [
        (8, "8:00 - 9:00"),
        (9, "9:00 - 10:00"),
        (10, "10:00 - 11:00"),
        (11, "11:00 - 12:00"),
        (13, "1:00 - 2:00"),
        (14, "2:00 - 3:00"),
        (15, "3:00 - 4:00"),
        (16, "4:00 - 5:00"),
        (17, "5:00 - 6:00"),
    ]

    # Construcción de filas de la tabla
    filas = []
    for hora_valor, hora_texto in horas:
        fila = [hora_texto]  # Primer columna: la hora
        for dia_semana in range(2, 7):  # 2=lunes, 6=viernes
            citas = Cita.objects.filter(
                horacita=hora_valor,
                fechacita__week=semanaactual,
                fechacita__week_day=dia_semana,
                fechacita__year=anoactual
            )
            if citas.exists():
                fila.append(citas.first())  # Puedes adaptar si hay múltiples
            else:
                fila.append(2)  # Código para disponible
        filas.append(fila)

    # Combinamos horarios y filas en una sola estructura para el template
    horarios_citas = [(fila[0], fila[1:]) for fila in filas]

    return render(request, 'Citas/citas.html', {
        'fechalunes': fechalunes,
        'fechamartes': fechamartes,
        'fechamiercoles': fechamiercoles,
        'fechajueves': fechajueves,
        'fechaviernes': fechaviernes,
        'conteocitas': conteocitas,
        'mes': mes,
        'semana': semanaactual,
        'horarios_citas': horarios_citas,
        'pacientes':pacientes,
    })

#FUNCION PARA OBTENER LAS CITAS DE LA SEMANA BUSCADA
@login_required
def buscar_semana(request, numano=None,numse=None):
    ####### SEMANA BUSCADA #########
    # Semana y año actuales
    

    pacientes = Paciente.objects.all().order_by('nombre')

    # Día lunes de la semana actual
    first_day = first_day_of_iso_week(numano, numse)
    lunes = first_day.date()

    # Fechas de la semana
    fechalunes = lunes.strftime("%d")
    fechamartes = (lunes + timedelta(days=1)).strftime("%d")
    fechamiercoles = (lunes + timedelta(days=2)).strftime("%d")
    fechajueves = (lunes + timedelta(days=3)).strftime("%d")
    fechaviernes = (lunes + timedelta(days=4)).strftime("%d")
    mes = nombre_mes(lunes.strftime("%m"))
    
    # Conteo de citas de la semana
    conteocitas = Cita.objects.filter(
        fechacita__week=numse,
        fechacita__year=numano
    ).count()

    # Horas a mostrar
    horas = [
        (8, "8:00 - 9:00"),
        (9, "9:00 - 10:00"),
        (10, "10:00 - 11:00"),
        (11, "11:00 - 12:00"),
        (13, "1:00 - 2:00"),
        (14, "2:00 - 3:00"),
        (15, "3:00 - 4:00"),
        (16, "4:00 - 5:00"),
        (17, "5:00 - 6:00"),
    ]

    # Construcción de filas de la tabla
    filas = []
    for hora_valor, hora_texto in horas:
        fila = [hora_texto]  # Primer columna: la hora
        for dia_semana in range(2, 7):  # 2=lunes, 6=viernes
            citas = Cita.objects.filter(
                horacita=hora_valor,
                fechacita__week=numse,
                fechacita__week_day=dia_semana,
                fechacita__year=numano
            )
            if citas.exists():
                fila.append(citas.first())  # Puedes adaptar si hay múltiples
            else:
                fila.append(2)  # Código para disponible
        filas.append(fila)

    # Combinamos horarios y filas en una sola estructura para el template
    horarios_citas = [(fila[0], fila[1:]) for fila in filas]

    return render(request, 'Citas/citas.html', {
        'fechalunes': fechalunes,
        'fechamartes': fechamartes,
        'fechamiercoles': fechamiercoles,
        'fechajueves': fechajueves,
        'fechaviernes': fechaviernes,
        'conteocitas': conteocitas,
        'mes': mes,
        'semana': numse,
        'horarios_citas': horarios_citas,
        'pacientes':pacientes,
    })

#VISTA PARA AGREGAR CITA
@login_required
def crear_cita(request):
    paciente_id = request.GET.get('paciente_id') or request.POST.get('paciente')
    paciente_nombre = request.GET.get('paciente_nombre')
    historial_consultas = []

    paciente_obj = None
    if paciente_id:
        paciente_obj = get_object_or_404(Paciente, idpaciente=paciente_id)
        historial_consultas = Consulta.objects.filter(paciente=paciente_obj).order_by('-fechaconsulta')

    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fechacita']
            hora = form.cleaned_data['horacita']
            cita_existente = Cita.objects.filter(fechacita=fecha, horacita=hora).exists()
            if cita_existente:
                messages.error(request, f"No se puede agendar la cita porque ya esta ocupada la hora.")
                return render(request, 'Citas/form_cita.html', {
                    'form': form,
                    'paciente_id': paciente_id,
                    'paciente_nombre': paciente_nombre,
                    'historial_consultas': historial_consultas
                })
            else:
                messages.success(request, f"Cita agendada correctamente para {paciente_nombre} el {fecha} a las {hora}.")
                form.save()
                return redirect('/citas/')
        else:
            return render(request, 'Citas/form_cita.html', {
                'form': form,
                'paciente_id': paciente_id,
                'paciente_nombre': paciente_nombre,
                'historial_consultas': historial_consultas
            })
    else:
        initial = {}
        if paciente_obj:
            initial['paciente'] = paciente_obj
        form = CitaForm(initial=initial)
        return render(request, 'Citas/form_cita.html', {
            'form': form,
            'paciente_id': paciente_id,
            'paciente_nombre': paciente_nombre,
            'historial_consultas': historial_consultas
        })

#VISTA EDITAR CITA
@login_required
def editar_cita(request, pk=None):
    cita = get_object_or_404(Cita, pk=pk)
    paciente = cita.paciente
    paciente_nombre = paciente.nombre
    historial_consultas = Consulta.objects.filter(paciente=paciente).order_by('-fechaconsulta')

    if request.method == 'GET':
        citaform = CitaForm(instance=cita)
        return render(request, 'Citas/form_cita.html', {
            'form': citaform,
            'paciente_nombre': paciente_nombre,
            'historial_consultas': historial_consultas
        })

    if request.method == 'POST':
        citaform = CitaForm(request.POST, instance=cita)
        if citaform.is_valid():
            fecha = citaform.cleaned_data['fechacita']
            hora = citaform.cleaned_data['horacita']
            existe = Cita.objects.filter(fechacita=fecha, horacita=hora).exclude(pk=cita.pk).exists()
            if existe:
                messages.error(request, f"No se puede editar la cita porque ya esta ocupada la hora.")
                return render(request, 'Citas/form_cita.html', {
                    'form': citaform,
                    'paciente_nombre': paciente_nombre,
                    'historial_consultas': historial_consultas
                })
            else:
                messages.success(request, f"Cita editada correctamente para {paciente_nombre} el {fecha} a las {hora}.")
                citaform.save()
                return redirect('/citas/')
        else:
            return render(request, 'Citas/form_cita.html', {
                'form': citaform,
                'paciente_nombre': paciente_nombre,
                'historial_consultas': historial_consultas
            })

#VISTA ELIMINAR CITAS
@login_required
def eliminar_cita(request, pk=None):
    messages.success(request, f"Cita eliminada correctamente.")
    Cita.objects.filter(pk=pk).delete()
    return redirect('/citas/')

    


########################## PACIENTES ################################################

#VISTA LISTAR PACIENTES
@login_required
def ListaPacientes(request):
    filtro = request.GET.get('filtro', 'nombre')
    buscar = request.GET.get('buscar', '')

    pacientes = Paciente.objects.all().order_by('nombre')

    if buscar:
        buscar = buscar.strip().lower()
        if filtro == 'nombre':
            pacientes = pacientes.filter(nombre__icontains=buscar)
        elif filtro == 'telefono':
            pacientes = pacientes.filter(telefono__icontains=buscar)
        elif filtro == 'sexo':
            if buscar in ['masculino', 'm']:
                pacientes = pacientes.filter(sexo='M')
            elif buscar in ['femenino', 'f']:
                pacientes = pacientes.filter(sexo='F')

    pagina = request.GET.get("page", 1)
    try:
        paginator = Paginator(pacientes, 10)
        pacientes_paginados = paginator.page(pagina)
    except:
        raise Http404("Página no encontrada")

    return render(request, 'Pacientes/pacientes.html', {
        'entity': pacientes_paginados,
        'paginator': paginator,
        'filtro': filtro,
        'buscar': request.GET.get('buscar', '')
    })

#VISTA CREAR PACIENTE
@login_required
def crear_paciente(request):    
    if request.method == 'GET':
        return render(request, 'Pacientes/form_paciente.html', {'form': PacienteForm()})
    
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            nuevo_paciente = form.save()
            # Redireccionar con ID y nombre como parámetros
            messages.success(request, f"Paciente {nuevo_paciente.nombre} creado correctamente.")
            query_params = urlencode({
                'paciente_id': nuevo_paciente.idpaciente,
                'paciente_nombre': nuevo_paciente.nombre
            })
            return redirect(f'/agregarconsulta/?{query_params}')
        
        return render(request, 'Pacientes/form_paciente.html', {'form': form})

#VISTA EDITAR PACIENTE
@login_required
def editar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            messages.success(request, f"Paciente {paciente.nombre} editado correctamente.")
            form.save()
            return redirect('/pacientes/')
    else:
        form = PacienteForm(instance=paciente)

    return render(request, 'Pacientes/form_paciente.html', {'form': form})

#VISTA ELIMINAR PACIENTE
@login_required
def eliminar_paciente(request, pk=None):
    paciente = get_object_or_404(Paciente, pk=pk)

    tiene_consultas = paciente.consulta_set.exists()
    tiene_citas = paciente.cita_set.exists()

    if tiene_consultas or tiene_citas:
        messages.error(request, "No se puede eliminar el paciente porque tiene citas o consultas asociadas.")
        return redirect('/pacientes/')

    paciente.delete()
    messages.success(request, "Paciente eliminado correctamente.")
    return redirect('/pacientes/')

#VISTA PARA MOSTRAR EL HISTORIAL DE PACIENTES
def paciente_historial(request,pk=None):
    conteo = Consulta.objects.filter(paciente__idpaciente=pk).count()
    paciente = Paciente.objects.get(pk=pk)
    consultas = Consulta.objects.filter(paciente__idpaciente=pk).order_by('-fechaconsulta')
    pagina = request.GET.get("page", 1)
    try:
        paginator = Paginator(consultas, 15)
        consultas = paginator.page(pagina)
    except:
        raise Http404
    nombre = paciente.nombre
    data={
        'entity':consultas,
        'nombre':nombre,
        'conteo': conteo,
        'paginator':paginator
    }
    return render(request,'Pacientes/historial.html/',data)

#VISTA PARA MOSTRAR EL HISTORIAL DEL PACIENTE DETALLADO
def paciente_historialid(request,pk=None):
    consult = Consulta.objects.get(idconsulta=pk)
    #receta = Receta.objects.get(consulta__idconsulta=pk)
    data={
        'consulta':consult,
        #'receta':receta
    }
    
    return render(request,'Pacientes/historialid.html/',data)

#VISTA PARA BUSCAR PACIENTES
@login_required
def buscar_paciente(request, name):
    allpacientes = Paciente.objects.all().order_by('nombre')
    pacientes = Paciente.objects.filter(nombre__icontains=name).order_by('nombre')
    if len(pacientes) >= 1:
                pagina = request.GET.get("page", 1)

                try:
                    paginator = Paginator(pacientes, 10)
                    pacientes = paginator.page(pagina)
                except:
                    raise Http404

                data = {
                    'entity': pacientes,
                    'paginator':paginator
                }
                return render(request, 'Pacientes/pacientes.html', data)
    else:
        existe = 1
        pagina = request.GET.get("page", 1)

        try:
            paginator = Paginator(allpacientes, 10)
            allpacientes = paginator.page(pagina)
        except:
            raise Http404

    data = {
        'entity': allpacientes,
        'paginator':paginator,
        'mensaje': existe,
        }    
    return render(request, 'Pacientes/pacientes.html', data)

#VISTA PARA BUSCAR PACIENTES EN INDEX
@login_required
def buscar_paciente_index(request, name):
    
    pacientes = Paciente.objects.filter(nombre__icontains=name).order_by('nombre')
    if len(pacientes) >= 1:
                pagina = request.GET.get("page", 1)

                try:
                    paginator = Paginator(pacientes, 10)
                    pacientes = paginator.page(pagina)
                except:
                    raise Http404

                data = {
                    'entity': pacientes,
                    'paginator':paginator
                }
                
                return render(request, 'Pacientes/pacientes.html', data)
    else:
        mensaje=1
        data = infohome()
        data.update({'mensaje':mensaje})
       
    return render(request, 'index.html', data)



########################### CONSULTAS ###############################################

#VISTA PARA LISTAR CONSULTAS
@login_required
def ListaConsultas(request):
    filtro = request.GET.get('filtro', 'paciente')
    buscar = request.GET.get('buscar', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    pacientes = Paciente.objects.all().order_by('nombre')

    consultas = Consulta.objects.all().order_by('-fechaconsulta')
    # Filtro por búsqueda
    if buscar:
        buscar = buscar.strip().lower()
        if filtro == 'paciente':
            consultas = consultas.filter(paciente__nombre__icontains=buscar)
        elif filtro == 'tipo':
            if buscar in ['lesion', 'lesión']:
                consultas = consultas.filter(tipo__iexact='Lesion')
            elif buscar in ['patologia', 'patología']:
                consultas = consultas.filter(tipo__iexact='Patologia')
        elif filtro == 'precioconsulta':
            try:
                buscar = buscar.replace(',', '.')
                valor = Decimal(buscar)
                # Buscar precios entre valor y valor + 1
                consultas = consultas.filter(precioconsulta__gte=valor, precioconsulta__lt=valor + Decimal('1.00'))
            except (InvalidOperation, ValueError):
                pass

    # Filtro por fechas
    if fecha_inicio:
        try:
            fecha_ini = datetime.strptime(fecha_inicio.strip(), '%Y-%m-%d').date()
            consultas = consultas.filter(fechaconsulta__gte=fecha_ini)
        except (ValueError, TypeError):
            pass

    if fecha_fin:
        try:
            fecha_fin_dt = datetime.strptime(fecha_fin.strip(), '%Y-%m-%d').date()
            consultas = consultas.filter(fechaconsulta__lte=fecha_fin_dt)
        except (ValueError, TypeError):
            pass

    # Paginación
    pagina = request.GET.get("page", 1)
    try:
        paginator = Paginator(consultas, 10)
        consultas_paginadas = paginator.page(pagina)
    except:
        raise Http404("Página no encontrada")

    return render(request, 'Consultas/consultas.html', {
        'entity': consultas_paginadas,
        'paginator': paginator,
        'filtro': filtro,
        'buscar': buscar,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'pacientes':pacientes,
    })

#VISTA PARA AGREGAR CONSULTAS DESDE CREAR PACIENTE
@login_required
def crear_consulta(request):
    paciente_id = request.GET.get('paciente_id') or request.POST.get('paciente')
    paciente_nombre = request.GET.get('paciente_nombre')

    historial_consultas = []

    if paciente_id:
        historial_consultas = Consulta.objects.filter(paciente_id=paciente_id).order_by('-fechaconsulta')
        
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            messages.success(request, f"Consulta creada correctamente para {paciente_nombre}.")
            consulta = form.save()
            return redirect('/consultas/')
    else:
        initial = {}
        if paciente_id:
            initial['paciente'] = paciente_id
        form = ConsultaForm(initial=initial)

    return render(request, 'Consultas/form_consulta.html', {
        'form': form,
        'paciente_nombre': paciente_nombre,
        'historial_consultas': historial_consultas
    })

#VISTA EDITAR COSULTAS
@login_required
def editar_consulta(request, pk=None):
    consulta = Consulta.objects.get(pk=pk)
    historial_consultas = Consulta.objects.filter(paciente=consulta.paciente).order_by('-fechaconsulta')
    paciente_nombre = request.GET.get('paciente_nombre', consulta.paciente.nombre)
    if request.method == 'GET':
        consultaform = ConsultaForm(instance=consulta)

        return render(
            request,
            'Consultas/form_consulta.html',
            {   
                'paciente_nombre': paciente_nombre,
                'consulta': consulta,
                'form': consultaform,
                'historial_consultas': historial_consultas,  # Aseguramos pasar el historial
            }
        )
    if request.method == 'POST':
        consultaform = ConsultaForm(
            data=request.POST,
            instance=consulta
        )
        if consultaform.is_valid():
            messages.success(request, f"Consulta editada correctamente para {paciente_nombre}.")
            consultaform.save()
            return redirect('/consultas/')
        else:
            return render(
                request,
                'Consultas/form_consulta.html',
                {'form': consultaform, 
                 'historial_consultas': historial_consultas,
                 'paciente_nombre': paciente_nombre,}
            )

#VISTA ELIMINAR CONSULTAS
@login_required
def eliminar_consulta(request, pk=None):
    consulta = get_object_or_404(Consulta, pk=pk)
    consulta.delete()
    messages.success(request, "Consulta eliminada correctamente.")
    return redirect('/consultas/')

#VISTA PARA BUSCAR CONSULTA
@login_required
def buscar_consulta(request, name=None):
    allconsultas = Consulta.objects.all().order_by('-idconsulta')
    consultas = Consulta.objects.filter(paciente__nombre__icontains=name)
    if len(consultas) >= 1:
                pagina = request.GET.get("page", 1)

                try:
                    paginator = Paginator(consultas, 10)
                    consultas = paginator.page(pagina)
                except:
                    raise Http404

                data = {
                    'entity': consultas,
                    'paginator':paginator

                }
            
                return render(request, 'Consultas/consultas.html', data)
    else:
        existe = 1
        pagina = request.GET.get("page", 1)

        try:
            paginator = Paginator(allconsultas, 10)
            allconsultas = paginator.page(pagina)
        except:
            raise Http404

    data = {
        'entity': allconsultas,
        'paginator':paginator,
        'mensaje': existe,
        }    
    return render(request, 'Consultas/consultas.html', data)



########################### RECETAS ###############################################

#VISTA PARA LISTAR RECETAS
@login_required
def ListaRecetas(request):
    recetas = Receta.objects.all().order_by('-idreceta')
    pagina = request.GET.get("page", 1)

    try:
        paginator = Paginator(recetas, 10)
        recetas = paginator.page(pagina)
    except:
        raise Http404

    data = {
        'entity': recetas,
        'paginator':paginator
    }
    return render(request,  'Recetas/recetas.html',data )

#VISTA PARA AGREGAR CONSULTAS
@login_required
def crear_receta(request):
    consulta_id = request.GET.get('consulta_id')
    paciente_nombre = request.GET.get('paciente_nombre')

    if request.method == 'POST':
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.consulta_id = consulta_id  # Asignamos la consulta relacionada
            receta.save()
            return redirect('/recetas/')  # o a donde desees
    else:
        form = RecetaForm()

    return render(request, 'Recetas/crear_receta.html', {
        'RecetaForm': form,
        'paciente_nombre': paciente_nombre
    })
        
#VISTA EDITAR RECETA
@login_required
def editar_receta(request, pk=None):
    receta = Receta.objects.get(pk=pk)

    if request.method == 'GET':
        recetaform=RecetaForm(instance=receta)

        return render(
            request,
            'Recetas/actualizar_receta.html',
            {
                'receta': receta, 
                'recetaform':recetaform
            }
        )
    if request.method == 'POST':
        recetaform=RecetaForm(
            data=request.POST,
            instance=receta
        )
        if recetaform.is_valid():
            recetaform.save()
            return redirect('/recetas/')
        else:
            recetaform=RecetaForm(
            data=request.POST,
            instance=receta
        )
        return render(
            request,
            'Recetas/crear_receta.html',
            {'RecetaForm': recetaform}
        )
    
#VISTA ELIMINAR RECETA
@login_required
def eliminar_receta(request, pk=None):
    Receta.objects.filter(pk=pk).delete()
    return redirect('/recetas/')

#VISTA PARA BUSCAR RECETA
@login_required
def buscar_receta(request, name=None):
    allrecetas = Receta.objects.all().order_by('fechareceta')
    recetas = Receta.objects.filter(consulta__paciente__nombre__icontains=name)
    if len(recetas) >= 1:
                pagina = request.GET.get("page", 1)

                try:
                    paginator = Paginator(recetas, 10)
                    recetas = paginator.page(pagina)
                except:
                    raise Http404

                data = {
                    'entity': recetas,
                    'paginator':paginator

                }
            
                return render(request, 'Recetas/recetas.html', data)
    else:
        existe = 1
        pagina = request.GET.get("page", 1)

        try:
            paginator = Paginator(allrecetas, 10)
            allrecetas = paginator.page(pagina)
        except:
            raise Http404

    data = {
        'entity': allrecetas,
        'paginator':paginator,
        'mensaje': existe,
        }    
    return render(request, 'Recetas/recetas.html', data)

#LISTVIEW PARA EXPORTAR RECETA A PDF
class imprimirreceta(View):

    def get(self, request,pk, *args, **kwargs):
        receta = Receta.objects.get(idreceta = pk)
        data = {
            
            'receta': receta
        }
        pdf = render_to_pdf('recetas/imprimirreceta.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
