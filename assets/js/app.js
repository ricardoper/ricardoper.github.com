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

	// Tema claro/oscuro: sin eleccion guardada se sigue al sistema; el boton fija una eleccion explicita
	var themeButton = document.querySelector('.theme-toggle');

	if (themeButton) {
		var darkQuery = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

		var isDark = function () {
			var theme = doc.getAttribute('data-theme');
			return theme ? theme === 'dark' : !!(darkQuery && darkQuery.matches);
		};

		var syncTheme = function () {
			themeButton.setAttribute('aria-pressed', String(isDark()));
		};

		themeButton.hidden = false;
		syncTheme();

		themeButton.addEventListener('click', function () {
			var next = isDark() ? 'light' : 'dark';
			doc.setAttribute('data-theme', next);
			try { localStorage.setItem('theme', next); } catch (e) {}
			syncTheme();
		});

		if (darkQuery && darkQuery.addEventListener) darkQuery.addEventListener('change', syncTheme);
	}

	// Animacion de entrada al hacer scroll (solo si el visitante no pidio menos movimiento)
	var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

	if (!calm && 'IntersectionObserver' in window) {
		var seen = new IntersectionObserver(function (entries) {
			entries.forEach(function (entry) {
				if (!entry.isIntersecting) return;
				entry.target.classList.add('is-visible');
				seen.unobserve(entry.target);
			});
		}, { rootMargin: '0px 0px -8% 0px' });

		[].forEach.call(document.querySelectorAll('#about .row, section.resume .header-col, section.resume .item'), function (el) {
			el.classList.add('reveal');
			seen.observe(el);
		});
	}

	// Imprimir / guardar CV en PDF: los puestos plegados se abren solo durante la impresion
	var folded = [];

	function printOpen() {
		folded = [].filter.call(document.querySelectorAll('details.older'), function (d) { return !d.open; });
		folded.forEach(function (d) { d.open = true; });
		[].forEach.call(document.querySelectorAll('.reveal'), function (el) { el.classList.add('is-visible'); });
	}

	function printRestore() {
		folded.forEach(function (d) { d.open = false; });
		folded = [];
	}

	window.addEventListener('beforeprint', printOpen);
	window.addEventListener('afterprint', printRestore);

	[].forEach.call(document.querySelectorAll('[data-print]'), function (button) {
		button.hidden = false;
		button.addEventListener('click', function () { window.print(); });
	});

	// Cookies: Google Analytics solo se carga si el visitante lo acepta
	var consentBox = document.getElementById('consent');

	if (consentBox) {
		var gaId = consentBox.getAttribute('data-ga');
		var MAX_AGE = 395 * 24 * 3600 * 1000; // la eleccion se vuelve a preguntar pasados ~13 meses

		var readConsent = function () {
			try {
				var at = parseInt(localStorage.getItem('consentAt'), 10);
				if (!at || Date.now() - at > MAX_AGE) return null;
				return localStorage.getItem('consent');
			} catch (e) {
				return null;
			}
		};

		var saveConsent = function (value) {
			try {
				localStorage.setItem('consent', value);
				localStorage.setItem('consentAt', String(Date.now()));
			} catch (e) {}
		};

		var loadAnalytics = function () {
			if (!gaId || window.gtag) return;
			window['ga-disable-' + gaId] = false;
			window.dataLayer = window.dataLayer || [];
			window.gtag = function () { window.dataLayer.push(arguments); };
			var s = document.createElement('script');
			s.async = true;
			s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(gaId);
			document.head.appendChild(s);
			window.gtag('js', new Date());
			window.gtag('config', gaId);
		};

		// Si se retira el consentimiento, se desactiva GA y se borran sus cookies (_ga, _ga_*)
		var clearAnalytics = function () {
			if (gaId) window['ga-disable-' + gaId] = true;
			var host = location.hostname;
			var domains = ['', host, '.' + host, '.' + host.replace(/^www\./, '')];
			document.cookie.split(';').forEach(function (cookie) {
				var name = cookie.split('=')[0].trim();
				if (!/^_ga/.test(name)) return;
				domains.forEach(function (domain) {
					document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + (domain ? '; domain=' + domain : '');
				});
			});
		};

		var state = readConsent();
		if (state === 'granted') loadAnalytics();
		else if (!state) consentBox.hidden = false;

		[].forEach.call(consentBox.querySelectorAll('[data-consent]'), function (button) {
			button.addEventListener('click', function () {
				var value = button.getAttribute('data-consent');
				saveConsent(value);
				consentBox.hidden = true;
				if (value === 'granted') loadAnalytics(); else clearAnalytics();
			});
		});

		[].forEach.call(document.querySelectorAll('[data-consent-open]'), function (button) {
			button.hidden = false;
			button.addEventListener('click', function () {
				consentBox.hidden = false;
				consentBox.querySelector('button').focus();
			});
		});
	}

	window.addEventListener('scroll', onScroll, { passive: true });
	window.addEventListener('resize', onResize);
	window.addEventListener('orientationchange', onResize);
	onResize();
}());
