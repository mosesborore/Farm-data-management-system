$(document).ready(function () {
   $("#table_id").DataTable({
    columnDefs:[{
      orderable: false,
      className: 'focusedRow',
      target: 0
    }],
    select:{
      style: 'multi',
    },
    order:[[1, 'asc']],
    scrollX: true,
    scrollY: "70vh",
    scrollCollapse: true,
    //responsive: true,
    paging: true,
    dom: "Bfrtip",
    orientation: "landscape",
    buttons: [
      {
        text: "Export PDF",
        extend: "pdfHtml5",
        messageTop: "Farm information report",
        exportOptions: {
          columns: [':visible']
        }
      },
      'colvis'
    ],
  });
});
