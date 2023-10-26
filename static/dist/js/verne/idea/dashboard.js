//-------------------START FILTROS ----------------------

//--------Filtro por PRIORIDAD Y TIPO DE INNOVACIÓN------------


    $('#prioridads').select2({
        placeholder: "Selecciona un usuario",
        //dropdownParent: $("#creacion"),
        dropdownAutoWidth: false,
        allowClear: true,
        width: '100%',
        multiple: true,
    })

    $('#tipo_innovacions').select2({
        placeholder: "Selecciona un usuario",
        //dropdownParent: $("#creacion"),
        dropdownAutoWidth: false,
        allowClear: true,
        width: '100%',
        multiple: true,
    })


//--------Filtro por encargado------------

    function BuscarPorEncargado(id_input, url_django) {

        $(id_input).select2({
            placeholder: "Puedes seleccionar varios",
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

    BuscarPorEncargado('#collaborator', '/ideas/search_colaborator/');



//--------Filtro por ID Idea------------

    let url_completa = new URL(window.location.href);
    let parametros = new URLSearchParams(url_completa.search);
    ids_ideas = parametros.getAll('id_idea') //Prints ["294","295"]. object
    ids_ideas_data_ajax = JSON.stringify(ids_ideas)
            
    function BuscarPorIdea(id_input, url_django) {
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
    BuscarPorIdea('#id_idea', '/ideas/buscar_id_idea/')


//--------Filtro por rango de fecha------------

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

//----------------------END FILTROS---------------------------------------------



//----------------------MODAL DETALLES ---------------------------------------------
function open_modal_detail(url) {
    $('#ModalDetail').load(url, function(res) {

        $('#ModalDetail').html(res).modal({
            keyboard: false,
            //backdrop: 'static',
            show: true,

        })

    });
    
}
//----------------------END MODAL DETALLES ---------------------------------------------



//----------------------START FASES---------------------------------------------

// ----------------- Load More Fase PAIN ------------------------------
    const postsBox = document.getElementById('posts-box')
    const spinnerBox = document.getElementById('spinner-box')
    const loadBtn = document.getElementById('load-btn')
    const loadBox = document.getElementById('loading-box')
    let visible = 4

    const handleGetData = () => {
        $.ajax({
            type: 'GET', 
            url: `/ideas/posts-json/${visible}/1/`,
            data: { 
                id_idea_nombre:ids_ideas_data_ajax,
                titulo_nombre: $('#titulo_idea').val(),
                tipo_innovacion: $('#tipo_innovacion').val(), 
                prioridad: $('#prioridad').val(),
                daterange: $('#daterange').val(),
                asigned: $('#collaborator').val(),

            },
            beforeSend: function () {
                    $("#loader").show();
                    spinnerBox.classList.remove('not-visible')
                },

            complete: function (res) {
                $("#loader").hide();
                spinnerBox.classList.add('not-visible')
            },
            success: function (response) {
                maxSize = response.max
                const data = response.data
                // spinnerBox.classList.remove('not-visible')
                setTimeout(() => {
                    
                        document.getElementById('count_pain').innerHTML = response.numero_ideas
                        // spinnerBox.classList.add('not-visible')
                        data.map(post => {
   
                        if(post.asigned__profile__avatar === null){
                                post.asigned__profile__avatar='default-user.png';
                            }

                        postsBox.innerHTML +=
                        `
                        <a onclick="return open_modal_detail ('/ideas/dashboard/ideas_details/${post.id}')">
                        <div class="course p-one">
                        <div class="course-info">
                            <button class="btn boton-id boton-one">Idea ${post.id}</button>
                            <span class="avatar"></span>		
                            <p class="title">${post.title}</p>
                            <span><i class=" far fa-clock pr-1"></i>${post.phase_date_throught} d </span>
                            <span class="avatar">
                                <img class="avatar-card" src="/media/${post.asigned__profile__avatar}" data-toggle="tooltip" data-placement="top" title="${post.asigned__email}" >
                            </span>
                        </div>
                        </div>
                        </a>
                        `
                        })
                        if (maxSize) {
                        console.log('done')
                        loadBox.innerHTML = "<p class= phase1>Sin más ideas</p>"
                        }
                    }, 500)
            },

            error: function (error) {
                console.log(error)
            }
        })
    }

    handleGetData()
    loadBtn.addEventListener('click', () => {
        visible += 4
        handleGetData()
    })
  
// ----------------- Load More Fase OBSERVACION ------------------------------
    const postsBoxObs = document.getElementById('posts-box-obs')
    const spinnerBoxObs = document.getElementById('spinner-box-obs')
    const loadBtnObs = document.getElementById('load-btn-obs')
    const loadBoxObs = document.getElementById('loading-box-obs')
    let visibleObs = 4

    const handleGetDataObs = () => {
    $.ajax({
        type: 'GET', 
        url: `/ideas/posts-json/${visibleObs}/2/`,
        data: { 
            id_idea_nombre:ids_ideas_data_ajax,
            titulo_nombre: $('#titulo_idea').val(),
            tipo_innovacion: $('#tipo_innovacion').val(), 
            prioridad: $('#prioridad').val(),
            daterange: $('#daterange').val(),
            asigned: $('#collaborator').val(),
        },
        beforeSend: function () {
            console.log("$('#id_idea').val( ",$('#id_idea').val())
            spinnerBoxObs.classList.remove('not-visible')
            },

        complete: function (res) {
            spinnerBoxObs.classList.add('not-visible')
        },
        success: function (response) {
            maxSizeObs = response.max
            const dataObs = response.data	
            //spinnerBoxObs.classList.remove('not-visibleObs')
            setTimeout(() => {
            //spinnerBoxObs.classList.add('not-visibleObs')
            document.getElementById('count_obs').innerHTML = response.numero_ideas

            dataObs.map(post => {
                
            if(post.asigned__profile__avatar === null){
                post.asigned__profile__avatar='default-user.png';
            }

                postsBoxObs.innerHTML +=
                `
                <a onclick="return open_modal_detail ('/ideas/dashboard/ideas_details/${post.id}')">
                <div class="course p-two">
                <div class="course-info">
                    <button class="btn boton-id boton-two">Idea ${post.id}</button>
                    <span class="avatar"></span>		
                    <p class="title">${post.title}</p>
                    <span><i class=" far fa-clock pr-1"></i>${post.phase_date_throught} d </span>
                    <span class="avatar">
                    <img class="avatar-card" src="/media/${post.asigned__profile__avatar}" data-toggle="tooltip" data-placement="top" title="${post.asigned__email}" >
                    </span>
                </div>
                </div>
                </a>
            
                `
                })
                if (maxSizeObs) {
                loadBoxObs.innerHTML = "<p class= phase2>Sin más ideas</p>"
                }
            }, 500)
        },
        error: function (error) {
            console.log(error)
        }
    })
    }

    handleGetDataObs()

    loadBtnObs.addEventListener('click', () => {
    visibleObs += 4
    handleGetDataObs()
    })

// ----------------- Load More Fase IDEACION ------------------------------

    const postsBoxIde = document.getElementById('posts-box-ide')
    const spinnerBoxIde = document.getElementById('spinner-box-ide')
    const loadBtnIde = document.getElementById('load-btn-ide')
    const loadBoxIde = document.getElementById('loading-box-ide')
    let visibleIde = 4

    const handleGetDataIde = () => {
    $.ajax({
        type: 'GET', 
        url: `/ideas/posts-json/${visibleIde}/3/`,
        data: { 
            id_idea_nombre:ids_ideas_data_ajax,
            titulo_nombre: $('#titulo_idea').val(),
            tipo_innovacion: $('#tipo_innovacion').val(), 
            prioridad: $('#prioridad').val(),
            daterange: $('#daterange').val(),
            asigned: $('#collaborator').val(),
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
        document.getElementById('count_ide').innerHTML = response.numero_ideas
        dataIde.map(post => {

            if(post.asigned__profile__avatar === null){
                post.asigned__profile__avatar='default-user.png';
            }

            postsBoxIde.innerHTML +=
            `
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

// ----------------- Load More Fase PROTOTIPADO ------------------------------

    const postsBoxPro = document.getElementById('posts-box-pro')
    const spinnerBoxPro = document.getElementById('spinner-box-pro')
    const loadBtnPro = document.getElementById('load-btn-pro')
    const loadBoxPro = document.getElementById('loading-box-pro')
    let visiblePro = 4

    const handleGetDataPro = () => {
    $.ajax({
        type: 'GET', 
        url: `/ideas/posts-json/${visiblePro}/4/`,
        data: { 
            id_idea_nombre:ids_ideas_data_ajax,
            titulo_nombre: $('#titulo_idea').val(),
            tipo_innovacion: $('#tipo_innovacion').val(), 
            prioridad: $('#prioridad').val(),
            daterange: $('#daterange').val(),
            asigned: $('#collaborator').val(),

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

        document.getElementById('count_pro').innerHTML = response.numero_ideas

        dataPro.map(post => {

            if(post.asigned__profile__avatar === null){
                post.asigned__profile__avatar='default-user.png';
            }

            postsBoxPro.innerHTML +=
            `
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

//----------------------END FASES---------------------------------------------
