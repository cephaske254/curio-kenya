$(document).ready(function () {
    var cart_items = []

    document.querySelector('#ksh_usd').checked = JSON.parse(sessionStorage.getItem('usd'))

    $('#ksh_usd').click(function () {
        sessionStorage.setItem('usd', !JSON.parse(sessionStorage.getItem('usd')))
        updateCart()
    })

    function getCurrency() {
        currency = $('#ksh_usd').prop('checked')
        if (currency) {
            return ['usd_price', 'USD ']
        } else {
            return ['ksh_price', 'Ksh ']
        }
    }

    function updateQuantity() {
        $('input.quantity').change(function () {
            if ($(this).val() < 1) { $(this).val(1) }
            parents = $(this).parentsUntil('.cart-item')
            id = parents.find('button').attr('data-id')
            cart_item = cart_items[id]
            cart_item.quantity = $(this).val()
            update(id)
            setCardPrice(id)
            setTotal()
        })
    }

    function setTotal() {
        total = 0;
        for (const key in cart_items) {
            const item = cart_items[key]
            total += (item[getCurrency()[0]] * item.quantity)
        }
        $('.total-prc').html(`${format_price(total)}`)
    }


    function setCardPrice(item_id) {
        item = $(`#cart-item-${item_id}`)
        const price = cart_items[item_id][getCurrency()[0]] * cart_items[item_id].quantity
        item.find('.prc').html(format_price(price))
    }

    function mount() {
        let cart_items_element = $('#cart-items')
        cart_items_element.empty()
        let total_count = 0

        for (e in cart_items) { if (cart_items.hasOwnProperty(e)) total_count++; }
        $("#cart-count").html(total_count)

        for (let cart_item in cart_items) {
            const price = cart_items[cart_item][getCurrency()[0]]
            item = cart_items[cart_item]
            cart_items_element.append(`
            <li class="cart-item card mx-0 border-0 p-2" id="cart-item-${cart_item}">
                            <img src="${item.image}" loading='lazy' onerror="this.src='https://placehold.it/200x200'" alt="" class="rounded mr-auto" width="50" height="50">
                            <div class="item-info d-flex small">
                                <div class="col">
                                    <span class="font-weight-bold">${item.name}</span>
                                </div>
                                <div class="col">
                                    quantity
                                    <input type="number" value="${item.quantity}" min="1" class="form-control form-control-sm quantity" required>
                                </div>
                                <div class="d-flex flex-column small">
                                    <div class="font-weight-bold prc">${format_price(price * item.quantity)}</div>
                                    <button class="btn btn-danger btn-sm ml-auto delete" data-usd="${item.usd_price}" data-ksh="${item.ksh_price}"
                                        data-id="${cart_item}"><i class="fas fa-times-circle"></i></button>
                                    <div class="text-muted prc-each">
                                        ${parseFloat(price).toFixed(2)} each
                                    </div>
                                </div>
                            </div>
                    </li>
                   `)

            $('button.delete').click(function () {
                id = $(this).attr('data-id')
                toggleAddToCart(id)
                remove(id)
            })
        }
    }

    function format_price(price) {
        return `${getCurrency()[1]} ${parseFloat(price).toFixed(2).toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")}`
    }

    function toggleAddToCart(id) {
        let element = $(`.add-to-cart[data-id="${id}"]`)
        if (element.hasClass('active')) {
            element.html('ADD TO CART').removeClass('active')

        } else {
            element.html('REMOVE ITEM').addClass('active')
        }
    }

    async function getCart() {
        let response = await fetch('/cart/');
        if (response.status === 200) {
            cart_items = await response.json()
            await sessionStorage.setItem('cart', JSON.stringify(cart_items))
            await updateCart()
        }
    }

    async function remove(id) {
        response = await fetch(`/cart/remove/${id}/`, { method: 'GET' })
        if (response.status === 200) {
            cart_items = await response.json()
            await sessionStorage.setItem('cart', JSON.stringify(cart_items))
            await updateCart()
        }
    }

    async function update(id) {
        data = new FormData()
        const quantity = cart_items[id].quantity
        if (!quantity | parseFloat(quantity) < 1) { return }
        data.append('quantity', quantity)
        response = await fetch(`/cart/add/${id}/`, {
            method: 'POST',
            body: data,
            redirect: 'follow'
        })
        if (response.status >= 200 && response.status < 400) {
            sessionStorage.setItem('cart', JSON.stringify(await response.json()))
        }
    }

    function updateCart() {
        cart_items = JSON.parse(sessionStorage.getItem('cart'))
        // mount()
        updateQuantity()
        setTotal()
    }

    async function addToCart(id) {
        await toggleAddToCart(id)
        let response = await fetch(`/cart/add/${id}/`);
        if (response.status === 200) {
            cart_items = await response.json().then(function () {
                sessionStorage.setItem('cart', JSON.stringify(cart_items))
                updateCart()
            })
        }
    }

    function configure() {
        $('button.add-to-cart').click(function () {
            id = $(this).attr('data-id')
            addToCart(id)
        })
        getCart()
    }

    configure()

})