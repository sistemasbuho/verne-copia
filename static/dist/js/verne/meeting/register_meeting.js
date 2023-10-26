
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


BuscarPorNombreModeloMultipleEmail('#activate_select_editar_comitte', '/meeting/buscar_usuario/')
BuscarPorNombreModeloMultipleEmail('#activate_select_editar_multiple', '/meeting/buscar_idea/')