(function($) {
    
    "use strict";


    /*--------------------------
     Preloader jQuery
     ---------------------------- */
    setTimeout(function() {
        $('body').addClass('loaded');
    }, 3000);

    // CounterUp
    $('.count').counterUp({
        delay: 10, // the delay time in ms
        time: 2000 // the speed time in ms
    });
    

    // Video popup
    jQuery("a.demo").YouTubePopUp();

    // Fancybox
    $(document).ready(function() {
        $('.fancybox').fancybox();
    });


    /*--------------------------
     Bootstrap slider captions animation
    ---------------------------- */
    (function( $ ) {
        //Function to animate slider captions 
        function doAnimations( elems ) {
            //Cache the animationend event in a variable
            var animEndEv = 'webkitAnimationEnd animationend';
            
            elems.each(function () {
                var $this = $(this),
                    $animationType = $this.data('animation');
                $this.addClass($animationType).one(animEndEv, function () {
                    $this.removeClass($animationType);
                });
            });
        }
        
        //Variables on page load 
        var $myCarousel = $('#carousel-example-generic'),
            $firstAnimatingElems = $myCarousel.find('.item:first').find("[data-animation ^= 'animated']");
            
        //Initialize carousel 
        $myCarousel.carousel({
            interval: 5000,
        });
        
        //Animate captions in first slide on page load 
        doAnimations($firstAnimatingElems);

        //Other slides to be animated on carousel slide event 
        $myCarousel.on('slide.bs.carousel', function (e) {
            var $animatingElems = $(e.relatedTarget).find("[data-animation ^= 'animated']");
            doAnimations($animatingElems);
        });

        $myCarousel.on('mouseover', function (e) {
             $myCarousel.carousel();
        });
        
    })(jQuery);


    /*--------------------------
     Highlight the top nav as scrolling occurs
     ---------------------------- */
    $('body').scrollspy({
        target: '.navbar-fixed-top',
        offset: 51
    })

    /*--------------------------
     Closes the Responsive Menu on Menu Item Click
     ---------------------------- */
    $('.navbar-collapse ul li a').on('click', function () {
        $('.navbar-toggle:visible').click();
    });


    /*--------------------------
     Offset for Main Navigation
     ---------------------------- */
    $('#mainNav').affix({
        offset: {
            top: 100
        }
    });

    /*--------------------------
     Scroll Menu jQuery
     ---------------------------- */
    function main() {

        $("a.page-scroll").on('click', function () {
            if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                if (target.length) {
                    $('html,body').animate({
                        scrollTop: target.offset().top - 40
                    }, 900);
                    return false;
                }
            }
        });
    }

    main();

    /*--------------------------
     Map Trigger
     ---------------------------- */
    $('#map_canvas').mapit();


})(window.jQuery); // End of use strict

