$(document).ready(function () {
   $("#table_id").DataTable({
    scrollX: true,
    scrollY: "70vh",
    select:true,
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
      },
    ],
  });
});
