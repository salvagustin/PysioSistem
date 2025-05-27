from django.db import models
import datetime

horayfecha = datetime.datetime.now()
semanaactual = horayfecha.isocalendar().week

# Create your models here.
class Paciente(models.Model):
    idpaciente = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre', max_length=300)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', null = False)
    fechacreacion = models.DateField('Fecha de creacion', auto_now=True, auto_now_add=False)
    telefono = models.PositiveIntegerField('Telefono')
    Opciones = (("M", "Masculino"), ("F", "Femenino"))
    sexo =  models.CharField('Sexo', max_length=1, choices=Opciones, blank=False, null=False)

    def __str__(self):
        return f"{self.nombre}"



class Consulta(models.Model):
    idconsulta = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, blank=False, null=False)
    fechaconsulta = models.DateField('Fecha de consulta', auto_now_add=True)
    horaconsulta = models.TimeField('Hora consulta', auto_now=True, auto_now_add=False)
    precioconsulta = models.DecimalField('Precio', max_digits=10, decimal_places=2, blank=False, null=False)
    opciones = (("Lesion", "Lesion"), ("Patologia", "Patologia"))
    tipo =  models.CharField('Tipo', max_length=9, choices=opciones, blank=False, null=False)
    observaciones = models.CharField('Observaciones', max_length=500)
   
    
    def __str__(self):
        return f"{self.idconsulta} {self.paciente.nombre}"
    
#class Ejercicio(models.Model):
 #   idejercicio = models.AutoField(primary_key=True)
 #categoria
 #subcategoria
  #  nombre = models.CharField('Nombre', max_length=300)
   # semana = models.PositiveIntegerField('Semana')
    #descripcion = models.CharField('Descripcion', max_length=300)
    # Imagen
    # Video
    # lesion o patologia
    # subir pdf

class Receta(models.Model):
    idreceta = models.AutoField(primary_key=True)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, blank=False, null=False)
    fechareceta = models.DateField('Fecha de receta', auto_now=True, auto_now_add=False)
    medicamento = models.CharField('Medicamento', max_length=500)
    dosis = models.CharField('Dosis', max_length=500)
    duracion = models.PositiveIntegerField('Duracion')
    indicaciones = models.CharField('Indicaciones', max_length=500)
    def __str__(self):
        return f"{self.idreceta} {self.consulta.paciente.nombre}"

class Cita(models.Model):
    idcita = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, blank=False, null=False)
    fechacita = models.DateField('Fecha de cita')
    opciones = (("8", "8:00 - 9:00"), ("9", "9:00 - 10:00"),("10", "10:00 - 11:00"),("11", "11:00 - 12:00"),
                ("13", "01:00 - 02:00"),("14", "02:00 - 03:00"),("15", "03:00 - 04:00"),("16", "04:00 - 05:00"),("17", "05:00 - 06:00"))
    horacita =  models.CharField('Hora cita', max_length=11, choices=opciones, blank=False, null=False)
    observaciones = models.CharField('Observaciones', max_length=500)


