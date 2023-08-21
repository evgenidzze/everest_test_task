$(document).ready(function () {

    $('.increment-btn').click(function (e) {
        console.log('func work')
        e.preventDefault();

        let qtyInput = $(this).closest('.product-data').find('.input-qty');
        let qty = parseInt(qtyInput.val(), 10);
        qty = isNaN(qty) ? 0 : qty;

        if (qty < 10) {
            qty++;
            qtyInput.val(qty);
        }
    });

    $('.decrement-btn').click(function (e) {
        console.log('func work')
        e.preventDefault();

        let qtyInput = $(this).closest('.product-data').find('.input-qty');
        let qty = parseInt(qtyInput.val(), 10);
        qty = isNaN(qty) ? 0 : qty;

        if (qty > 1) {
            qty--;
            qtyInput.val(qty);
        }
    });
});