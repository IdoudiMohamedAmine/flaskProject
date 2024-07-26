(function ($) {
    "use strict";

    function serviceActive($scope, $) {
        const serviceswiper = new Swiper('.tg-service-active', {
            speed: 1500,
            loop: true,
            slidesPerView: 4,
            spaceBetween: 30,
            autoplay: true,
            breakpoints: {
                '1200': {
                    slidesPerView: 4,
                },
                '992': {
                    slidesPerView: 4,
                },
                '768': {
                    slidesPerView: 3,
                },
                '576': {
                    slidesPerView: 2,
                },
                '0': {
                    slidesPerView: 1,
                },
            },
            // Navigation arrows
            navigation: {
                prevEl: '.service-next',
                nextEl: '.service-prev',
            },
        });
    }
    function counterActive($scope, $) {
        new PureCounter();
        new PureCounter({
            filesizing: true,
            selector: ".filesizecount",
            pulse: 2,
        });
    }
    function revealActive($scope, $) {
        const hoverItem = document.querySelectorAll(".tg-reveal-item");
        function moveImage(e, hoverItem, index) {
            const item = hoverItem.getBoundingClientRect();
            const x = e.clientX - item.x;
            const y = e.clientY - item.y;
            if (hoverItem.children[index]) {
                hoverItem.children[index].style.transform = `translate(${x}px, ${y}px)`;
            }
        }
        hoverItem.forEach((item, i) => {
            item.addEventListener("mousemove", (e) => {
                setInterval(moveImage(e, item, 1), 50);
            });
        });
    }
    function testimonialActive($scope, $) {
        const testimonial = new Swiper('.tg-testimonial-active', {
            // Optional parameters
            speed: 1500,
            loop: true,
            slidesPerView: 2,
            spaceBetween: 30,
            autoplay: true,
            breakpoints: {
                '1200': {
                    slidesPerView: 2,
                },
                '992': {
                    slidesPerView: 2,
                },
                '768': {
                    slidesPerView: 2,
                },
                '576': {
                    slidesPerView: 1,
                },
                '0': {
                    slidesPerView: 1,
                },
            },
            // Navigation arrows
            navigation: {
                prevEl: '.test-next',
                nextEl: '.test-prev',
            },
        });
    }
    function brandActive($scope, $) {
        const brand = new Swiper('.tg-brand-active', {
            // Optional parameters
            speed: 1500,
            loop: true,
            slidesPerView: 6,
            autoplay: true,
            breakpoints: {
                '1200': {
                    slidesPerView: 6,
                },
                '992': {
                    slidesPerView: 5,
                },
                '768': {
                    slidesPerView: 4,
                },
                '576': {
                    slidesPerView: 3,
                },
                '0': {
                    slidesPerView: 2,
                },
            },
        });
    }
    function serviceActiveTwo($scope, $) {
        const servic2swiper = new Swiper('.tg-service-2-active', {
            // Optional parameters
            speed: 1500,
            loop: true,
            slidesPerView: 3,
            spaceBetween: 30,
            autoplay: true,
            breakpoints: {
                '1200': {
                    slidesPerView: 3,
                },
                '992': {
                    slidesPerView: 2,
                },
                '768': {
                    slidesPerView: 2,
                },
                '576': {
                    slidesPerView: 1,
                },
                '0': {
                    slidesPerView: 1,
                },
            },
            // Navigation arrows
            navigation: {
                prevEl: '.service-next',
                nextEl: '.service-prev',
            },
        });
    }
    function testimonialActiveTwo($scope, $) {
        const testimonial3 = new Swiper('.tg-testimonial-2-active', {
            // Optional parameters
            speed: 1500,
            loop: true,
            slidesPerView: 1,
            spaceBetween: 30,
            autoplay: true,
            breakpoints: {
                '1200': {
                    slidesPerView: 1,
                },
                '992': {
                    slidesPerView: 1,
                },
                '768': {
                    slidesPerView: 1,
                },
                '576': {
                    slidesPerView: 1,
                },
                '0': {
                    slidesPerView: 1,
                },
            },
            pagination: {
                el: ".test-slider-dots",
                clickable:true,
            },
        });
    }
    function projectGalleryActive($scope, $) {
        const gellaryswiper = new Swiper('.tg-gellary-active', {
            // Optional parameters
            speed: 1500,
            loop: true,
            slidesPerView: 4,
            spaceBetween: 30,
            autoplay: true,
            breakpoints: {
                '1200': {
                    slidesPerView: 4,
                },
                '992': {
                    slidesPerView: 4,
                },
                '768': {
                    slidesPerView: 3,
                },
                '576': {
                    slidesPerView: 2,
                },
                '0': {
                    slidesPerView: 1,
                },
            },
            // Navigation arrows
            navigation: {
                prevEl: '.gellary-next',
                nextEl: '.gellary-prev',
            },
        });
    }
    function teamActive($scope, $) {
        const teamswiper = new Swiper('.tg-team-2-active', {
            // Optional parameters
            speed: 1500,
            loop: true,
            slidesPerView: 3,
            spaceBetween: 30,
            autoplay: true,
            breakpoints: {
                '1200': {
                    slidesPerView: 3,
                },
                '992': {
                    slidesPerView: 3,
                },
                '768': {
                    slidesPerView: 2,
                },
                '576': {
                    slidesPerView: 1,
                },
                '0': {
                    slidesPerView: 1,
                },
            },
            // Navigation arrows
            navigation: {
                prevEl: '.team-2-next',
                nextEl: '.team-2-prev',
            },
        });
    }
    function testimonialActiveThree($scope, $) {
        const testimonialswiper = new Swiper('.tg-testimonial-3-active', {
            // Optional parameters
            speed: 1500,
            loop: true,
            slidesPerView: 1,
            spaceBetween: 30,
            autoplay: false,
            breakpoints: {
                '1200': {
                    slidesPerView: 1,
                },
                '992': {
                    slidesPerView: 1,
                },
                '768': {
                    slidesPerView: 1,
                },
                '576': {
                    slidesPerView: 1,
                },
                '0': {
                    slidesPerView: 1,
                },
            },
            pagination: {
                el: ".test-2-slider-dots",
                clickable:true,
            },
        });
    }
    function ProjectActiveEight($scope, $) {
        const projectswiper = new Swiper('.tg-project-3-active', {
            // Optional parameters
            speed: 1500,
            loop: true,
            slidesPerView: 4,
            spaceBetween: 30,
            autoplay: false,
            breakpoints: {
                '1200': {
                    slidesPerView: 4,
                },
                '992': {
                    slidesPerView: 3,
                },
                '768': {
                    slidesPerView: 3,
                },
                '576': {
                    slidesPerView: 2,
                },
                '0': {
                    slidesPerView: 1,
                },
            },
            // Navigation arrows
            navigation: {
                prevEl: '.project-3-next',
                nextEl: '.project-3-prev',
            },
        });
    }

    $(window).on('elementor/frontend/init', function () {
        if (elementorFrontend.isEditMode()) {
            elementorFrontend.hooks.addAction('frontend/element_ready/int-service.default', serviceActive)
            elementorFrontend.hooks.addAction('frontend/element_ready/int-funfact.default', counterActive)
            elementorFrontend.hooks.addAction('frontend/element_ready/int-project-v2.default', revealActive)
            elementorFrontend.hooks.addAction('frontend/element_ready/int-testimonial.default', testimonialActive)
            elementorFrontend.hooks.addAction('frontend/element_ready/int-brand.default', brandActive)
            elementorFrontend.hooks.addAction('frontend/element_ready/int-service-v3.default', serviceActiveTwo)
            elementorFrontend.hooks.addAction('frontend/element_ready/int-project-v4.default', revealActive)
            elementorFrontend.hooks.addAction('frontend/element_ready/int-funfact-v2.default', counterActive)
            elementorFrontend.hooks.addAction('frontend/element_ready/int-funfact-v3.default', counterActive)
            elementorFrontend.hooks.addAction('frontend/element_ready/int-funfact-v4.default', counterActive)
            elementorFrontend.hooks.addAction('frontend/element_ready/int-testimonial-v2.default', testimonialActiveTwo)
            elementorFrontend.hooks.addAction('frontend/element_ready/int-testimonial-v3.default', testimonialActiveThree)
            elementorFrontend.hooks.addAction('frontend/element_ready/int-project-v6.default', projectGalleryActive)
            elementorFrontend.hooks.addAction('frontend/element_ready/int-team-v2.default', teamActive)
            elementorFrontend.hooks.addAction('frontend/element_ready/int-project-v8.default', ProjectActiveEight)
        }
    });

})(jQuery);