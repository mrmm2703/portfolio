// Hover handlers
$(".dark_card .img").mouseover(function () {
    $(this).stop()
    $(this).animate({
        width: "95%"
    }, {
        step: function(now, fx) {
            // console.log(fx.pos)
            // console.log('box-shadow: 0 2px 2px 0 rgba(0, 0, 0, '+0.14*(fx.pos+1)+'), 0 3px 1px -2px rgba(0, 0, 0, '+0.2*(fx.pos+1)+'), 0 1px 5px 0 rgba(0, 0, 0, '+0.12*(fx.pos+1)+')')
            $(this).css('height', $(this).width()+"px")
            $(this).css('margin-top', (origMargin - ($(this).height() - origSize))+"px")
            // $(this).css('box-shadow', ('box-shadow: 0 2px 2px 0 rgba(0, 0, 0, '+0.14*(fx.pos+1)+'), 0 3px 1px -2px rgba(0, 0, 0, '+0.2*(fx.pos+1)+'), 0 1px 5px 0 rgba(0, 0, 0, '+0.12*(fx.pos+1)+')'))
        }, duration: 150
    })
})
$(".dark_card .img").mouseout(function () {
    $(this).stop()
    $(this).animate({
        width: "90%"
    }, {
        step: function(now, fx) {
            $(this).css('height', $(this).width()+"px")
            $(this).css('margin-top', (origMargin - ($(this).height() - origSize))+"px")
            // $(this).css('box-shadow', 'box-shadow: 0 2px 2px 0 rgba(0, 0, 0, '+0.24*(1-fx.pos)+'), 0 3px 1px -2px rgba(0, 0, 0, '+0.4*(fx.pos+1)+'), 0 1px 5px 0 rgba(0, 0, 0, '+0.24*(fx.pos+1)+')')
        }, duration: 150
    })
})