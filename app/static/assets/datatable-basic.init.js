
$('#zero_config1').DataTable({
    columnDefs: [
        { orderable: false, targets: 0 }
      ]
});




$('#default_order').DataTable({
    "order": [
        [3, "desc"]
    ]
});




$('#multi_col_order').DataTable({
    columnDefs: [{
        targets: [0],
        orderData: [0, 1]
    }, {
        targets: [1],
        orderData: [1, 0]
    }, {
        targets: [4],
        orderData: [4, 0]
    }]
});