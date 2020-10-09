
$(document).ready(function () {

    $('.carousel .carousel-item').first().addClass('active')

    $('.navbar-toggler').click(function () {
        $('#navbar').toggleClass('bg-white-tr')
    })

    $('.search_toggle').hover(function () {
        $(this).hide()
        $('.search_form').animate({ width: 'toggle' }, '100%')
    }, function () {
        $('.search_form').mouseleave(function () {
            $(this).mouseleave(function () {
                $(this).hide()
                $('.search_toggle').fadeIn()
            })
        })
    })



    let prevScrollpos = window.pageYOffset;
    let outerHeight = window.outerHeight / 2;
    let navMarginTop = $('#navbar').css('margin-top');
    let navbar = document.getElementById("navbar");

    // NAVBAR SCROLL EFFECT
    window.onscroll = function () {
        var currentScrollPos = window.pageYOffset;
        if (prevScrollpos < currentScrollPos) {
            if (currentScrollPos > outerHeight) {
                $('#navbar').css({ 'margin-top': `-${navbar.clientHeight + 2}px` })
            }
            navbar.style.background = 'rgba(255, 255, 255,.90)'
        } else {
            if (currentScrollPos == 0) {
                navbar.style.background = 'rgba(255, 255, 255,.90)'
            } else {
                navbar.style.background = 'rgb(255, 255, 255)'
            }
            if (currentScrollPos > outerHeight) {
                $('#navbar').css({ 'margin-top': navMarginTop })
            }
        }
        prevScrollpos = currentScrollPos;
    }
    // 

    function setTopContainer() {
        $('.for-top').css({
            'margin-top': `${navbar.clientHeight + 10}px`,
        })
    }
    setTopContainer()
    $(window).on('resize', function () {
        setTopContainer()
    })



})