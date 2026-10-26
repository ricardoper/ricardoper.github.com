(function () {
	var doc = document.documentElement;
	var header = document.getElementById('home');
	var nav = document.getElementById('nav-wrap');
	var headline = document.querySelector('#home .responsive-headline');
	var links = nav.querySelectorAll('#nav a[href^="#"]');
	var blocks = [header].concat([].slice.call(document.querySelectorAll('section')));
	var ticking = false;

	doc.classList.replace('no-js', 'js');

	// Titular: ancho / 10, acotado entre 40px y 70px (x la escala de la raiz, que crece en pantallas grandes)
	function fitHeadline() {
		var k = parseFloat(getComputedStyle(doc).fontSize) / 10;
		var size = headline.getBoundingClientRect().width / 10;
		headline.style.fontSize = Math.max(40 * k, Math.min(70 * k, size)) + 'px';
	}

	// Enlace activo: última sección cuyo borde superior ya pasó el 15% del viewport
	function markActive() {
		var line = window.innerHeight * 0.15;
		var active = blocks[0];

		blocks.forEach(function (block) {
			if (block.getBoundingClientRect().top <= line) {
				active = block;
			}
		});

		[].forEach.call(links, function (a) {
			a.parentNode.classList.toggle('current', a.hash === '#' + active.id);
		});
	}

	// Menú: oculto mientras se cruza la cabecera en escritorio, opaco al pasarla
	function updateNav() {
		var y = window.pageYOffset;
		var h = header.offsetHeight;
		var hide = y > h * 0.1 && y < h && window.innerWidth > 768;

		nav.classList.toggle('nav-hidden', hide);
		if (hide) closeLangMenus();
		nav.classList.toggle('opaque', y >= h * 0.1);
	}

	function onScroll() {
		if (ticking) return;
		ticking = true;
		requestAnimationFrame(function () {
			ticking = false;
			markActive();
			updateNav();
		});
	}

	function onResize() {
		fitHeadline();
		onScroll();
	}

	// Desplegable de idioma: se cierra al hacer clic fuera, con Escape o al ocultarse el menu
	var langMenus = document.querySelectorAll('.lang-menu');

	function closeLangMenus(except) {
		[].forEach.call(langMenus, function (m) {
			if (m !== except) m.open = false;
		});
	}

	document.addEventListener('click', function (e) {
		closeLangMenus(e.target.closest ? e.target.closest('.lang-menu') : null);
	});

	document.addEventListener('keydown', function (e) {
		if (e.key === 'Escape') closeLangMenus();
	});

	// Recuerda el idioma elegido para que la raiz no vuelva a redirigir
	[].forEach.call(document.querySelectorAll('a[data-lang]'), function (a) {
		a.addEventListener('click', function () {
			try { localStorage.setItem('lang', a.getAttribute('data-lang')); } catch (e) {}
		});
	});

	window.addEventListener('scroll', onScroll, { passive: true });
	window.addEventListener('resize', onResize);
	window.addEventListener('orientationchange', onResize);
	onResize();
}());
