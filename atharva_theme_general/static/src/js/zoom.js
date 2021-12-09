odoo.define('atharva_theme_general.elevatezoom', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.WebsiteSale.include({
        _startZoom: function () {
            var $image = $('.image-container img');
            var magnify = 1.2;
            if (($image.height() <= 500) && ($image.width() <= 500)) magnify = 1.5;
            $image
                .wrap('<span style="display:inline-block"></span>')
                .css('display', 'block')
                .parent()
                .zoom({
                    url: $(this).find('img').attr('data-zoom'),
                    magnify
                });
        }
    });

    publicWidget.registry.websiteImageZoom = publicWidget.Widget.extend({
        selector: '.oe_website_sale .product-img-section',
        events: {
            'slid.bs.carousel #o-carousel-product': '_onChangeSlide',
        },
        _onChangeSlide: function (ev) {
            ev.preventDefault();
            var sale = new publicWidget.registry.WebsiteSale();
            sale._startZoom();
        },
    });

});

