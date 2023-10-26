var $ = jQuery.noConflict();

/*-----------------Modales opcines en vista  Update Idea---------------*/

/*Inactivar Idea*/

function open_modal_inactive_idea(url) {
    $('#ModalInactive').load(url, function() {

        $(this).modal('show');
    
    });
}

/*Cambiar fase*/

function open_modal_phase_idea(url) {
    $('#ModalPhase').load(url, function(res) {

        // $(this).modal('show');
        $('#ModalPhase').html(res).modal({
            keyboard: false,
            backdrop: 'static',
            show: true,

        })
        console.log('Mogal fasee')
    });
}


/*Referenciar*/


function open_modal_reference(url) {
    $('#ModalReference').load(url, function() {

        $(this).modal('show');
    });
}


/*Reactivar Idea*/

function open_modal_reactive(url) {
    $('#ModalReactive').load(url, function() {

        $(this).modal('show');
    });
}

/*Pasar por metodo fastrack*/


function open_modal_fastrack(url) {
    $('#ModalFastrack').load(url, function() {

        $(this).modal('show');
    });
}


