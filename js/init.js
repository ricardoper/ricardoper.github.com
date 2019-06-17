$(document).ready(function() {


	function javascriptDetect()
	{
		$('html.no-js').removeClass('no-js').addClass('js');
	}


	function adjustText() {
		$('#home .responsive-headline').fitText(1, { minFontSize: '40px', maxFontSize: '70px' });
	}


	function headerBackimgSize() {
		$('header').attr('style', 'height: '+$(window).height()+'px;');
		$('body').css('style', 'width: '+$(window).width()+'px;');
	}


	function naviPosition() {
		var sections = $('section');
		var naviLinks = $('#home #nav-wrap a');

		sections.waypoint({
			handler: function(event, direction) {
				var activeSection = $(this);

				if (direction === 'up') {
					activeSection = activeSection.prev();
				}

				var activeLink = $('#home #nav-wrap a[href=\'#'+activeSection.attr('id')+'\']');

				naviLinks.parent().removeClass('current');

				activeLink.parent().addClass('current');
			},
			offset: '15%'
		});
	}


	function naviFadeRun(navi, headerHeight) {
		var scrollTop = $(window).scrollTop();

		if ( (scrollTop > headerHeight * .10) && (scrollTop < headerHeight) && ($(window).outerWidth() > 768 ) ) {
			navi.fadeOut();
		} else {
			if (scrollTop < headerHeight * .10) {
				navi.removeClass('opaque').fadeIn();
			} else {
				navi.addClass('opaque').fadeIn();
			}
		}
	}

	function naviFade() {
		var navi = $('#home #nav-wrap');
		var headerHeight = $('#home').height();

		naviFadeRun(navi, headerHeight);

		$(window).on('scroll', function() {
			naviFadeRun(navi, headerHeight);
		});
	}


	function smoothScroll() {
		$('.smoothscroll').on('click',function (e) {
			e.preventDefault();
			e.stopPropagation();

			var target = this.hash;
			var $target = $(target);

			$('html, body').stop().animate({
				'scrollTop': $target.offset().top
			}, 800, 'swing', function () {
				window.location.hash = target;
			});
		});
	}



	javascriptDetect();
	adjustText();
	headerBackimgSize();
	naviPosition();
	naviFade();
	smoothScroll();

	$(window).on('resize', function() {
		adjustText();
		headerBackimgSize();
	});


});
