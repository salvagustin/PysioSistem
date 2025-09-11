document.addEventListener('DOMContentLoaded', function() {


/* VARIABLA PARA EVALUAR LOS INPUT VACIOS */
var exp = /^[W]{1}[K]{1}\d{2}-\d{4}$/


/* FUNCION PARA ELIMINAR REGISTROS */
function eliminarregistro(id,objeto,objeto2){
	swal({
		title: "Eliminar registro numero: "+ id+" ?",
		text: objeto +": "+objeto2,
		icon: "warning",
		buttons: true,
		dangerMode: false,
	})
		.then((OK) => {
			if (OK) {
				location.href="/eliminar"+objeto+"/"+id;
				
			} else {
				swal("Su registro No fue Eliminado");
			}
		});
	}
/*FUNCION PARA BUSCAR CITAS POR SEMANA*/
function buscarsemana(){
	const week = document.getElementsByName('week')[0].value;
	if( week == null || week.length == 0 || exp.test(week) ) {
		swal({
			title: "!Campo vacio!",
			text: "Seleccione una semana",
			timer: 2000,
			showConfirmButton: false});
	}else{
		numano = week.substr(0,4)
		numse = week.substr(6,2)
		location.href = "/buscarsemana/"+ numano + "/"+ numse
	}	
}
/*FUNCION PARA BUSCAR PACIENTE*/
function buscar_paciente(){
	const name = document.getElementsByName('nombre')[0].value;
	
	if( name == null || name.length == 0 || exp.test(name) ) {
		location.href = "/pacientes/"
		swal({
			title: "!Campo vacio!",
			text: "Escriba un nombre",
			timer: 5000,
			showConfirmButton: false});
			
	}else{
		location.href = "/buscarpaciente/"+ name
	}	
}

/*FUNCION PARA BUSCAR PACIENTE EN INDEX*/
function buscar_paciente_index() {
  const name = document.getElementsByName('nombre')[0].value.trim();

  if (!name) {
    Swal.fire({
      icon: 'warning',
      title: '¡Campo vacío!',
      text: 'Escriba un nombre para buscar.',
      timer: 3000,
      showConfirmButton: false
    });
  } else {
    const encodedName = encodeURIComponent(name);
    window.location.href = "/buscarpacienteindex/" + encodedName + "/";
  }
}

/*FUNCION PARA BUSCAR CONSULTA POR PACIENTE*/
function buscar_consulta(){
	const name = document.getElementsByName('consulta')[0].value;
	if( name == null || name.length == 0 || exp.test(name) ) {
		swal({
			title: "!Campo vacio!",
			text: "Escriba un nombre",
			timer: 3000,
			showConfirmButton: false});
			location.href = "/consultas/"
	}else{
		location.href = "/buscarconsulta/"+ name
	}	
}
/*FUNCION PARA BUSCAR RECETA POR PACIENTE*/
function buscar_receta(){
	const name = document.getElementsByName('receta')[0].value;
	if( name == null || name.length == 0 || exp.test(name) ) {
		swal({
			title: "!Campo vacio!",
			text: "Escriba un nombre",
			timer: 3000,
			showConfirmButton: false});
			location.href = "/recetas/"
	}else{
		location.href = "/buscarreceta/"+ name
	}	
}

function consultadetalles(detalles){
	swal({
		title: "Detalles",
		text:  detalles});
	
}




function calcularEdad(fechaStr) {
const nacimiento = new Date(fechaStr);
const hoy = new Date();
let edad = hoy.getFullYear() - nacimiento.getFullYear();
const m = hoy.getMonth() - nacimiento.getMonth();
if (m < 0 || (m === 0 && hoy.getDate() < nacimiento.getDate())) {
  edad--;
}
return edad;
}
  

const modalPaciente = document.getElementById('modalPaciente');
if (modalPaciente) {
    modalPaciente.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;

        const id = button.getAttribute('data-id');
        const nombre = button.getAttribute('data-nombre');
        const fechaNacimiento = button.getAttribute('data-fecha');
        const telefono = button.getAttribute('data-telefono');
        const sexo = button.getAttribute('data-sexo');
        const usuario = button.getAttribute('data-user') || 'No asignado';

        const edad = calcularEdad(fechaNacimiento);

        document.getElementById("pacienteNombre").textContent = nombre;
        document.getElementById("pacienteFechaNacimiento").textContent = fechaNacimiento;
        document.getElementById("pacienteTelefono").textContent = telefono;
        document.getElementById("pacienteEdad").textContent = edad;
        document.getElementById("pacienteSexo").textContent = sexo ? (sexo === 'M' ? 'Masculino' : 'Femenino') : 'No especificado';
        document.getElementById("pacienteUsuario").textContent = usuario;

        document.getElementById("btnEditarPaciente").href = `/editarpaciente/${id}/`;
        document.getElementById("btnHistorial").href = `/historial/${id}/`;
        document.getElementById('formEliminarPaciente').action = `/eliminarpaciente/${id}/`;

    });
}

const modalDoctor = document.getElementById('modalDoctor');
if (modalDoctor) {
    modalDoctor.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;

        const id = button.getAttribute('data-id');
        const nombre = button.getAttribute('data-nombre');
        const usuario = button.getAttribute('data-user') || 'No asignado';

        // Asignar los datos al contenido del modal
        document.getElementById("doctorNombre").textContent = nombre;
        document.getElementById("doctorUsuario").textContent = usuario;

        // Configurar botones del modal
        document.getElementById("btnEditarDoctor").href = `/editardoctor/${id}/`;
        document.getElementById("formEliminarDoctor").action = `/eliminardoctor/${id}/`;
    });
}


const modalConsulta = document.getElementById('modalConsulta');
if (modalConsulta) {
    modalConsulta.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;

        const id = button.getAttribute('data-id');
        const nombre = button.getAttribute('data-nombre');
        const fecha = button.getAttribute('data-fechaconsulta');
        const hora = button.getAttribute('data-horaconsulta');
        const precio = button.getAttribute('data-precioconsulta');
        const observaciones = button.getAttribute('data-observaciones');
        const doctor = button.getAttribute('data-doctor') || 'No asignado';

        document.getElementById("consultaId").textContent = id;
        document.getElementById("consultaNombre").textContent = nombre;
        document.getElementById("consultaFechaconsulta").textContent = fecha;
        document.getElementById("consultaHoraconsulta").textContent = hora;
        document.getElementById("consultaPrecioconsulta").textContent = precio;
        document.getElementById("consultaObservaciones").textContent = observaciones;
        document.getElementById("consultaDoctor").textContent = doctor;

        document.getElementById("btnEditarConsulta").href = `/editarconsulta/${id}/`;
        document.getElementById('formEliminarConsulta').action = `/eliminarconsulta/${id}/`;

    });
}


    const modalCita = document.getElementById('modalCita');
    if (modalCita) {
    modalCita.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;

        const id = button.getAttribute('data-id');
        const nombre = button.getAttribute('data-nombre');
        const fecha = button.getAttribute('data-fechacita');
        const hora = button.getAttribute('data-horacita');
        const doctor = button.getAttribute('data-doctor') || 'No asignado';
        const observaciones = button.getAttribute('data-observaciones'); // corregido

        // Verifica que los elementos existan antes de asignar
        const nombreEl = document.getElementById("citaNombre");
        const fechaEl = document.getElementById("citaFechacita");
        const horaEl = document.getElementById("citaHoracita");
        const doctorEl = document.getElementById("citaDoctor");
        const observacionesEl = document.getElementById("citaObservaciones");

        if (nombreEl) nombreEl.textContent = nombre || "No disponible";
        if (fechaEl) fechaEl.textContent = fecha || "No disponible";
        if (horaEl) horaEl.textContent = hora || "No disponible";
        if (doctorEl) doctorEl.textContent = doctor || "No asignado";
        if (observacionesEl) observacionesEl.textContent = observaciones || "Sin observaciones";

        document.getElementById("btnEditarCita").href = `/editarcita/${id}/`;
        document.getElementById('formEliminarCita').action = `/eliminarcita/${id}/`;

    });
    }


    
function eliminarImagen(id) {
    if (confirm('¿Estás seguro de eliminar esta imagen?')) {
        fetch(`/eliminar-imagen/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                Swal.fire('Eliminado', 'Imagen eliminada correctamente', 'success');
                // Opcional: Recargar el modal
                document.querySelector(`[data-bs-target="#modalEjercicio"][data-id="${document.getElementById('ejercicioId').textContent}"]`).click();
            } else {
                Swal.fire('Error', data.message || 'No se pudo eliminar', 'error');
            }
        });
    }
}
// Imágenes
const imagenesContainer = document.getElementById('modalImagenes');
imagenesContainer.innerHTML = '';
try {
    const imagenes = JSON.parse(button.getAttribute('data-imagenes'));
    if (imagenes.length) {
        imagenes.forEach((imgData) => {
            const wrapper = document.createElement('div');
            wrapper.className = 'position-relative';

            const img = document.createElement('img');
            img.src = typeof imgData === 'string' ? imgData : imgData.url;
            img.className = 'img-thumbnail';
            img.style.maxHeight = '150px';

            const btnDelete = document.createElement('button');
            btnDelete.className = 'btn btn-sm btn-danger position-absolute top-0 end-0 m-1';
            btnDelete.innerHTML = '<i class="bi bi-trash"></i>';
            btnDelete.onclick = () => eliminarImagen(imgData.id || null);

            wrapper.appendChild(img);
            wrapper.appendChild(btnDelete);
            imagenesContainer.appendChild(wrapper);
        });
    } else {
        imagenesContainer.innerHTML = '<p class="text-muted">Sin imágenes</p>';
    }
} catch (e) {
    imagenesContainer.innerHTML = '<p class="text-danger">Error al cargar imágenes</p>';
}




});