/* Local storage capturar
miStorage = window.localStorage;

function storeid(){
    miStorage.setItem('ids', JSON.stringify($('#id_idea').val()));
}
*/


/* Opción con Url de parametros:

?id_idea=294&id_idea=295&titulo=&tipo_innovacion=&prioridad=&datarange=

*/ 
let url_completa = new URL(window.location.href);
let parametros = new URLSearchParams(url_completa.search);

ids_ideas = parametros.getAll('id_idea') //Prints ["294","295"]. object
ids_ideas_data_ajax = JSON.stringify(ids_ideas)
        

function BuscarPorNombreModeloMultipleEmail(id_input, url_django) {
    $(id_input).select2({
      placeholder: " ",
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
            console.log("data ",data)
          return {
            results: $.map(data, function (item, index) {
              return {
                text: item.id,
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

        /* Permite obtener valores por localstorage 
        
        var local_ids = JSON.parse(localStorage.getItem("ids")) //['294', '295', '296']

        if(local_ids.length != 0){
            
            for (var i = 0; i < local_ids.length; i++){
                console.log("state ",local_ids[i]) //294
                var newState = new Option(local_ids[i], local_ids[i], true, true);
                $("#id_idea").append(newState).trigger('change');
            }
        }

        */      

        // captura la url para pintarla en el select2
        if(ids_ideas){

            for (var i = 0; i < ids_ideas.length; i++){
                console.log("state ",ids_ideas[i]) //294
                var newState = new Option(ids_ideas[i], ids_ideas[i], true, true);
                $("#id_idea").append(newState).trigger('change');
            }
        }

  }


// Multiple es para campos many to many, reutilizamos la funcion para los campos  
BuscarPorNombreModeloMultipleEmail('#id_idea', '/ideas/buscar_id_idea/')


function open_modal_detail(url) {
    $('#ModalDetail').load(url, function(res) {

        $('#ModalDetail').html(res).modal({
            keyboard: false,
            //backdrop: 'static',
            show: true,

        })

    });
    
}

// START: Rango de fecha de ingestion


    $("#daterange").daterangepicker({
        opens: 'left',
        timePicker: false, //hora
        autoUpdateInput: false,
        autoApply: false,
        //startDate: moment().add(5, 'day'),
        //startDate: moment().subtract(1, 'year').add(1,'day'),//"2020-01-01",
        //endDate: moment(),
        
        //startDate: moment().year()+"-01-01",//"2020-01-01",
        //endDate: moment().add(2, 'month'),

        minDate: "2015-01-01",
        changeYear:true,
        locale: {
            "format": "YYYY-MM-DD - YYYY-MM-DD",
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

    }, cb_ingestion);


    function cb_ingestion(start, end) {

        if (start._isValid && end._isValid) {
            
            $('#daterange').val(start.format('YYYY-MM-DD') + ' - ' + end.format('YYYY-MM-DD'));
           
        } else {
            $('#daterange').val('');
           
        }
    }

    $('input[name="daterange_name"]').on('apply.daterangepicker', function (ev, picker) {
        $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
    });

    $('input[name="daterange_name"]').on('cancel.daterangepicker', function (ev, picker) {
        $(this).val('');
    });

// END: Rango de fecha del ingestion


// ----------------- Load More Fase Banco ------------------------------

const postsBoxIde = document.getElementById('posts-box-banco')
const spinnerBoxIde = document.getElementById('spinner-box-banco')
const loadBtnIde = document.getElementById('load-btn-banco')
const loadBoxIde = document.getElementById('loading-box-banco')
let visibleIde = 4

const handleGetDataIde = () => {
$.ajax({
    type: 'GET', 
    url: `/ideas/posts-json/${visibleIde}/6/`,
    data: { 
        id_idea_nombre:ids_ideas_data_ajax,
        titulo_nombre: $('#titulo_idea').val(),
        tipo_innovacion: $('#tipo_innovacion').val(), 
        prioridad: $('#prioridad').val(),
        daterange: $('#daterange').val(),
        activado: false,
    },
    beforeSend: function () {
        spinnerBoxIde.classList.remove('not-visible')
    },

    complete: function (res) {
        spinnerBoxIde.classList.add('not-visible')
    },

    success: function (response) {
    maxSizeIde = response.max
    const dataIde = response.data	
    //spinnerBoxIde.classList.remove('not-visible')
    setTimeout(() => {
    //spinnerBoxIde.classList.add('not-visible')
    document.getElementById('count_banco').innerHTML = response.numero_ideas
    dataIde.map(post => {
        if(post.asigned__profile__avatar === null){
            post.asigned__profile__avatar='default-user.png';
        }

        postsBoxIde.innerHTML +=
        `
        <div class="col-md-6" >
        <a onclick="return open_modal_detail ('/ideas/dashboard/ideas_details/${post.id}')">
        <div class="course p-three">
        <div class="course-info">
            <button class="btn boton-id boton-three">Idea ${post.id}</button>
            <span class="avatar"></span>		
            <p class="title">${post.title}</p>
            <span><i class=" far fa-clock pr-1"></i>${post.phase_date_throught} d </span>
            <span class="avatar">
                <img class="avatar-card" src="/media/${post.asigned__profile__avatar}" data-toggle="tooltip" data-placement="top" title="${post.asigned__email}" >
            </span>
        </div>
        </div>
        </a>
        </div>
    `
        })
        if (maxSizeIde) {
        loadBoxIde.innerHTML = "<p class=phase3>Sin más ideas</p>"
        }
    }, 500)
    },
    error: function (error) {
    console.log(error)
    }
})
}

handleGetDataIde()

loadBtnIde.addEventListener('click', () => {
visibleIde += 4
handleGetDataIde()
})

// ----------------- Load More Fase Impleementación ------------------------------

const postsBoxPro = document.getElementById('posts-box-implementacion')
const spinnerBoxPro = document.getElementById('spinner-box-implementacion')
const loadBtnPro = document.getElementById('load-btn-implementacion')
const loadBoxPro = document.getElementById('loading-box-implementacion')
let visiblePro = 4

const handleGetDataPro = () => {
$.ajax({
    type: 'GET', 
    url: `/ideas/posts-json/${visiblePro}/5/`,
    data: { 
        id_idea_nombre:ids_ideas_data_ajax,
        titulo_nombre: $('#titulo_idea').val(),
        tipo_innovacion: $('#tipo_innovacion').val(), 
        prioridad: $('#prioridad').val(),
        daterange: $('#daterange').val(),
        activado: true,

    },
    beforeSend: function () {
        spinnerBoxPro.classList.remove('not-visible')
        },

    complete: function (res) {
        spinnerBoxPro.classList.add('not-visible')
    },
    success: function (response) {
    maxSizePro = response.max
    const dataPro = response.data	
    //spinnerBoxPro.classList.remove('not-visible')
    setTimeout(() => {
    //spinnerBoxPro.classList.add('not-visible')

    document.getElementById('count_implementacion').innerHTML = response.numero_ideas

    dataPro.map(post => {

        if(post.asigned__profile__avatar === null){
            post.asigned__profile__avatar='default-user.png';
        }

        postsBoxPro.innerHTML +=
        `
        <div class="col-md-6" >
        <a onclick="return open_modal_detail ('/ideas/dashboard/ideas_details/${post.id}')">
        <div class="course p-four">
        <div class="course-info">
            <button class="btn boton-id boton-four">Idea ${post.id}</button>
            <span class="avatar"></span>		
            <p class="title">${post.title}</p>
            <span><i class=" far fa-clock pr-1"></i>${post.phase_date_throught} d </span>
            <span class="avatar">
                <img class="avatar-card" src="/media/${post.asigned__profile__avatar}" data-toggle="tooltip" data-placement="top" title="${post.asigned__email}" >
            </span>
        </div>
        </div>
        </a>
        </div>
    `
        })
        if (maxSizePro) {
        loadBoxPro.innerHTML = "<p class=phase4 >Sin más ideas</p>"
        }
    }, 500)
    },
    error: function (error) {
    console.log(error)
    }
})
}

handleGetDataPro()

loadBtnPro.addEventListener('click', () => {
visiblePro += 4
handleGetDataPro()
})

