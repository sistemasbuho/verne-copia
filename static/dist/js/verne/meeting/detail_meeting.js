   
// Modal para comentarios en detail_ metting
   var $ = jQuery.noConflict();

   function abrir_modal_edicion_proyecto(url) {
       $('#myModalComentario').load(url, function() {
           $(this).modal('show');
       }); 
   }

   // Modal para comentarios en detail_ metting
   function abrir_modal_close_meeting(url) {
       $('#ModalClose').load(url, function() {
           $(this).modal('show');
       }); 
   }


   function open_modal_detail(url) {
    $('#ModalDetail').load(url, function() {
        $(this).modal('show');
    }); 
}


function open_modal_vote(url) {
    $('#ModalVote').load(url, function() {
        $(this).modal('show');
    }); 
}