from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from gestor.models import *
from gestor.forms import *
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import logout
from django.db.models import Sum,Count, IntegerField
from django.db.models.functions import ExtractMonth, Cast
from django.db.models.expressions import RawSQL
from django.views.generic import View
from datetime import timedelta, date
from urllib.parse import urlencode
from .utils import render_to_pdf
from django.utils import timezone
import datetime
import json
from datetime import datetime, timedelta, date
from decimal import Decimal, InvalidOperation


#OBTENER FECHA ACTUAL Y FORMATEAR SEMANA Y MES ACTUALES
horayfecha = datetime.now()
horaactual = horayfecha.hour
semanaactual = horayfecha.isocalendar().week
anoactual = horayfecha.isocalendar().year
mesactualnumero = horayfecha.strftime("%m").capitalize()

grupos_permitidos = ['administrador', 'doctor', 'nutricionista', 'fisioterapeuta']



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

def infohome(request):
    hoy = date.today()
    user = request.user

    citas = Cita.objects.none()
    consultas = Consulta.objects.none()

    # Verificamos a qué grupo pertenece el usuario
    grupos = user.groups.values_list('name', flat=True)

    if 'administrador' in grupos:
        # Admin ve todo
        citas = Cita.objects.filter(fechacita=hoy)
        consultas = Consulta.objects.filter(fechaconsulta=hoy)

    elif 'doctor' in grupos or 'fisioterapeuta' in grupos or 'nutricionista' in grupos:
        try:
            doctor = Doctor.objects.get(usuario=user)
        except Doctor.DoesNotExist:
            doctor = None

        if doctor:
            citas = Cita.objects.filter(fechacita=hoy, doctor=doctor)
            consultas = Consulta.objects.filter(fechaconsulta=hoy, doctor=doctor)

    consultasdiarias = consultas.count()
    devengadodiario = consultas.aggregate(Sum('precioconsulta')).get('precioconsulta__sum') or 0

    pacientes = Paciente.objects.all()  # Pacientes visibles para todos

    # Tabla de horarios
    horario = {
        'matutino': {8: '', 9: '', 10: '', 11: ''},
        'vespertino': {13: '', 14: '', 15: '', 16: '', 17: ''}
    }

    for cita in citas:
        hora = cita.horacita
        if hora in horario['matutino']:
            horario['matutino'][hora] = cita.paciente.nombre
        elif hora in horario['vespertino']:
            horario['vespertino'][hora] = cita.paciente.nombre

    return {
        'proximacita': citas,
        'citashoy': citas.count(),
        'consultashoy': consultasdiarias,
        'devengadohoy': devengadodiario,
        'pacientes': pacientes,
        'horario': horario,
        'mensaje': 0
    }

@login_required
def inicio(request):
    user = request.user

    # Si es cliente, redirigir a su home
    if user.groups.filter(name='cliente').exists():
        return render(request, 'clientes/home.html')

    elif user.groups.filter(name='administrador').exists():
       
       return render(request, 'administrador.html')

    # Para otros grupos (doctor, admin, fisio, nutri) cargamos el index con datos personalizados
    data = infohome(request)
    return render(request, 'index.html', data)

@login_required
def salir(request):
    logout(request)
    return redirect('login.html')

####### FUNCION PARA CALCULAR LA EDAD DE LOS PACIENTES #####
def calcular_edad(fecha_nacimiento):
    hoy = date.today()
    return hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))


#################### ESTADISTICAS ###################################
@login_required
def estadisticas(request):
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
    hoy = date.today()
    year_actual = hoy.year
    mes_actual = hoy.month
    
    # Datos para las tarjetas resumen (mantén tu lógica existente)
    consultasmes = Consulta.objects.filter(fechaconsulta__month=mes_actual, fechaconsulta__year=year_actual).count()
    citasmes = Cita.objects.filter(fechacita__month=mes_actual, fechacita__year=year_actual).count()
    pacientesmesactual = Paciente.objects.filter(fechacreacion__month=mes_actual, fechacreacion__year=year_actual).count()
    devengadomes = Consulta.objects.filter(fechaconsulta__month=mes_actual, fechaconsulta__year=year_actual).aggregate(Sum('precioconsulta')).get('precioconsulta__sum') or 0
    
    consultasanio = Consulta.objects.filter(fechaconsulta__year=year_actual).count()
    citasanio = Cita.objects.filter(fechacita__year=year_actual).count()
    pacientesanio = Paciente.objects.filter(fechacreacion__year=year_actual).count()
    devengadoanio = Consulta.objects.filter(fechaconsulta__year=year_actual).aggregate(Sum('precioconsulta')).get('precioconsulta__sum') or 0
    
    totalconsultas = Consulta.objects.count()
    totalcitas = Cita.objects.count()
    totalpacientes = Paciente.objects.count()
    totaldevengado = Consulta.objects.aggregate(Sum('precioconsulta')).get('precioconsulta__sum') or 0
    
    # DATOS PARA GRÁFICOS
    
    # 1. Conteo de consultas por mes
    conteoconsultas = []
    for i in range(1, 13):
        consulta = Consulta.objects.filter(fechaconsulta__month=i, fechaconsulta__year=year_actual).count()
        conteoconsultas.append(consulta)
    
    # 2. Ganancias por mes
    consultatotal = []
    for i in range(1, 13):
        sumadevengado = Consulta.objects.filter(fechaconsulta__month=i, fechaconsulta__year=year_actual).aggregate(Sum('precioconsulta')).get('precioconsulta__sum')
        if sumadevengado == None:
            sumadevengado = 0 
        consultatotal.append(float(sumadevengado))
    
    # 3. Datos para gráfico combinado (home)
    consulta_por_mes = (Consulta.objects.filter(fechaconsulta__year=year_actual).annotate(mes=ExtractMonth('fechaconsulta')).values('mes').annotate(
                        total_ganancias=Sum('precioconsulta'), total_consultas=Count('idconsulta')))
    
    paciente_por_mes = (Paciente.objects.filter(fechacreacion__year=year_actual).annotate(mes=ExtractMonth('fechacreacion')).values('mes')
                        .annotate(total_pacientes=Count('idpaciente')))
    
    consultatotal_home = [0] * 12
    conteoconsultas_home = [0] * 12
    conteopacientes = [0] * 12
    
    for c in consulta_por_mes:
        index = c['mes'] - 1
        consultatotal_home[index] = float(c['total_ganancias'] or 0)
        conteoconsultas_home[index] = int(c['total_consultas'])
    
    for p in paciente_por_mes:
        index = p['mes'] - 1
        conteopacientes[index] = int(p['total_pacientes'])
    
    # 4. Rangos de edad de pacientes
    pacientes = Paciente.objects.all()
    rango_edad = {
        '1-10 años': 0,
        '11-18 años': 0,
        '19-30 años': 0,
        '31-45 años': 0,
        '46-60 años': 0,
        'Más de 60 años': 0
    }
    
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
    
    # 5. Top 5 pacientes con más consultas
    top_pacientes = (
        Consulta.objects.values('paciente__nombre')
        .annotate(total=Count('paciente__idpaciente'))
        .order_by('-total')[:5]
    )
    
    nombres_top = [p['paciente__nombre'] for p in top_pacientes]
    cantidades_top = [p['total'] for p in top_pacientes]
    
    # Meses para los gráficos
    meses = ["En", "Feb", "Mar", "Ab", "May", "Jun", "Jul", "Ago", "Sept", "Oct", "Nov", "Dic"]
    
    context = {
        # Datos de tarjetas resumen
        'mesactual': hoy.strftime('%B'),
        'year': year_actual,
        'consultasmes': consultasmes,
        'citasmes': citasmes,
        'pacientesmesactual': pacientesmesactual,
        'devengadomes': devengadomes,
        'consultasanio': consultasanio,
        'citasanio': citasanio,
        'pacientesanio': pacientesanio,
        'devengadoanio': devengadoanio,
        'totalconsultas': totalconsultas,
        'totalcitas': totalcitas,
        'totalpacientes': totalpacientes,
        'totaldevengado': totaldevengado,
        
        # Datos para gráficos
        'meses': meses,
        'conteoconsultas': conteoconsultas,
        'consultatotal': consultatotal,
        'consultatotal_home': consultatotal_home,
        'conteoconsultas_home': conteoconsultas_home,
        'conteopacientes': conteopacientes,
        'rango_edad': rango_edad,
        'nombres_top': nombres_top,
        'cantidades_top': cantidades_top,
    }
    
    return render(request, 'estadisticas.html', context)



########################### CITAS ##############################################

#VISTA PARA LISTAR CITAS
@login_required
def ListaCitas(request):
    
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')

    # Intentar encontrar al profesional vinculado a este usuario
    doctor_actual = Doctor.objects.filter(usuario=request.user).first()

    semanaactual = datetime.now().isocalendar()[1]
    anoactual = datetime.now().year
    pacientes = Paciente.objects.all().order_by('nombre')

    first_day = first_day_of_iso_week(anoactual, semanaactual)
    lunes = first_day.date()

    fechalunes = lunes.strftime("%d")
    fechamartes = (lunes + timedelta(days=1)).strftime("%d")
    fechamiercoles = (lunes + timedelta(days=2)).strftime("%d")
    fechajueves = (lunes + timedelta(days=3)).strftime("%d")
    fechaviernes = (lunes + timedelta(days=4)).strftime("%d")
    mes = nombre_mes(lunes.strftime("%m"))

    # Base query: filtrar por doctor si no es administrador
    base_query = Cita.objects.filter(
        fechacita__week=semanaactual,
        fechacita__year=anoactual
    )
    if not request.user.groups.filter(name='administrador').exists():
        base_query = base_query.filter(doctor=doctor_actual)

    conteocitas = base_query.count()

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

    filas = []
    for hora_valor, hora_texto in horas:
        fila = [hora_texto]
        for dia_semana in range(2, 7):  # lunes a viernes
            citas_dia = base_query.filter(
                horacita=hora_valor,
                fechacita__week_day=dia_semana
            )
            if citas_dia.exists():
                fila.append(citas_dia.first())
            else:
                fila.append(2)  # Disponible
        filas.append(fila)

    horarios_citas = [(fila[0], fila[1:]) for fila in filas]

    citas = Cita.objects.all().order_by('-fechacita', 'horacita')
    if not request.user.groups.filter(name='administrador').exists():
        citas = citas.filter(doctor=doctor_actual)

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
        'pacientes': pacientes,
        'citas': citas,
    })

#FUNCION PARA OBTENER LAS CITAS DE LA SEMANA BUSCADA
@login_required
def buscar_semana(request, numano=None,numse=None):
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
    ####### SEMANA BUSCADA #########
    # Semana y año actuales
    
     # Intentar encontrar al profesional vinculado a este usuario
    doctor_actual = Doctor.objects.filter(usuario=request.user).first()
    
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
        fechacita__year=numano,
        doctor=doctor_actual
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
                fechacita__year=numano,
                doctor=doctor_actual
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
    grupos_permitidos = ['administrador', 'doctor', 'nutricionista', 'fisioterapeuta']
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')

    paciente_id = request.GET.get('paciente_id') or request.POST.get('paciente')
    paciente_nombre = request.GET.get('paciente_nombre')
    historial_consultas = []
    paciente_obj = None

    if paciente_id:
        paciente_obj = get_object_or_404(Paciente, idpaciente=paciente_id)
        historial_consultas = Consulta.objects.filter(paciente=paciente_obj).order_by('-fechaconsulta')

    # Detectamos si es admin y obtenemos el doctor logueado si existe
    es_admin = request.user.groups.filter(name='administrador').exists()
    doctor_actual = Doctor.objects.filter(usuario=request.user).first()

    if request.method == 'POST':
        # Copiamos los datos para modificar si no es admin
        data_mutable = request.POST.copy()
        if not es_admin and doctor_actual:
            data_mutable['doctor'] = doctor_actual.pk

        form = CitaForm(data_mutable, es_admin=es_admin)

        if form.is_valid():
            cita = form.save(commit=False)

            # Forzamos doctor si no es admin
            if not es_admin and doctor_actual:
                cita.doctor = doctor_actual

            # Verificar si existe una cita en ese horario con ese doctor
            if Cita.objects.filter(fechacita=cita.fechacita, horacita=cita.horacita, doctor=cita.doctor).exists():
                messages.error(request, f"No se puede agendar la cita porque ya está ocupada la hora.")
            else:
                cita.save()
                messages.success(request, f"Cita agendada correctamente para {paciente_nombre} el {cita.fechacita} a las {cita.horacita}.")
                return redirect('/citas/')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        initial = {}
        if paciente_obj:
            initial['paciente'] = paciente_obj
        form = CitaForm(initial=initial, es_admin=es_admin)

    return render(request, 'Citas/form_cita.html', {
        'form': form,
        'paciente_id': paciente_id,
        'paciente_nombre': paciente_nombre,
        'historial_consultas': historial_consultas
    })

#VISTA EDITAR CITA
@login_required
def editar_cita(request, pk=None):
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
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
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
    messages.success(request, f"Cita eliminada correctamente.")
    Cita.objects.filter(pk=pk).delete()
    return redirect('/citas/')

########################## PACIENTES  ################################################

#VISTA LISTAR PACIENTES
@login_required
def ListaPacientes(request):
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
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
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
    if request.method == 'GET':
        return render(request, 'Pacientes/form_paciente.html', {'form': PacienteForm()})
    
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            nuevo_paciente = form.save()
            
            # Verificar qué botón fue presionado
            if 'btn_consulta' in request.POST:
                # Si presionó el botón de consulta, redirigir a agregar consulta
                messages.success(request, f"Paciente {nuevo_paciente.nombre} creado correctamente.")
                query_params = urlencode({
                    'paciente_id': nuevo_paciente.idpaciente,
                    'paciente_nombre': nuevo_paciente.nombre
                })
                return redirect(f'/agregarconsulta/?{query_params}')
            else:
                # Si presionó guardar o actualizar, redirigir a la lista de pacientes
                messages.success(request, f"Paciente {nuevo_paciente.nombre} guardado correctamente.")
                return redirect('ListaPacientes')
        
        return render(request, 'Pacientes/form_paciente.html', {'form': form})

#VISTA EDITAR PACIENTE 
@login_required
def editar_paciente(request, pk):
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
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
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
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
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
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
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
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
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
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
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
    name = name.strip()
    if not name:
        return redirect('inicio')

    pacientes = Paciente.objects.filter(nombre__icontains=name).order_by('nombre')

    if pacientes.exists():
        paginator = Paginator(pacientes, 10)
        page = request.GET.get("page", 1)

        try:
            pacientes_page = paginator.page(page)
        except:
            raise Http404("Página no encontrada")

        return render(request, 'Pacientes/pacientes.html', {
            'entity': pacientes_page,
            'paginator': paginator
        })
    else:
        messages.error(request, f"No se encontraron pacientes con el nombre: {name}")
        data = infohome()
        return render(request, 'index.html', data)


########################### DOCTORES ###############################################

# VISTA LISTAR DOCTORES
@login_required
def lista_doctores(request):
    if not request.user.groups.filter(name='administrador').exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')

    filtro = request.GET.get('filtro', 'nombre')
    buscar = request.GET.get('buscar', '')

    doctores = Doctor.objects.all().order_by('nombre')

    if buscar:
        buscar = buscar.strip().lower()
        if filtro == 'nombre':
            doctores = doctores.filter(nombre__icontains=buscar)
        elif filtro == 'usuario':
            doctores = doctores.filter(usuario__username__icontains=buscar)

    pagina = request.GET.get("page", 1)
    try:
        paginator = Paginator(doctores, 10)
        doctores_paginados = paginator.page(pagina)
    except:
        raise Http404("Página no encontrada")

    return render(request, 'Doctores/doctores.html', {
        'entity': doctores_paginados,
        'paginator': paginator,
        'filtro': filtro,
        'buscar': buscar
    })

# VISTA CREAR DOCTOR
@login_required
def crear_doctor(request):
    if not request.user.groups.filter(name='administrador').exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')

    if request.method == 'GET':
        return render(request, 'Doctores/form_doctor.html', {'form': DoctorForm()})

    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            nuevo_doctor = form.save()
            messages.success(request, f"Doctor {nuevo_doctor.nombre} creado correctamente.")
            return redirect('lista_doctores')
        return render(request, 'Doctores/form_doctor.html', {'form': form})

# VISTA EDITAR DOCTOR
@login_required
def editar_doctor(request, pk):
    if not request.user.groups.filter(name='administrador').exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')

    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, f"Doctor {doctor.nombre} editado correctamente.")
            return redirect('lista_doctores')
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'Doctores/form_doctor.html', {'form': form})

# VISTA ELIMINAR DOCTOR
@login_required
def eliminar_doctor(request, pk):
    if not request.user.groups.filter(name='administrador').exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')

    doctor = get_object_or_404(Doctor, pk=pk)
    nombre = doctor.nombre
    doctor.delete()
    messages.success(request, f"Doctor {nombre} eliminado correctamente.")
    return redirect('lista_doctores')

########################### CONSULTAS ###############################################

#VISTA PARA LISTAR CONSULTAS
@login_required
def ListaConsultas(request):
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')

    filtro = request.GET.get('filtro', 'paciente')
    buscar = request.GET.get('buscar', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    pacientes = Paciente.objects.all().order_by('nombre')

    # Si el usuario pertenece al grupo administrador ve todas las consultas
    if request.user.groups.filter(name='administrador').exists():
        consultas = Consulta.objects.all().order_by('-fechaconsulta')
    else:
        # Buscar al doctor asociado al usuario
        doctor_actual = Doctor.objects.filter(usuario=request.user).first()
        consultas = Consulta.objects.filter(doctor=doctor_actual).order_by('-fechaconsulta')

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
                consultas = consultas.filter(precioconsulta__gte=valor,
                                             precioconsulta__lt=valor + Decimal('1.00'))
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
    paginator = Paginator(consultas, 10)
    try:
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
        'pacientes': pacientes,
    })

#VISTA PARA AGREGAR CONSULTAS DESDE CREAR PACIENTE
@login_required
def crear_consulta(request):
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')

    paciente_id = request.GET.get('paciente_id') or request.POST.get('paciente')
    paciente_nombre = request.GET.get('paciente_nombre')
    historial_consultas = []

    if paciente_id:
        historial_consultas = Consulta.objects.filter(
            paciente_id=paciente_id
        ).order_by('-fechaconsulta')

    # Saber si es admin y obtener el doctor logeado si existe
    es_admin = request.user.groups.filter(name='administrador').exists()
    doctor_actual = Doctor.objects.filter(usuario=request.user).first()

    if request.method == 'POST':
        form = ConsultaForm(request.POST, es_admin=es_admin)

        # Forzamos doctor si el usuario no es admin antes de validar
        if not es_admin and doctor_actual:
            # Hacemos mutable el QueryDict
            data_mutable = request.POST.copy()
            data_mutable['doctor'] = doctor_actual.pk
            form = ConsultaForm(data_mutable, es_admin=es_admin)

        if form.is_valid():
            consulta = form.save(commit=False)

            # Si no es admin, aseguramos que el doctor quede asignado
            if not es_admin and doctor_actual:
                consulta.doctor = doctor_actual

            consulta.save()
            messages.success(request, f"Consulta creada correctamente para {paciente_nombre}.")
            return redirect('/consultas/')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        initial = {}
        if paciente_id:
            initial['paciente'] = paciente_id
        form = ConsultaForm(initial=initial, es_admin=es_admin)

    return render(request, 'Consultas/form_consulta.html', {
        'form': form,
        'paciente_nombre': paciente_nombre,
        'historial_consultas': historial_consultas
    })

#VISTA EDITAR COSULTAS
@login_required
def editar_consulta(request, pk=None):
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
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
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
    consulta = get_object_or_404(Consulta, pk=pk)
    consulta.delete()
    messages.success(request, "Consulta eliminada correctamente.")
    return redirect('/consultas/')

#VISTA PARA BUSCAR CONSULTA
@login_required
def buscar_consulta(request, name=None):
    if not request.user.groups.filter(name__in=grupos_permitidos).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
    allconsultas = Consulta.objects.all().order_by('-idconsulta')
    
    # Intentar encontrar al profesional vinculado a este usuario
    doctor_actual = Doctor.objects.filter(usuario=request.user).first()

    consultas = Consulta.objects.filter(paciente__nombre__icontains=name,doctor=doctor_actual)
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
        mensaje = messages.error(request, "No se encontraron consultas para el paciente buscado.")
        pagina = request.GET.get("page", 1)

        try:
            paginator = Paginator(allconsultas, 10)
            allconsultas = paginator.page(pagina)
        except:
            raise Http404

    data = {
        'entity': allconsultas,
        'paginator':paginator,
        'mensaje': mensaje,
        }    
    return render(request, 'Consultas/consultas.html', data)



########################### RECETAS ###############################################

#VISTA PARA LISTAR RECETAS
@login_required
def ListaRecetas(request):
    if not request.user.groups.filter(name='administrador').exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
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
    if not request.user.groups.filter(name='administrador').exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
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
    if not request.user.groups.filter(name='administrador').exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
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
    if not request.user.groups.filter(name='administrador').exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
    Receta.objects.filter(pk=pk).delete()
    return redirect('/recetas/')

#VISTA PARA BUSCAR RECETA
@login_required
def buscar_receta(request, name=None):
    if not request.user.groups.filter(name='administrador').exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
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

grupos_permitidoss = ['administrador', 'fisioterapeuta']
#VISTA PARA LISTAR EJERCICIOS
@login_required
def ListaEjercicios(request):
   
    if not request.user.groups.filter(name__in=grupos_permitidoss).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
    ejercicios = Ejercicio.objects.all().order_by('nombre')
    pagina = request.GET.get("page", 1)

    try:
        paginator = Paginator(ejercicios, 10)
        ejercicios = paginator.page(pagina)
    except:
        raise Http404

    data = {
        'entity': ejercicios,
        'paginator':paginator
    }
    return render(request,  'Ejercicios/ejercicios.html',data )


#VISTA PARA AGREGAR EJERCICIO
@login_required
def crear_ejercicio(request):
    if not request.user.groups.filter(name__in=grupos_permitidoss).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
    if request.method == 'POST':
        ejercicio_form = EjercicioForm(request.POST, request.FILES)
        imagenes = request.FILES.getlist('imagenes')

        if ejercicio_form.is_valid():
            ejercicio = ejercicio_form.save()
            for img in imagenes:
                ImagenEjercicio.objects.create(ejercicio=ejercicio, imagen=img)
            messages.success(request, "Ejercicio creado correctamente.")
            return redirect('ListaEjercicios')
        else:
            messages.error(request, "Error al crear el ejercicio. Por favor, revisa los datos ingresados.")
    else:
        ejercicio_form = EjercicioForm()

    return render(request, 'ejercicios/form_ejercicio.html', {
        'form': ejercicio_form,
    })

# VISTA EDITAR EJERCICIO
@login_required
def editar_ejercicio(request, pk):
    if not request.user.groups.filter(name__in=grupos_permitidoss).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    imagenes_json = [
    {"id": img.id, "url": img.imagen.url}
    for img in ejercicio.imagenes.all()
    ]

    if request.method == 'POST':
        ejercicio_form = EjercicioForm(request.POST, request.FILES, instance=ejercicio)
        nuevas_imagenes = request.FILES.getlist('imagenes')

        if ejercicio_form.is_valid():
            ejercicio = ejercicio_form.save()
            for img in nuevas_imagenes:
                ImagenEjercicio.objects.create(ejercicio=ejercicio, imagen=img)
            messages.success(request, f"Ejercicio '{ejercicio.nombre}' editado correctamente.")
            return redirect('ListaEjercicios')
        else:
            messages.error(request, "Error al editar el ejercicio. Revisa los datos ingresados.")
    else:
        ejercicio_form = EjercicioForm(instance=ejercicio)

    return render(request, 'ejercicios/form_ejercicio.html', {
        'form': ejercicio_form,
    })

# VISTA ELIMINAR EJERCICIO
@login_required
@require_POST
def eliminar_ejercicio(request, pk):
    if not request.user.groups.filter(name__in=grupos_permitidoss).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    ejercicio.delete()
    messages.success(request, f"Ejercicio '{ejercicio.nombre}' eliminado correctamente.")
    return redirect('ListaEjercicios')

# VISTA ELIMINAR IMAGEN DE EJERCICIO
@csrf_exempt
def eliminar_imagen(request, imagen_id):
    if not request.user.groups.filter(name__in=grupos_permitidoss).exists():
        messages.error(request, "No tienes permiso.")
        return render(request, 'clientes/home.html')

    if request.method == 'DELETE':
        try:
            imagen = ImagenEjercicio.objects.get(id=imagen_id)
            imagen.delete()
            return JsonResponse({'ok': True})
        except ImagenEjercicio.DoesNotExist:
            return JsonResponse({'error': 'Imagen no encontrada'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


################### CLIENTES ########################################

# VISTA DE INICIO DE CLIENTES

def home_cliente(request):
    return render(request, 'clientes/home.html')

@login_required
def agendar_cita(request):
    try:
        paciente = Paciente.objects.get(usuario=request.user)
    except Paciente.DoesNotExist:
        paciente = None

    cita_actual = None
    puede_agendar = True

    if paciente:
        ahora = timezone.localtime()
        hoy = ahora.date()

        citas_futuras = Cita.objects.filter(
            paciente=paciente,
            fechacita__gte=hoy
        ).order_by('fechacita', 'horacita')

        for cita in citas_futuras:
            cita_hora = timezone.make_aware(
                timezone.datetime.combine(cita.fechacita, timezone.datetime.min.time()).replace(hour=cita.horacita),
                timezone.get_current_timezone()
            )
            if cita_hora > ahora:
                cita_actual = cita
                puede_agendar = False
                break

    if request.method == 'POST' and paciente and puede_agendar:
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.paciente = paciente

            # Validar fechas pasadas y horas pasadas desde la vista
            hoy = timezone.localtime().date()
            ahora = timezone.localtime().time()
            print(hoy)
            print(ahora)
            if cita.fechacita < hoy:
                print(cita.fechacita)
                messages.error(request, "No puedes agendar citas en fechas pasadas.")
            else:
                hora_cita = time(cita.horacita, 0)
                if cita.fechacita == hoy and ahora >= hora_cita:
                    messages.error(request, "No puedes agendar citas para horas que ya pasaron hoy.")
                elif Cita.objects.filter(fechacita=cita.fechacita, horacita=cita.horacita).exists():
                    messages.error(request, "Ya existe una cita para ese día y hora.")
                else:
                    cita.save()
                    messages.success(request, "Cita agendada correctamente.")
                    return redirect('agendar_cita')
    else:
        form = CitaForm(initial={'paciente': paciente})

    return render(request, 'Clientes/cita.html', {
        'form': form,
        'cita_actual': cita_actual,
        'paciente': paciente,
        'puede_agendar': puede_agendar,
    })

@login_required
def ejercicios_cliente(request):
    categorias = Ejercicio.objects.values_list('categoria', flat=True).distinct()
    return render(request, 'clientes/ejercicios.html', {'categorias': categorias})

@login_required
def api_subcategorias(request):
    categoria = request.GET.get('categoria')
    subcategorias = Ejercicio.objects.filter(categoria=categoria).values_list('subcategoria', flat=True).distinct()
    semanas = Ejercicio.objects.filter(categoria=categoria).values_list('semana', flat=True).distinct()
    return JsonResponse({'subcategorias': list(subcategorias), 'semanas': list(semanas)})

@login_required
def api_ejercicios(request):
    categoria = request.GET.get('categoria')
    subcategoria = request.GET.get('subcategoria')
    semana = request.GET.get('semana')
    ejercicios = Ejercicio.objects.filter(categoria=categoria, subcategoria=subcategoria, semana=semana)
    data = []
    for e in ejercicios:
        imagenes = [img.imagen.url for img in e.imagenes.all()]
        data.append({
            'nombre': e.nombre,
            'descripcion': e.descripcion,
            'pdf': e.pdf.url if e.pdf else '',
            'imagenes': imagenes
        })
        print(data)
    return JsonResponse({'ejercicios': data})