u('li.sub-list').on('click', function () {
    u(this).children('ul').toggleClass("is-hidden")
})