from django import forms
from gestor.models import *
from django.contrib.auth.models import User, Group
from datetime import datetime, time, date
from django.core.exceptions import ValidationError




class DateInput(forms.DateInput):
    input_type = 'date'

class PacienteForm(forms.ModelForm):
    usuario_display = forms.CharField(
        label='Usuario',
        required=False,
        widget=forms.TextInput(attrs={
            'readonly': True,
            'style': 'width: 50%; background-color: #f8f9fa; cursor: not-allowed;'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si estamos editando un paciente existente
        if self.instance and self.instance.pk:
            # Ocultar el campo usuario original
            self.fields['usuario'].widget = forms.HiddenInput()
            
            # Mostrar el nombre del usuario en el campo personalizado
            if self.instance.usuario:
                self.fields['usuario_display'].initial = self.instance.usuario.username
            else:
                self.fields['usuario_display'].initial = 'Sin usuario asignado'
        else:
            # Para nuevo paciente, ocultar el campo display y mostrar el select
            self.fields['usuario_display'].widget = forms.HiddenInput()
            
            # Mantener la lógica original para nuevo paciente
            try:
                grupo_cliente = Group.objects.get(name='cliente')
                usuarios_cliente = User.objects.filter(groups=grupo_cliente)
                usuarios_con_paciente = Paciente.objects.exclude(usuario=None).values_list('usuario', flat=True)
                usuarios_disponibles = usuarios_cliente.exclude(id__in=usuarios_con_paciente)
                
                self.fields['usuario'].queryset = usuarios_disponibles
                self.fields['usuario'].empty_label = "Seleccionar usuario"
                
            except Group.DoesNotExist:
                usuarios_con_paciente = Paciente.objects.exclude(usuario=None).values_list('usuario', flat=True)
                self.fields['usuario'].queryset = User.objects.exclude(id__in=usuarios_con_paciente)
                self.fields['usuario'].empty_label = "Seleccionar usuario (grupo 'cliente' no existe)"

    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': DateInput(attrs={'style': 'width: 50%'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre','autocomplete':'off'}),
            'telefono': forms.NumberInput(attrs={'placeholder': 'XXXX XXXX','autocomplete':'off','style': 'width: 50%'}),
            'sexo': forms.Select(attrs={'style': 'width: 50%'}),
            'usuario': forms.Select(attrs={'style': 'width: 50%'})
        }

    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')
        
        # Si estamos editando, mantener el usuario original
        if self.instance and self.instance.pk:
            return self.instance.usuario
        
        # Verificar si el usuario ya tiene un paciente asignado (solo para nuevos pacientes)
        if usuario:
            if Paciente.objects.filter(usuario=usuario).exists():
                raise forms.ValidationError("Este usuario ya tiene un paciente asignado.")
        
        return usuario

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = '__all__'
        widgets = {
            'observaciones': forms.Textarea(attrs={'placeholder': 'Diagnóstico del paciente', "rows": 5}),
            'precioconsulta': forms.NumberInput(attrs={'placeholder': '$00.00', 'style': 'width: 50%'}),
        }

    def __init__(self, *args, **kwargs):
        es_admin = kwargs.pop('es_admin', False)  # <- parámetro extra desde la vista
        super().__init__(*args, **kwargs)

        # Si ya tenemos paciente en initial o POST lo ocultamos
        if self.initial.get('paciente') or self.data.get('paciente'):
            self.fields['paciente'].widget = forms.HiddenInput()

        # Si el usuario NO es admin, ocultamos el select de doctor
        if not es_admin:
            self.fields['doctor'].widget = forms.HiddenInput()

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'
        widgets = {
            'paciente': forms.HiddenInput(),
            'fechacita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'horacita': forms.Select(attrs={'style': 'width: 50%'}),
            'observaciones': forms.Textarea(attrs={'placeholder': 'Detalles de la cita', "rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        es_admin = kwargs.pop('es_admin', False)
        super().__init__(*args, **kwargs)

        if not es_admin:
            # Ocultamos el campo doctor para doctores
            self.fields['doctor'].widget = forms.HiddenInput()
        else:
            # Admin ve el select con todos los doctores
            self.fields['doctor'].queryset = Doctor.objects.all()

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = [ 'medicamento', 'dosis', 'duracion', 'indicaciones']
        widgets = {'medicamento':forms.Textarea(attrs={'placeholder': 'Nombre del medicamento','autocomplete':'off',"rows":5}),
                   'dosis':forms.Textarea(attrs={'placeholder': 'Dosis','autocomplete':'off',"rows":5}),
                   'indicaciones':forms.Textarea(attrs={'placeholder': 'Indicaciones','autocomplete':'off',"rows":5}),
                   'duracion':forms.NumberInput(attrs={'placeholder': 'Dias','autocomplete':'off','style':'width: 50%'})
                   
                   }

class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['categoria', 'pdf', 'subcategoria', 'nombre', 'semana', 'descripcion']
        widgets = {
            'categoria': forms.TextInput(attrs={'placeholder': 'Categoria', 'autocomplete': 'off'}),
            'subcategoria': forms.TextInput(attrs={'placeholder': 'Subcategoria', 'autocomplete': 'off'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del ejercicio', 'autocomplete': 'off'}),
            'semana': forms.NumberInput(attrs={'placeholder': 'Semana', 'style': 'width: 50%'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Descripción del ejercicio', "rows": 5}),
            'imagenes': forms.ClearableFileInput(),
            'pdf': forms.ClearableFileInput()
        }

class ImagenEjercicioForm(forms.ModelForm):
    class Meta:
        model = ImagenEjercicio
        fields = ['imagen']
        

    class Meta:
        model = Cita
        fields = ['fechacita', 'horacita', 'observaciones']
        widgets = {
            'fechacita': DateInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%',
                'min': date.today().strftime('%Y-%m-%d')
            }),
            'horacita': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Detalles de la cita (opcional)',
                'rows': 4,
                'style': 'width: 100%'
            })
        }
        labels = {
            'fechacita': 'Fecha de la cita',
            'horacita': 'Hora de la cita',
            'observaciones': 'Observaciones'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['observaciones'].required = False
        
    def clean_fechacita(self):
        fecha = self.cleaned_data.get('fechacita')
        if fecha and fecha < date.today():
            raise forms.ValidationError("No se puede agendar una cita en el pasado.")
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fechacita')
        hora = cleaned_data.get('horacita')
        
        if fecha and hora:
            # Verificar si ya existe una cita en esa fecha y hora
            if Cita.objects.filter(fechacita=fecha, horacita=hora).exists():
                raise forms.ValidationError("Esta fecha y hora ya están ocupadas. Por favor, selecciona otra.")
        
        return cleaned_data

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['nombre', 'usuario']
        labels = {
            'nombre': 'Nombre del Doctor',
            'usuario': 'Usuario asociado',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del doctor',
                'required': True
            }),
            'usuario': forms.Select(attrs={
                'class': 'form-select',
            }),
        } 