// PARAMS
var TableID         = '#example';
var TooltipText     = 'Click here to edit';
var SelectRowClass  = 'bg-primary'; // To force Bootstrap's primary colour or any other
//


var table = $(TableID).DataTable({
    "dom": "<'card-body pl-0 pr-0 pt-0'<'row align-items-center'<'col-12 col-md-6'B><'col-6'f>>>" +
            "<'row'<'col-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
    buttons: [
    // FIXED CONTROL BUTTONS
        // Page rows
        'pageLength',

        // Export to CSV
        {
            className: 'ml-2 rounded',
            text: 'Export',
            extend: 'csvHtml5'
        },
    // END FIXED CONTROL

    // SELECTED ROWS BUTTONS
    // Those buttons appear when there are selected buttons
        {
            text: 'Edit',
            // .ml-2 and .rounded-left to make a flawless space between this first button and the fixed ones
            // .btn-req-selection to make the show/disapear behaviour
            // .invisible to make it invisible by default
            className: 'ml-2 rounded-left btn-req-selection invisible',
            action: function ( e, dt, node, config ) {
                var SelectedRow = dt.rows({ selected: true }).data().join(',');
                alert(SelectedRow);
            }
        },
        {
            text: 'Lock',
            className: 'btn-req-selection invisible', // Basic classes for selection control and invisibility
            action: function ( e, dt, node, config ) {
                var SelectedRow = dt.rows({ selected: true }).data().join(',');
                alert(SelectedRow);
            }
        },
        {
            text: 'Delete',
            className: 'btn-req-selection invisible btn-danger', // Bootstrap's btn-danger for delete
            action: function ( e, dt, node, config ) {
                var SelectedRow = dt.rows({ selected: true }).data().join(',');
                alert(SelectedRow);
            }
        }

    ],
    "select": {
        "style":    'os',
        "blurable": true
    },
});

// ROW SELECTION
//
// I had to force Bootstrap's primary colour to highlight the selection.
// I also used Bootstrap's invisible class to make the buttons appear/disappear
// depending on row selection
table.on( 'select', function ( e, dt, type, indexes ) {
    // Set Bootstrap's highlight
    indexes.forEach(function (element, index, array) {
        table.row(element).nodes().to$().addClass( 'text-white ' + SelectRowClass);
    });

    // Make '.btn-req-selection' buttons visible
    $('div.dt-buttons a.btn-req-selection').removeClass('invisible');
} );

// ROW DESELECTION
table.on( 'deselect', function ( e, dt, type, indexes ) {
    // Removing Bootstrap's highlight
    indexes.forEach(function (element, index, array) {
        table.row(element).nodes().to$().removeClass( 'text-white ' + SelectRowClass);
    });

    // Make '.btn-req-selection' buttons invisible
    if (table.rows( { selected: true } ).data().length == 0 ) {
        $('div.dt-buttons a.btn-req-selection').addClass('invisible');
    }
});


// To make the control buttons smaller
$('div.dt-buttons').addClass('btn-group-sm');

// Adding table's tooltip
$(TableID + ' tr').attr('title', TooltipText);