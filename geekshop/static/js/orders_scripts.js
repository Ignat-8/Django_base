window.onload = function () {
    var _quantity, _price, _storage;
    var orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    var quantity_arr = [];
    var price_arr = [];
    var storage_arr = [];
    var TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    var order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    var order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    for (var i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _storage = parseInt($('input[name="orderitems-' + i + '-storage"]').val());
        _price = parseFloat($('input[name="orderitems-' + i + '-price"]').val().replace(',', '.'));

        quantity_arr[i] = _quantity;

        if (_price) {
            price_arr[i] = _price;
            storage_arr[i] = _storage;
        } else {
            price_arr[i] = 0;
            storage_arr[i] = '';
        }
    }
    if (!order_total_quantity) {
        for (var i = 0; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
    }

    $('.order_form').on('click', 'input[type="number"]', function () {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        }
        if (quantity_arr[orderitem_num] > storage_arr[orderitem_num]) {
            commentsUpdate('ошибка - кол-во на складе', orderitem_num);
        } else {
            commentsUpdate('', orderitem_num);
        }
    });

    $('.order_form').on('click', 'input[type="checkbox"]', function () {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            delta_quantity = quantity_arr[orderitem_num];
        }
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    });

    $('.order_form select').change(function () {
        var target = event.target;
        // target.value = id продукта из изменяемого поля <select>
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        $.ajax({
            url: "/order/get_product_info/" + target.value,
            success: function (data) {
                $('input[name="orderitems-' + orderitem_num + '-price"]').val(data.price + ' руб');
                $('input[name="orderitems-' + orderitem_num + '-storage"]').val(data.storage);
                price_arr[orderitem_num] = data.price;
                storage_arr[orderitem_num] = data.storage;
                quantity_arr[orderitem_num] = 0;
            },
        });
    });

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;
        $('.order_total_cost').html(order_total_cost.toString());
        $('.order_total_quantity').html(order_total_quantity.toString());
    }

    function commentsUpdate(comments, i) {
        $('input[name="orderitems-' + i + '-comments"]').val(comments.toString());
    }

    function deleteOrderItem(row) {
        var target_name = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }
}


