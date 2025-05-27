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
function buscar_paciente_index(){
	const name = document.getElementsByName('nombre')[0].value;
	
	if( name == null || name.length == 0 || exp.test(name) ) {
		location.href = "/inicio/"
		swal({
			title: "!Campo vacio!",
			text: "Escriba un nombre",
			timer: 5000,
			showConfirmButton: false});	
	}else{
		location.href = "/buscarpacienteindex/"+ name 
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

//FUNCION PARA CREAR GRAFICO DE CONTEO DE CONSULTAS
const initChart = async () => {
	const chartDom = document.getElementById("chart");
	// Evita error si el elemento no existe
	if (!chartDom) return;
	try {
	  const response = await fetch("http://127.0.0.1:8000/get_chart/");
	  const option = await response.json();
	  const myChart = echarts.init(chartDom);
	  myChart.setOption(option);
	  myChart.resize();
	} catch (error) {
	  console.error("Error cargando el gráfico:", error);
	}
  };
  // Ejecuta cuando el DOM está completamente cargado
  window.addEventListener("DOMContentLoaded", initChart);


// FUNCIÓN PARA CREAR GRÁFICO DE SUMA DE GANANCIAS POR MES
const initChart2 = async () => {
	const chartDom = document.getElementById("chart2");
	// Evita error si el elemento no existe
	if (!chartDom) return;
	try {
	  const response2 = await fetch("http://127.0.0.1:8000/get_chart2/");
	  const option2 = await response2.json();
	  const myChart2 = echarts.init(chartDom);
	  myChart2.setOption(option2);
	  myChart2.resize();
	} catch (error) {
	  console.error("Error cargando el gráfico:", error);
	}
  };
  // Ejecuta cuando el DOM está completamente cargado
  window.addEventListener("DOMContentLoaded", initChart2);


  //FUNCION PARA CREAR GRAFICO DEL HOME
const initChart3 = async () => {
	const chartDom3 = document.getElementById("chart3");
	// Evita error si el elemento no existe
	if (!chartDom3) return;
	try {
	  const response3 = await fetch("http://127.0.0.1:8000/get_chart3/");
	  const option3 = await response3.json();
	  const myChart3 = echarts.init(chartDom3);
	  myChart3.setOption(option3);
	  myChart3.resize();
	} catch (error) {
	  console.error("Error cargando el gráfico:", error);
	}
  };
  // Ejecuta cuando el DOM está completamente cargado
  window.addEventListener("DOMContentLoaded", initChart3);


//FUNCION PARA CREAR GRAFICO DE EDADES
const initChart4 = async () => {
	const chartDom4 = document.getElementById("chart4");
	// Evita error si el elemento no existe
	if (!chartDom4) return;
	try {
	  const response4 = await fetch("http://127.0.0.1:8000/get_chart4/");
	  const option4 = await response4.json();
	  const myChart4 = echarts.init(chartDom4);
	  myChart4.setOption(option4);
	  myChart4.resize();
	} catch (error) {
	  console.error("Error cargando el gráfico:", error);
	}
  };
  // Ejecuta cuando el DOM está completamente cargado
  window.addEventListener("DOMContentLoaded", initChart4);

  //FUNCION PARA CREAR GRAFICO DE PACIENTES CON MAS CONSULTAS
const initChart5 = async () => {
	const chartDom5 = document.getElementById("chart5");
	// Evita error si el elemento no existe
	if (!chartDom5) return;
	try {
	  const response5 = await fetch("http://127.0.0.1:8000/get_chart5/");
	  const option5 = await response5.json();
	  const myChart5 = echarts.init(chartDom5);
	  myChart5.setOption(option5);
	  myChart5.resize();
	} catch (error) {
	  console.error("Error cargando el gráfico:", error);
	}
  };
  // Ejecuta cuando el DOM está completamente cargado
  window.addEventListener("DOMContentLoaded", initChart5);




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

        const edad = calcularEdad(fechaNacimiento);

        document.getElementById("pacienteNombre").textContent = nombre;
        document.getElementById("pacienteFechaNacimiento").textContent = fechaNacimiento;
        document.getElementById("pacienteTelefono").textContent = telefono;
        document.getElementById("pacienteEdad").textContent = edad;

        document.getElementById("btnEditarPaciente").href = `/editarpaciente/${id}/`;
        document.getElementById("btnHistorial").href = `/historial/${id}/`;
        document.getElementById('formEliminarPaciente').action = `/eliminarpaciente/${id}/`;

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

        document.getElementById("consultaId").textContent = id;
        document.getElementById("consultaNombre").textContent = nombre;
        document.getElementById("consultaFechaconsulta").textContent = fecha;
        document.getElementById("consultaHoraconsulta").textContent = hora;
        document.getElementById("consultaPrecioconsulta").textContent = precio;
        document.getElementById("consultaObservaciones").textContent = observaciones;

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
    const observaciones = button.getAttribute('data-observaciones'); // corregido

    // Verifica que los elementos existan antes de asignar
    const nombreEl = document.getElementById("citaNombre");
    const fechaEl = document.getElementById("citaFechacita");
    const horaEl = document.getElementById("citaHoracita");
    const observacionesEl = document.getElementById("citaObservaciones");

    if (nombreEl) nombreEl.textContent = nombre || "No disponible";
    if (fechaEl) fechaEl.textContent = fecha || "No disponible";
    if (horaEl) horaEl.textContent = hora || "No disponible";
    if (observacionesEl) observacionesEl.textContent = observaciones || "Sin observaciones";

    document.getElementById("btnEditarCita").href = `/editarcita/${id}/`;
    document.getElementById('formEliminarCita').action = `/eliminarcita/${id}/`;

  });
}

});