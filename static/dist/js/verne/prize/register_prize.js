$('#id_prize_crear').select2({
    width: '100%',
    dropdownAutoWidth: true,
    allowClear: false,
    placeholder:"Seleccciona el premio",
});

  
function BuscarPorNombreModeloMultipleEmail(id_input, url_django) {
    $(id_input).select2({
      placeholder: "Puedes seleccionar varios",
      //dropdownParent: $("#creacion"),
      dropdownAutoWidth: false,
      allowClear: true,
      selectOnClose: false,
      width: '100%',
      multiple: true,
      minimumInputLength: 1, //https://github.com/select2/select2/issues/2561

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

BuscarPorNombreModeloMultipleEmail('#id_user_crear', '/ideas/buscar_colaborador/')


// Generales

function notificacionError(mensaje) {
    Swal.fire({
        title: 'Error!',
        text: mensaje,
        icon: 'error',
        allowOutsideClick: false,
    })
}

function notificacionSuccess(puntos_premio,mensaje_con_puntos,mensaje_sin_puntos) {
    //console.log("mensaje ",mensaje)
    Swal.fire({
        title: 'Puntos requeridos: '+puntos_premio,
        //text: 'El resultado es:',
        html: 
        'Se asigno puntos a: <pre>' +
        mensaje_con_puntos +
        '</pre>'+
        'Error al asignar puntos: <pre>' +
        mensaje_sin_puntos +
        '</pre>'
        ,
        confirmButtonText: 'Aceptar',
        allowOutsideClick: false,
        //timer: 5000, //milisegundos = 5
    })
}

function activarBotonModalCRUD(id_html) {
    if ($(id_html).prop('disabled')) {
        $(id_html).prop('disabled', false);
    } else {
        $(id_html).prop('disabled', true);
    }
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

//AJAX

function registrar() {

    activarBotonModalCRUD('#boton_creacion')
    $.ajax({
        data: $('#form_creacion_asignacion_premio').serialize(),
        url: $('#form_creacion_asignacion_premio').attr('action'),
        type: $('#form_creacion_asignacion_premio').attr('method'),

        beforeSend: function () {
            $("#loader_crear").show();
        },

        complete: function (res) {
            $("#loader_crear").hide();
        },

        success: function (response) {

            // actualiza el listado que se paso como parámetro para ver cambios en el DataTable después de guardar
            notificacionSuccess(response.puntos_premio,response.mensaje_con_puntos, response.mensaje_sin_puntos);
            activarBotonModalCRUD('#boton_creacion')
        },
        error: function (error) {
            try {
                notificacionError(error.responseJSON.mensaje);
                mostrarErrorCreacionForm("#form_creacion_asignacion_premio", error)
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


document.getElementById("boton_creacion").addEventListener("click", function () {
    registrar();
});