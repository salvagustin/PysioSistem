from django import forms
from gestor.models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class PacienteForm(forms.ModelForm):

    class Meta:
        model = Paciente
        fields = '__all__'       
        widgets = {'fecha_nacimiento':DateInput(attrs={'style': 'width: 50%'}),
                   'nombre': forms.TextInput(attrs={'placeholder': 'Nombre','autocomplete':'off'}),
                   'telefono': forms.NumberInput(attrs={'placeholder': 'XXXX XXXX','autocomplete':'off','style': 'width: 50%'}),
                   'sexo': forms.Select(attrs={'style': 'width: 50%'})
                   
                   }


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = '__all__'
        widgets = {
            'presionarterial': forms.TextInput(attrs={'placeholder': 'XX/XX', 'style': 'width: 50%'}),
            'peso': forms.NumberInput(attrs={'placeholder': 'Kg', 'style': 'width: 50%'}),
            'temperatura': forms.NumberInput(attrs={'placeholder': '°C', 'style': 'width: 50%'}),
            'sintomas': forms.Textarea(attrs={'placeholder': 'Síntomas del paciente', "rows": 5}),
            'altura': forms.NumberInput(attrs={'placeholder': 'Mts', 'style': 'width: 50%'}),
            'diagnostico': forms.Textarea(attrs={'placeholder': 'Diagnóstico del paciente', "rows": 5}),
            'tratamiento': forms.Textarea(attrs={'placeholder': 'Tratamiento del paciente', "rows": 5}),
            'precioconsulta': forms.NumberInput(attrs={'placeholder': '$00.00', 'style': 'width: 50%'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('paciente') or self.data.get('paciente'):
            self.fields['paciente'].widget = forms.HiddenInput()


        

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'
        widgets = {
                    'paciente': forms.HiddenInput(),
                    'fechacita':DateInput(attrs= {'class':'form-control','style': 'width: 50%'}),
                    'observaciones':forms.Textarea(attrs={'placeholder': 'Detalles de la cita',"rows":5}),
                    'horacita':forms.Select(attrs={'style': 'width: 50%'})
                   
                   }
        
class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = [ 'medicamento', 'dosis', 'duracion', 'indicaciones']
        widgets = {'medicamento':forms.Textarea(attrs={'placeholder': 'Nombre del medicamento','autocomplete':'off',"rows":5}),
                   'dosis':forms.Textarea(attrs={'placeholder': 'Dosis','autocomplete':'off',"rows":5}),
                   'indicaciones':forms.Textarea(attrs={'placeholder': 'Indicaciones','autocomplete':'off',"rows":5}),
                   'duracion':forms.NumberInput(attrs={'placeholder': 'Dias','autocomplete':'off','style':'width: 50%'})
                   
                   }