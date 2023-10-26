
 
/*-----------Select2 campos del formulario Update-----------*/




$('#editar_objetivo').select2({
 width: '100%',
 multiple: true,
 placeholder:"Puedes escoger más de uno",
 dropdownAutoWidth: false,
 allowClear: true,
});


$('#edit_asigned').select2({
    width: '100%',
    multiple: false,
    placeholder:"Puedes escoger más de uno",
    dropdownAutoWidth: false,
    allowClear: true,
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
    funciones especificas de creación
---------------------------------------- */

function registrar() {

    activarBotonModalCRUD('#boton_creacion')
    $.ajax({
        data: $('#form_creacion').serialize(),
        url: $('#form_creacion').attr('action'),
        type: $('#form_creacion').attr('method'),

        beforeSend: function () {
            $("#loader_crear").show();
        },

        complete: function (res) {
            $("#loader_crear").hide();
        },

        success: function (response) {

            // actualiza el listado que se paso como parámetro para ver cambios en el DataTable después de guardar
            notificacionSuccess(response.mensaje);
            cerrar_modal_creacion();
            listaServerSide();
            activarBotonModalCRUD('#boton_creacion')
        },
        error: function (error) {
            try {
                notificacionError(error.responseJSON.mensaje);
                mostrarErrorCreacionForm("#form_creacion", error)
                activarBotonModalCRUD('#boton_creacion')
            } catch (error) {
                Swal.fire({
                    title: 'Error de servidor, contactar con soporte',
                    text: error,
                    icon: 'error',
                    allowOutsideClick: false,
                })
                activarBotonModalCRUD('#boton_creacion')
            }
        }
    });
}

//Carga el modal, la validación de repetidos y los select2
function abrir_modal_creacion(url) {
    activarBotonModalCRUD('#abrir_modal_creacion')
    //Recibe una url y por medio de get reciba un html si todo funciona "Entra al success", si hay un error muestra un  error
    $.ajax({
        url: url,
        type: "GET",
        cache: false,
        dataType: "html",

        beforeSend: function () {
            $("#loader").show();
        },

        complete: function (res) {
            $("#loader").hide();

            activarBotonModalCRUD('#abrir_modal_creacion')
          // $('#fase_form_create1').appendTo($('#fase_form_create1').val(id_idea_url))
            $('#id_form_create1').appendTo($('#id_form_create1').val(id_idea_url))
        },

        success: function (res) {
            $('#creacion').html(res).modal({ //Se envia respuesta del html que renderiza, modal es propio de bootstrap
                keyboard: false,    // keyboard: no deja salir con el teclado,  
                backdrop: 'static', // que sea estatico 
                show: true, //que se muestre(show)
            })
            // keyboard: no deja salir con el teclado, static que sea estatico y que se muestre(show)

            document.getElementById("boton_creacion").addEventListener("click", function () {
                registrar();
            });

            BuscarPorNombreModelo('#user_crear', '/ideas/buscar_colaborador/');
            $('#user_crear').empty()      
        },

        error: function (xhr, ajaxOptions, thrownError) {
            try {
                if (xhr.status == 403) {
                    Swal.fire({
                        title: 'Error!' + thrownError,
                        text: 'No cuenta con el permiso necesario para acceder',
                        icon: 'error',
                        allowOutsideClick: false,
                    })
                }
            } catch (error) {
                Swal.fire({
                    title: 'Error de servidor, contactar con soporte',
                    text: error,
                    icon: 'error',
                    allowOutsideClick: false,
                })
            }
        }
    });
}

//Valida si existe el botón de creación
if (document.getElementById("abrir_modal_creacion")) {
    document.getElementById("abrir_modal_creacion").addEventListener("click", function () {
        abrir_modal_creacion('/ideas/task_create_idea/');
    });
}


/* ----------------------------------------
    funciones especificas de edición
 ---------------------------------------- */

 function abrir_modal_edicion(url) {
    //obtener id de la url
    
    //opcion equivocada
    //var regex = /[0-9]/g;
    //console.log("regex ",regex )
    //var id = url.match(regex);

    //opción 1
    // var id = url.match(/\d/g);
    // id=id.join("");
    // console.log("url ", url)
    // console.log("id ", id)

    //opción 2
    console.log("url.split('/')[3] ",url.split('/')[3])
    let id = url.split('/')[3]

    activarBotonListar('#editar_lista_', id)
    $.ajax({
        url: url,
        type: "GET",
        cache: false,
        dataType: "html",

        beforeSend: function () {
            $("#loader").show();
        },

        complete: function (res) {
            $("#loader").hide();
        },

        success: function (res) {
            activarBotonListar('#editar_lista_', id);
            $('#edicion').html(res).modal({
                keyboard: false,
                backdrop: 'static',
                show: true,
            })

            //$('#edicion').html(res).modal('show')


            document.getElementById("boton_edicion").addEventListener("click", function () {
                editar();
            });

            BuscarPorNombreModelo('#user_editar', '/ideas/buscar_colaborador/');
  
        },

        error: function (xhr, ajaxOptions, thrownError) {
            //capturo el error 403
            try {
                if (xhr.status == 403) {
                    Swal.fire({
                        title: 'Error!' + thrownError,
                        text: 'No cuenta con el permiso necesario para acceder',
                        icon: 'error',
                        allowOutsideClick: false,
                    })
                }
            } catch (error) {
                Swal.fire({
                    title: 'Error de servidor, contactar con soporte',
                    text: error,
                    icon: 'error',
                    allowOutsideClick: false,
                })
            }
        }
    });
}

function editar() {
    activarBotonModalCRUD('#boton_edicion')
    $.ajax({
        data: $('#form_edicion').serialize(),
        url: $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),

        beforeSend: function () {
            $("#loader_editar").show();
        },

        complete: function (res) {
            $("#loader_editar").hide();
        },

        success: function (response) {
            notificacionSuccess(response.mensaje);
            cerrar_modal_edicion();
            //location.reload();
            listaServerSide();
        },

        error: function (error) {
            try {
                notificacionError(error.responseJSON.mensaje);
                mostrarErrorEdicionForm("#form_edicion", error)
                activarBotonModalCRUD('#boton_edicion')
            } catch (error) {
                Swal.fire({
                    title: 'Error de servidor, contactar con soporte',
                    text: error,
                    icon: 'error',
                    allowOutsideClick: false,
                })
                activarBotonModalCRUD('#boton_edicion')
            }
        }

    })
}


/* ----------------------------------------
    funciones especificas de eliminación
 ---------------------------------------- */

 function abrir_modal_eliminacion(url) {
    

    console.log("url.split('/')[3] eliminar ",url.split('/')[3])
    let id = url.split('/')[3]

    activarBotonListar('#eliminar_lista_', id);

    $.ajax({
        url: url,
        success: function (res) {
            activarBotonListar('#eliminar_lista_', id);
            $('#eliminacion').html(res).modal({
                keyboard: false,
                backdrop: 'static',
                show: true,
            })

            document.getElementById("boton_eliminacion").addEventListener("click", function () {
                eliminar();
            });

        },
        error: function (xhr, ajaxOptions, thrownError) {
            activarBotonModalCRUD('#boton_eliminacion')
            try {
                //capturo el error 403
                if (xhr.status == 403) {
                    Swal.fire({
                        title: 'Error!' + thrownError,
                        text: 'No cuenta con el permiso necesario para acceder',
                        icon: 'error',
                        allowOutsideClick: false,
                    })
                }
            } catch (error) {
                Swal.fire({
                    title: 'Error de servidor, contactar con soporte',
                    text: error,
                    icon: 'error',
                    allowOutsideClick: false,
                })
            }
        }

    });
}

function eliminar() {
    activarBotonModalCRUD('#boton_eliminacion')
    //var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
    //console.log("token ",token)
    let csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        headers: {
            'X-CSRFToken': csrfmiddlewaretoken
        },
        //url: '/ideas/task_delete/' + pk + '/',
        url: $('#form_eliminar').attr('action'),
        type: 'delete',
        cache: false,

        beforeSend: function () {
            $("#loader_eliminar").show();
        },

        complete: function (res) {
            $("#loader_eliminar").hide();
        },

        success: function (response) {
            notificacionSuccess(response.mensaje);
            cerrar_modal_eliminacion();
            listaServerSide();

        },
        error: function (error) {
            try {
                notificacionError(error.responseJSON.mensaje);
                activarBotonModalCRUD('#boton_eliminacion')

            } catch (error) {
                Swal.fire({
                    title: 'Error de servidor, contactar con soporte',
                    text: error,
                    icon: 'error',
                    allowOutsideClick: false,
                })
                activarBotonModalCRUD('#boton_eliminacion')
            }
        }
    })
}

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
        "processing": true,
        "serverSide": true,
        "ajax": function (data, callback, settings) {
            //data: contiene toda la estructura del datatable en el se manejan diccionario para la busqueda
            //console.log("data 1- ", data)
            //seleccionamos el dato de orderby

            //Estos datos se capturan del html
            let columna_filtro = data.columns[data.order[0].column].data.replace(/\./g, "__"); //limpiamos la url del filtro
            let search_nombre = $('#search_nombre').val();
            //let fecha_rango = $('#rango_input').val();
            let search_estado = $("#search-estado").val();

            //al interior del get se capturan todas las acciones
            //Los datos del get se envian por url  y llegan a la vista 
            $.get('/ideas/list_task_idea/', {
                //  Parametros para pasarlos a la url y luego capturarlos desde la vista
                //  "GET /stakeholders/reglas/?limite=10&inicio=0&filtro=&order_by=id&asc_desc=asc

                limite: data.length,
                inicio: data.start,
                filtro: search_nombre,
                idea_get_ajax: id_idea_url,
                //fase_get_ajax: id_fase_url,
                //rango_fecha_creacion: fecha_rango,
                order_by: columna_filtro,
                search_estado: search_estado,
                asc_desc: data.order[0].dir, //seleccionar el campo de asc o des del array llamado: ORDER


            }, function (res) {
                // una vez recibida la respuesta del servidor hacer

                console.log('res',res)
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
                "data": "task__title",
                'orderable': true,
                'width': '30%',
            },

            {
                "data": "task__user__email",
                'orderable': true,
                'width': '20%',
            },
            {
                "data": "task__complete",
                'orderable': true,
                'width': '15%',
                render: function (data, type, row) {
                    if (data)
                        return '<div class="fonticon-wrap"><i class="fa fa-check"></i></div>';
                    else
                        return '<div class="fonticon-wrap"><i class="fa fa-times"></i></div>';

                },
            },

            {
                "data": null,
                'orderable': false,
                'className': "container",
                'width': '30%',
                render: function (data, type, row) {
                    return '<div class="row justify-content-center"><div class="col-6 col-xl-6 col-lg-6 col-sm-6 text-right"><button id="editar_lista_' + row.task__id + '"' + 'type="button" class="btn btn-info " onclick="abrir_modal_edicion(\'/ideas/task_update_idea/' + row.task__id + '/\');"><i class="fa fa-edit fa-1x"></i></button></div>' + '<div class="col-6 col-xl-6 col-lg-6 col-sm-6 text-left"><button id="eliminar_lista_' + row.task__id + '"' + 'type="button" class="btn btn-danger" onclick="abrir_modal_eliminacion(\'/ideas/task_delete_idea/' + row.task__id + '/\');"><i class="fas fa-trash-alt fa-1x"></button></div></div>';
                    //return 'hola'
                },

            }

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


    $('#search-estado').on('keyup change', function () {
        table.draw();
    });

    // $("#rango_input").daterangepicker({
    //     onSelect: function () {
    //         table.draw();
    //     },
    //     opens: 'left',
    //     autoUpdateInput: false,
    //     autoApply: false,
    //     locale: {
    //         cancelLabel: 'Limpiar',
    //         format: 'YYYY-MM-DD',
    //         applyLabel: 'Apply',
    //     },
    //     timePickerIncrement: 1,
    //     clearBtn: true,
    //     ranges: {
    //         'Today': [moment()],
    //         'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days').add(1, 'days')],
    //         'This Week': [moment().startOf('week')],
    //         'Last 7 Days': [moment().subtract(6, 'days')],
    //         'Last 30 Days': [moment().subtract(29, 'days')],
    //         'This Month': [moment().startOf('month'), moment().endOf('month')],
    //         'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
    //     }

    // }, cb);

    // function cb(start, end) {

    //     if (start._isValid && end._isValid) {
    //         $('#rango_input').val(start.format('YYYY-MM-DD') + ' - ' + end.format('YYYY-MM-DD'));
    //         table.draw();
    //     } else {
    //         $('#rango_input').val('');
    //         table.draw();
    //     }
    // }

    // //Borrar la fecha con un botón
    // $('#resetDatePicker').on('click', function (e) {
    //     $('#rango_input').prop("resetDatePicker", true).val('');
    //     table.draw();
    // });


    // $('input[name="daterange"]').on('apply.daterangepicker', function (ev, picker) {
    //     $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
    //     table.draw();


    // });

    // $('input[name="daterange"]').on('cancel.daterangepicker', function (ev, picker) {
    //     $(this).val('');
    //     table.draw();

    // });

}


// Cuando la pagina esta totalmente creada carga la funcion
$(document).ready(function () {
  // Multiple es para campos many to many, reutilizamos la funcion para los campos  

BuscarPorNombreModeloMultipleEmail('#editar_colaborador', '/ideas/buscar_colaborador/')
BuscarPorNombreModeloMultipleEmail('#editar_merge', '/ideas/buscar_merge/')


    listaServerSide();
});