 // ----------------------------------------
 //  Listado por server side
 // Búsqueda por nombre oprimiendo enter
 // Búsqueda por estado
 //---------------------------------------- 

 $('#prioridad').select2({
    placeholder: "Selecciona un usuario",
    //dropdownParent: $("#creacion"),
    dropdownAutoWidth: false,
    allowClear: true,
    width: '100%',
    multiple: true,
 })

 $('#tipo').select2({
    placeholder: "Selecciona un usuario",
    //dropdownParent: $("#creacion"),
    dropdownAutoWidth: false,
    allowClear: true,
    width: '100%',
    multiple: true,
 })

function listaServerSideTable() {

    let table = $('#tabla_indicador').DataTable({
        "searching": false,
        "searchDelay": 2000,
        "async": true,
        "order": [[ 0, "desc" ]],
        "autoWidth": false,
        "paging": true,
        "destroy": true,
        "language": {
            "url": '/static/dist/js/es_es.json'
        },
        "processData": true, 
        "processing": true,
        "serverSide": true,
        "ajax": function (data, callback, settings) {
            //data: contiene toda la estructura del datatable en el se manejan diccionario para la busqueda
            //console.log("data 1- ", data)
            //seleccionamos el dato de orderby
            

            //Estos datos se capturan del html
            let columna_filtro = data.columns[data.order[0].column].data.replace(/\./g, "__"); //limpiamos la url del filtro
            let tipo = $('#tipo').val();
            let prioridad = $("#prioridad").val();

            //al interior del get se capturan todas las acciones
            //Los datos del get se envian por url  y llegan a la vista 
            $.get('/indicador/indicator_table/', {
                //  Parametros para pasarlos a la url y luego capturarlos desde la vista
                //  "GET /stakeholders/reglas/?limite=10&inicio=0&filtro=&order_by=id&asc_desc=asc

                limite: data.length,
                inicio: data.start,
                tipo: tipo,
                prioridad: prioridad,

                order_by: columna_filtro,
                asc_desc: data.order[0].dir, //seleccionar el campo de asc o des del array llamado: ORDER


            }, function (res) {
                // una vez recibida la respuesta del servidor hacer

           
                // document.getElementById('porcentaje_formacion').style.color = '#87499c'
                // document.getElementById("porcentaje_formacion").innerHTML = res.porcentaje;

                // document.getElementById('participacion').style.color = '#00ada1'
                // document.getElementById("participacion").innerHTML = res.participacion;


                callback({
                    //total de elemento que hay en la consulta
                    recordsTotal: res.length,
                    recordsFiltered: res.length,
                    //información
                    data: res.objects
                });
            }, );
        },


        //definimos las columnas
        "columns": [

            {
                "data": "Fase",
                'orderable': true,
                'width': '30%',
            },

            {
                "data": "Conteo",
                'orderable': true,
                'width': '20%',
            },

            {
                "data": "Prioridad",
                'orderable': true,
                'width': '20%',
            },

            {
                "data": "Tipo de Innovacion",
                'orderable': true,
                'width': '30%',
            },
 
 

        ],


    });

 
    $('#prioridad').on('keyup change', function () {
        table.draw();
    });

    $('#tipo').on('keyup change', function () {
        table.draw();
    });

}


// Cuando la pagina esta totalmente creada carga la funcion
$(document).ready(function () {
    // Multiple es para campos many to many, reutilizamos la funcion para los campos  
    
    listaServerSideTable();
});