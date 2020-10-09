
cart_items = JSON.parse(sessionStorage.getItem('cart'))
async function getCart() {
    const response = await fetch('/cart/', { method: 'GET' })
    if (response.status === 200) {
        cart_items = await response.json()
        await sessionStorage.setItem('cart', JSON.stringify(cart_items))
        await updateCart()
    }
}



async function toggleAddToCart(item_id) {
    let element = document.querySelector(`.add-to-cart[data-id="${item_id}"]`)

    if (element.classList.contains('active')) {
        element.classList.remove('active')
        element.innerHTML = 'ADD TO CART'

        destroyCard(item_id)
    } else {
        element.classList.add('active')
        element.innerHTML = 'REMOVE ITEM'

        const response = await fetch(`/cart/add/${item_id}/`, { method: 'GET' })
        cart_items = await response.json()
        await sessionStorage.setItem('cart', JSON.stringify(cart_items))
        await updateCart()
    }
}

function updateCart() {
    mount()
    setTotal()
    const item_update_quantity = $('input.quantity')
    const remove_item = $('button.delete')

    item_update_quantity.on('change', function () {
        const id = $(this).attr('data-id')
        if ($(this).val() < 1) { $(this).val(1); }
        cart_item = cart_items[id]
        cart_item.quantity = $(this).val()
        sessionStorage.setItem('cart', JSON.stringify(cart_items))
        updateQuantity(id, $(this).val())
    })

    remove_item.click(function () {
        destroyCard($(this).attr('data-id'))
    })
}

async function updateQuantity(id, quantity) {
    updateCard(id)
    let data = new FormData()
    data.append('quantity', quantity)

    const response = await fetch(`/cart/add/${id}/`, { method: 'POST', body: data })
    cart_items = await response.json()
}

function updateCard(item_id) {
    const item = $(`#cart-item-${item_id}`)
    const price = cart_items[item_id][getCurrency()[0]] * cart_items[item_id].quantity
    item.find('.prc').html(format_price(price))
    setTotal()
}

function destroyCard(item_id) {
    remove(item_id)
    let item = $(`#cart-item-${item_id}`)
    item.remove()

    let element = document.querySelector(`.add-to-cart[data-id="${item_id}"]`)
    element.classList.remove('active')
    element.innerHTML = 'ADD TO CART'
}

async function remove(item_id) {
    delete cart_items[item_id]
    setTotal()

    const response = await fetch(`/cart/remove/${item_id}/`, { method: 'GET' })
    cart_items = await response.json()
    await sessionStorage.setItem('cart', JSON.stringify(cart_items))



}
function getCurrency() {
    currency = $('#ksh_usd').prop('checked')
    if (currency) {
        return ['usd_price', 'USD ']
    } else {
        return ['ksh_price', 'Ksh ']
    }
}

function format_price(price) {
    return `${getCurrency()[1]} ${parseFloat(price).toFixed(2).toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")}`
}

function setTotal() {
    total = 0;
    for (const key in cart_items) {
        const item = cart_items[key]
        total += (item[getCurrency()[0]] * item.quantity)
    }
    $('.total-prc').html(`${format_price(total)}`)

    let total_count = 0
    for (e in cart_items) { if (cart_items.hasOwnProperty(e)) total_count++; }
    $("#cart-count").html(total_count)
}

function mount() {
    let cart_elements = ''
    for (const cart_item in cart_items) {
        if (cart_items.hasOwnProperty(cart_item)) {
            const item = cart_items[cart_item];
            const price = cart_items[cart_item][getCurrency()[0]]
            cart_elements += `
                <li class="cart-item card mx-0 border-0 p-2" id="cart-item-${cart_item}">
                        <img src="${item.image}" loading='lazy' onerror="this.src='https://placehold.it/200x200'" alt="" class="rounded mr-auto" width="50" height="50">
                        <div class="item-info d-flex small">
                            <div class="col">
                                <span class="font-weight-bold">${item.name}</span>
                            </div>
                            <div class="col">
                                quantity
                                <input type="number" value="${item.quantity}" min="1" class="form-control form-control-sm quantity" data-id="${cart_item}" required>
                            </div>
                            <div class="d-flex flex-column small">
                                <div class="font-weight-bold prc">
                                    ${format_price(price * item.quantity)}
                                </div>
                                <button class="btn btn-danger btn-sm ml-auto delete" data-usd="${item.usd_price}" data-ksh="${item.ksh_price}"
                                data-id="${cart_item}"><i class="fas fa-times-circle"></i>
                                </button>
                                <div class="text-muted prc-each">
                                    ${parseFloat(price).toFixed(2)} each
                                </div>
                            </div>
                        </div>
                    </li>
                    `
        }
    }
    if (cart_items_element.innerHTML != cart_elements) {
        cart_items_element.innerHTML = cart_elements
    }
}
window.onload = function () {
    cart_items_element = document.getElementById('cart-items')
    updateCart()
    getCart().then(updateCart())

    const ksh_usd = document.querySelector('#ksh_usd')
    ksh_usd.checked = JSON.parse(sessionStorage.getItem('usd'))
    ksh_usd.onclick = function () {
        sessionStorage.setItem('usd', !JSON.parse(sessionStorage.getItem('usd')))
        updateCart()
    }

    $('.add-to-cart').click(function () {
        let id = $(this).attr('data-id')
        toggleAddToCart(id)
        console.log(id)
    })

}