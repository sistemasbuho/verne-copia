
function listaServerSide() {

    let table = $('#tabla_listar_ideas').DataTable({
        "order": [[ 0, "desc" ]],
        "autoWidth": false,
        "searching": false,
        "searchDelay":2000,
        "paging": true,
        "destroy": true,
        "language": {
            "url": '/static/dist/js/es_es.json'
        },
        "processing": true,
        "serverSide": true,
        "ajax": function (data, callback, settings) {
            //data: contiene toda la estructura del datatable en el se manejan diccionario para la busqueda
            //seleccionamos el dato de orderby
            let columna_filtro = data.columns[data.order[0].column].data.replace(/\./g, "__"); //limpiamos la url del filtro
            
            //capturamos los valores de los inputs del formulario
            let fecha_rango = $('#rango_input').val();
            let title = $("#title").val();
            let prioridad_input = $("#priority").val();
            let innovation_type_input = $("#innovation_type").val();
            let is_active_input = $("#is_active").val();
            let is_fastrack_input = $("#is_fastrack").val();
            let collaborator_input = $("#collaborator_id").val();

            //al interior del get se capturan todas las acciones
            $.get('/ideas/evaluate/', {
                //  Parametros para pasarlos a la url y luego capturarlos desde la vista
                //  "GET /stakeholders/reglas/?limite=10&inicio=0&filtro=&order_by=id&asc_desc=asc

                limite: data.length,
                inicio: data.start,
                filtro: title,
                
                rango_fecha_creacion_get_ajax: fecha_rango,
                prioridad_get_ajax: prioridad_input,
                innovation_type_get_ajax: innovation_type_input,
                is_active_get_ajax: is_active_input,
                is_fastrack_get_ajax: is_fastrack_input,
                collaborator_get_ajax: collaborator_input,

                order_by: columna_filtro,
                asc_desc: data.order[0].dir, //seleccionar el campo de asc o des del array llamado: ORDER


            }, function (res) {
                console.log("res ",res)
                // una vez recibida la respuesta del servidor hacer
                callback({
                    //total de elemento que hay en la consulta
                    recordsTotal: res.length,
                    recordsFiltered: res.length,
                    //información
                    data: res.objects
                });
            }, );
            var host = data.collaborator_list
            console.log(host,'host')
        },

        
        //definimos las columnas
        "columns": [{
                "data": "id",
                'orderable': true,
                //'width': '14%',
            },
            {
                "data": "creation_date",
                'orderable': true,
            },
            {
                "data": "title",
                'orderable': true,
                'width': '34%',
                render: function (data, type, row) {
                    return '<a class="fila-titulo " href=/ideas/evaluate/update/'+ row.id +'>'+ row.title + '</a>'
          
                },
            },
            {
                "data": "priority",
                'orderable': true,
                //"defaultContent": "Sin data",
                render: function (data, type, row) {
                    if (row.priority) {
                        return '<span class="badge badge-info"> '+ row.priority+ ' </span>'
                    } else {
                        return '<span class="badge badge-info"> ' + 'POR DEFINIR' +' </span>'
                    }
                },
            },
            {
                "data": "collaborator_list",
                'orderable': true,
                "defaultContent": "Sin usuarios",
                render: function (data, type, row) {
                    let laughString = '';
                    laughString = row.collaborator_list.toString().replaceAll(',',', ');
                    return laughString
                },
            },

            {
                "data": "innovation_type",
                'orderable': true,
                //"defaultContent": "Sin data",
                render: function (data, type, row) {
                    if (row.innovation_type) {
                        return '<span class="badge badge-info"> '+ row.innovation_type+ ' </span>'
                    } else {
                        return '<span class="badge badge-info"> ' + 'POR DEFINIR' +' </span>'
                    }
                },
            },
            {
                "data": "is_active",
                'orderable': true,
                render: function (data, type, row) {
                    if (row.is_active == true) {
                        return '<a data-toggle="tooltip" data-placement="top" title="Habilitado" target="_blank" class="white btn btn-warning rounded-circle"><i class="fa fa-check"> </i></a>';
                    } else {
                        return '<a data-toggle="tooltip" data-placement="top" title="Inhabilitado" target="_blank" class="white btn btn-warning rounded-circle"><i class="fa fa-times"> </i></a>';
                    }
                }
            },
            {
                "data": "is_fastrack",
                'orderable': true,
                render: function (data, type, row) {
                    if (row.is_fastrack == true) {
                        return '<a data-toggle="tooltip" data-placement="top" title="Habilitado" target="_blank" class="white btn btn-info rounded-circle"><i class="fa fa-check"> </i></a>';
                    } else {
                        return '<a data-toggle="tooltip" data-placement="top" title="Inhabilitado" target="_blank" class="white btn btn-info rounded-circle"><i class="fa fa-times"> </i></a>';
                    }
                }
            },
            {
                "data": "current_phase",
                'orderable': true,
                "defaultContent": '<i class="fa fa-times"> </i>',
                render: function (data, type, row) {
                    if (row.current_phase == 1) {
                        return 'Pain';
                    } if (row.current_phase == 2)  {
                        return 'Observación';
                    } if (row.current_phase == 3)  {
                        return 'Ideación';
                    } if (row.current_phase == 4)  {
                        return 'Prototipado';
                    } if (row.current_phase == 5)  {
                        return 'Implementación';
                    } if (row.current_phase == 6)  {
                        return 'Banco de Ideas';
                    }
                    
                }
            },
        ],

    });

    // habilita el datarange y formatea el campo
    $("#rango_input").daterangepicker({
            onSelect: function () {
                table.draw();
            },
            opens: 'left',
            autoUpdateInput: false,
            autoApply: false,
            locale: {
                cancelLabel: 'Cancelar',
                format: 'YYYY-MM-DD',
                applyLabel: 'Apply',
            },
            timePickerIncrement: 1,
            ranges: {
                'Today': [moment(), moment()], //, moment().add(1, 'days')],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                'This Week': [moment().startOf('week'), moment()],
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                'This Month': [moment().startOf('month'), moment().endOf('month')],
                'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            }

        } , cb //CB es una función para habilitar el campo
    );

    function cb(start, end) {

        if (start._isValid && end._isValid) {
            console.log("mirar hiojo")
            $('#rango_input').val(start.format('YYYY-MM-DD') + ' - ' + end.format('YYYY-MM-DD'));
            //table.draw();
        } else {
            $('#rango_input').val('');
            //table.draw();
        }
    }


}

// Reutilizamos codigo en caso que necesitemos más select2 multiples
function BuscarPorNombreModeloMultiple(id_input, url_django) {

    $(id_input).select2({
        placeholder: "Selecciona un valor",
        //dropdownParent: $("#creacion"),
        language: "es",
        dropdownAutoWidth: true,
        allowClear: true,
        selectOnClose: false,
        multiple:true,
        width: '100%',
        //minimumInputLength: 2, //https://github.com/select2/select2/issues/2561

        ajax: {
            url: url_django,
            dataType:'json',
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



    //soluciòn al problema del placeholder en los select multiples
    $('.select2-search__field').css('width', '100%');

    //soluciòn al problema del scroll dentro de los modales
    $('select.select2:not(.normal)').each(function () {
        $(this).select2({
            dropdownParent: $(this).parent().parent()
        });
    });

}

BuscarPorNombreModeloMultiple('#collaborator_id', '/ideas/search_colaborator/');

// llamar la función para terner resultado en consola del navegador server side 
// apoyo https://riptutorial.com/datatables/example/14618/load-data-using-ajax-with-server-side-processing-
$(document).ready(function () {
    listaServerSide();
});
