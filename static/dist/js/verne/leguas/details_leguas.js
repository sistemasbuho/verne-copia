// ----------------------------------------------------
  $(function () {
    $("#example1").DataTable();
    $('#example2').DataTable({
      "paging": true,
      "lengthChange": true,
      "searching": true,
      "ordering": true,
      "info": true,
      "autoWidth": true,
    });
  });

// ----------------------------------------------------
  var $ = jQuery.noConflict();

   function open_modal_delete_action(url) {
       $('#ModalDeleteAction').load(url, function() {
           $(this).modal('show');      
       });
   }

// ----------------------------------------------------
   function open_modal_delete_prize(url) {
       $('#ModalDeletePrize').load(url, function() {
           $(this).modal('show');      
       });
   }

// ----------------------------------------------------
function open_modal_inactive_user(url) {
    $('#ModalInactiveUser').load(url, function() {
        $(this).modal('show');      
    });
}
// ----------------------------------------------------
function open_modal_club(url) {
  $('#ModalUserClub').load(url, function() {
      $(this).modal('show');      
  });
}


$(function() {

  $(".progress").each(function() {

    var value = $(this).attr('data-value');
    var value = (value*100)/20000
    var left = $(this).find('.progress-left .progress-bar');
    var right = $(this).find('.progress-right .progress-bar');

    if (value > 0) {
      if (value <= 50) {
        right.css('transform', 'rotate(' + percentageToDegrees(value) + 'deg)')
      } else {
        right.css('transform', 'rotate(180deg)')
        left.css('transform', 'rotate(' + percentageToDegrees(value - 50) + 'deg)')
      }
    }

  })

  function percentageToDegrees(percentage) {

    return percentage / 100 * 360

  }

});


$(function() {

  $(".progress-prize").each(function() {

    var value = $(this).attr('data-value');
    var value = (value*100)/30
    var left = $(this).find('.progress-left .progress-bar');
    var right = $(this).find('.progress-right .progress-bar');

    if (value > 0) {
      if (value <= 50) {
        right.css('transform', 'rotate(' + percentageToDegrees(value) + 'deg)')
      } else {
        right.css('transform', 'rotate(180deg)')
        left.css('transform', 'rotate(' + percentageToDegrees(value - 50) + 'deg)')
      }
    }

  })

  function percentageToDegrees(percentage) {

    return percentage / 100 * 360

  }

});

$(function() {

  $(".progress-ideas").each(function() {

    var value = $(this).attr('data-value');
    var value = (value*100)/30
    var left = $(this).find('.progress-left .progress-bar');
    var right = $(this).find('.progress-right .progress-bar');

    if (value > 0) {
      if (value <= 50) {
        right.css('transform', 'rotate(' + percentageToDegrees(value) + 'deg)')
      } else {
        right.css('transform', 'rotate(180deg)')
        left.css('transform', 'rotate(' + percentageToDegrees(value - 50) + 'deg)')
      }
    }

  })

  function percentageToDegrees(percentage) {

    return percentage / 100 * 360

  }

});
