
function BuscarPorNombreModeloEmail(id_input, url_django) {
  $(id_input).select2({
    placeholder: "Selecciona una opción",
    dropdownAutoWidth: false,
    allowClear: true,
    selectOnClose: false,
    minimumInputLength: 1,
    width:'100%',
    
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

  //Solución al problema del scroll dentro de los modales
    $('select.select2:not(.normal)').each(function () {
      $(this).select2({
        dropdownParent: $(this).parent().parent()
      });
    });
  }


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


// Multiple es para campos many to many, reutilizamos la funcion para los campos  
BuscarPorNombreModeloEmail('#activate_select_idea', '/prize/buscar_idea/')
BuscarPorNombreModeloMultipleEmail('#activate_select_usuarios', '/prize/buscar_usuario/')