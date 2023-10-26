
 var $ = jQuery.noConflict();


 $('#asignado_a').select2({
    placeholder: "Selecciona un usuario",
    //dropdownParent: $("#creacion"),
    dropdownAutoWidth: false,
    allowClear: true,
    selectOnClose: false,
    width: '100%',
    minimumInputLength: 2, //https://github.com/select2/select2/issues/2561

    ajax: {
        url: '/ideas/buscar_colaborador/',
        type:"GET",
        processResults: function (data) {
            return {
                results: $.map(data, function (item, index) {
                    return {
                        text: item.name,
                        id: item.id
                    }
                })
            };
        }
    }

});


function BuscarPorNombreModeloMultipleEmail(id_input, url_django) {

 $(id_input).select2({
   placeholder: "Puedes seleccionar varios",
   //dropdownParent: $("#creacion"),
   dropdownAutoWidth: false,
   allowClear: true,
   selectOnClose: false,
   language: "es",
   minimumInputLength:1,
   width: '100%',
   multiple: true,

   ajax: {
     url: url_django,
     dataType: 'json',
     type: "GET",
     processResults: function (data) {
       return {
         results: $.map(data, function (item, index) {
           return {
             text: item.name,
             id: item.id
           }
         })
       };
     }
   }

 });

 //soluciòn al problema del placeholder en los select multiples
 $('.select2-search__field').css('width', '100%');

 //soluciòn al problema del scroll dentro de los modales
 $('select.select2:not(.normal)').each(function () {
   $(this).select2({
     dropdownParent: $(this).parent().parent()
   });
 });

}




/* ----------------------------------------
    funciones Generales
 ---------------------------------------- */

 function activarBotonListar(id_html, id_registro) {
    //Valida el estado del disabled esta en true
    if ($(id_html + id_registro).prop('disabled')) {
        //activa el botón por medio del ID
        $(id_html + id_registro).prop('disabled', false);

    } else {
        //desactivar el botón por medio del ID
        $(id_html + id_registro).prop('disabled', true);
    }
}

function activarBotonModalCRUD(id_html) {
    if ($(id_html).prop('disabled')) {
        $(id_html).prop('disabled', false);
    } else {
        $(id_html).prop('disabled', true);
    }
}

function cerrar_modal_creacion() {
    $('#creacion').modal('hide');
}

function cerrar_modal_edicion() {
    $('#edicion').modal('hide');
}

function cerrar_modal_eliminacion() {
    $('#eliminacion').modal('hide');
}

function notificacionError(mensaje) {
    Swal.fire({
        title: '¡Error!',
        text: mensaje,
        icon: 'error',
        allowOutsideClick: false,
    })
}

function notificacionErrorInfo(mensaje,info,error_tittle) {
    Swal.fire({
        title: error_tittle,
        text: mensaje,
        icon: info,
        allowOutsideClick: false,
    })
}

function notificacionSuccess(mensaje) {
    Swal.fire({
        title: '¡Buen Trabajo!',
        text: mensaje,
        icon: 'success',
        timer: 5000, //milisegundos = 5
    })
}

function BuscarPorNombreModelo(id_input, url_django) {
    //console.log("url_django---------- ",url_django)
    $(id_input).select2({
        placeholder: "Selecciona un valor",
        //dropdownParent: $("#creacion"),
        //dropdownAutoWidth: false,
        allowClear: false,
        //selectOnClose: false,
        width: '100%',
        minimumInputLength: 2, //https://github.com/select2/select2/issues/2561

        ajax: {
            url: url_django,
            processResults: function (data) {
                return {
                    results: $.map(data, function (item, index) {
                        return {
                            text: item.name,
                            id: item.id
                        }
                    })
                };
            }
        }

    });


}

function mostrarErrorCreacionForm(id_form, errores) {

    //Limpiamos los errores que le asignamos la clase help-block
    $("div.help-block").remove();
    $("select,textarea, input").removeClass('is-invalid')
    //Recorremos el Json que almacena el error de form.erros
    for (var error in errores.responseJSON.error) {
        $(id_form + ' #' + error + "_crear").addClass('is-invalid'); // Añado una clase para que el input que de color rojo
        $(id_form + ' #' + error + "_crear").append('<div class="help-block text-danger">' + errores.responseJSON.error[error] + '</div>'); //pintar el error a interior del div creado
        if (error == '__all__'){
            console.log('error ',$(id_form + " #url_crear"))
            $(id_form + " #url_crear").addClass('is-invalid'); // Añado una clase para que el input que de color rojo
            $(id_form + " #url_crear").append('<div class="help-block text-danger">' + errores.responseJSON.error[error] + '</div>'); //pintar el error a interior del div creado
        }
        //$('#form_creacion .error_message #nombre').css( "border", "3px solid red" ); //Test para validar el campo en la consola del navegador
    }


}

// Se copia y se pega en el navegador para validar si funciona
let url_string = window.location.href
//Descomentamos esta lineas 
//console.log("url ",url_string)
//console.log("url.searchParams.get('id') ",url_string.split('/')[6])
let id_idea_url = url_string.split('/')[6]





/* ----------------------------------------
   Listado por server side
   Búsqueda por nombre oprimiendo enter
   Búsqueda por estado
 ---------------------------------------- */

function listaServerSide() {

    let table = $('#tabla_listar').DataTable({
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
            
            console.log("#asignado_a ",  $("#asignado_a").val())

            //Estos datos se capturan del html
            let columna_filtro = data.columns[data.order[0].column].data.replace(/\./g, "__"); //limpiamos la url del filtro
            let search_nombre = $('#search_nombre').val();
            let fecha_rango = $('#rango_input').val();
            let asignado_a = $("#asignado_a").val();

            //al interior del get se capturan todas las acciones
            //Los datos del get se envian por url  y llegan a la vista 
            $.get('/indicador/list_task/', {
                //  Parametros para pasarlos a la url y luego capturarlos desde la vista
                //  "GET /stakeholders/reglas/?limite=10&inicio=0&filtro=&order_by=id&asc_desc=asc

                limite: data.length,
                inicio: data.start,
                filtro: search_nombre,
                fecha_rango: fecha_rango,
                asignado_a: asignado_a,

                order_by: columna_filtro,
                asc_desc: data.order[0].dir, //seleccionar el campo de asc o des del array llamado: ORDER


            }, function (res) {
                // una vez recibida la respuesta del servidor hacer

           
                document.getElementById('porcentaje_formacion').style.color = '#87499c'
                document.getElementById("porcentaje_formacion").innerHTML = res.porcentaje;

                document.getElementById('participacion').style.color = '#00ada1'
                document.getElementById("participacion").innerHTML = res.participacion;


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
                "data": "id_user__email",
                'orderable': true,
                'width': '30%',
            },

            {
                "data": "name",
                'orderable': true,
                'width': '40%',
            },
            {
                "data": "date",
                'orderable': true,
                'width': '30%',
               
            },

        ],


    });

    // Habilita la búsqueda por escritura
    $('#search_nombre input').unbind();
    $('#search_nombre').bind("keyup", function (e) { // Bind our desired behavior
        // If the length is 3 or more characters, or the user pressed ENTER, search
        if (e.keyCode == 13) { //this.value.length > 2 && 
            // Call the API search function
            table.search(this.value).draw();
        }
        // Ensure we clear the search if they backspace far enough
        if (this.value == "") {
            //Si se van a realizar cambios en el datatable se debe usar draw, para ver los cambios
            table.search("").draw();
        }
        return;
    });



    $('#asignado_a').on('keyup change', function () {
        table.draw();
    });

    $("#rango_input").daterangepicker({
        onSelect: function () {
            table.draw();
        },
        opens: 'left',
        timePicker: false, //hora
        autoUpdateInput: true,
        autoApply: true,
        //startDate: moment().add(5, 'day'),
        //startDate: moment().subtract(1, 'year').add(1,'day'),//"2020-01-01",
        //endDate: moment(),
        
        
        startDate: moment().add(-1, 'month'),
        endDate: moment().add(0, 'days'),//"2020-01-01",

        minDate: "2020-01-01",
        changeYear:true,
        locale: {
            "format": "YYYY-MM-DD",
            "separator": " - ",
            "applyLabel": "Guardar",
            "cancelLabel": "Cancelar",
            "fromLabel": "Desde",
            "toLabel": "Hasta",
            "customRangeLabel": "Personalizar",
            "daysOfWeek": [
                "Do",
                "Lu",
                "Ma",
                "Mi",
                "Ju",
                "Vi",
                "Sa"
            ],
            "monthNames": [
                "Enero",
                "Febrero",
                "Marzo",
                "Abril",
                "Mayo",
                "Junio",
                "Julio",
                "Agosto",
                "Setiembre",
                "Octubre",
                "Noviembre",
                "Diciembre"
            ],
            "firstDay": 1
        },
        timePickerIncrement: 1,
        
        ranges: {
            'Today': [moment(), moment().add(1, 'days')],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days').add(1, 'days')],
            'This Week': [moment().startOf('week'), moment().add(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment().add(1, 'days')],
            'Last 30 Days': [moment().subtract(29, 'days'), moment().add(1, 'days')],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }

    }, cb);

    function cb(start, end) {

        if (start._isValid && end._isValid) {
            $('#rango_input').val(start.format('YYYY-MM-DD') + ' - ' + end.format('YYYY-MM-DD'));
            table.draw();
        } else {
            $('#rango_input').val('');
            table.draw();
        }
    }

    // //Borrar la fecha con un botón
    $('#resetDatePicker').on('click', function (e) {
        $('#rango_input').prop("resetDatePicker", true).val('');
        table.draw();
    });


    $('input[name="daterange"]').on('apply.daterangepicker', function (ev, picker) {
        $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
        table.draw();


    });

    $('input[name="daterange"]').on('cancel.daterangepicker', function (ev, picker) {
        $(this).val('');
        table.draw();

    });

}


// Cuando la pagina esta totalmente creada carga la funcion
$(document).ready(function () {
    // Multiple es para campos many to many, reutilizamos la funcion para los campos  
    
    listaServerSide();
});