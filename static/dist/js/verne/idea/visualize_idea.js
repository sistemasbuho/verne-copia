$(function () {
  console.log("ingreso... ")
    $("#example1").DataTable({
      
      "paging": true,
      "lengthChange": false,
      "searching": true,
      "ordering": true,
      "info": true,
      "autoWidth": false,
      "responsive": true,
      "order": [[ 0, "desc" ]],
      "responsive": true, 
      "lengthChange": false, 
      "autoWidth": false,
      
    })
   
  });
  