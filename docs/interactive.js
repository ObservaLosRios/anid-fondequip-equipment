// Navegación de secciones + auto-ajuste de altura de iframes
(function(){
	function getActiveSection() {
		return document.querySelector('.section.active');
	}

	function getIframesInScope(scopeEl) {
		const scope = scopeEl || document;
		return Array.from(scope.querySelectorAll('.chart-iframe'));
	}

	function isIframeLoaded(iframe) {
		return iframe?.dataset?.loaded === 'true';
	}

	function showSection(sectionId) {
		const sections = document.querySelectorAll('.section');
		sections.forEach(sec => sec.classList.remove('active'));
		const target = document.getElementById(sectionId);
		if (target) target.classList.add('active');

		const links = document.querySelectorAll('.nav-link');
		links.forEach(l => l.classList.remove('active'));
		const active = document.querySelector(`.nav-link[data-section="${sectionId}"]`);
		if (active) active.classList.add('active');

		target?.scrollIntoView({ behavior: 'smooth', block: 'start' });
		// Evita recalcular todos los iframes: solo la sección activa y solo si ya cargaron.
		requestAnimationFrame(() => resizeIframes(target));
	}

	function initNav() {
		const navContainer = document.getElementById('nav-links');
		if (!navContainer) return;
		navContainer.addEventListener('click', (e) => {
			const el = e.target;
			if (el && el.classList && el.classList.contains('nav-link')) {
				const section = el.getAttribute('data-section');
				if (section) {
					e.preventDefault();
					showSection(section);
				}
			}
		});
	}

	function resizeIframes(scopeEl) {
		const iframes = getIframesInScope(scopeEl);
		iframes.forEach((iframe) => {
			if (!isIframeLoaded(iframe)) return;
			try {
				const doc = iframe.contentDocument || iframe.contentWindow?.document;
				if (doc && doc.body) {
					const body = doc.body;
					const html = doc.documentElement;
					const height = Math.max(
						body.scrollHeight,
						body.offsetHeight,
						html.clientHeight,
						html.scrollHeight,
						html.offsetHeight
					);
					if (height && height > 0) {
						iframe.style.height = `${height + 40}px`;
						return;
					}
				}
			} catch (e) {
				// si no podemos medir (cross-origin), usamos fallback CSS
			}

			if (!iframe.style.height) {
				iframe.style.height = getComputedStyle(iframe).height || '600px';
			}
			iframe.style.width = '100%';
			iframe.style.border = '0';
		});
	}

	function hookIframeLoad() {
		const iframes = document.querySelectorAll('.chart-iframe');
		iframes.forEach((iframe) => {
			iframe.addEventListener('load', () => {
				iframe.dataset.loaded = 'true';
				const activeSection = getActiveSection();
				if (activeSection && activeSection.contains(iframe)) {
					setTimeout(() => resizeIframes(activeSection), 80);
				}
			});
		});
	}

	document.addEventListener('DOMContentLoaded', function(){
		initNav();
		hookIframeLoad();
		// No forzamos resize global: espera a que cargue cada iframe.
		const activeSection = getActiveSection();
		if (activeSection) resizeIframes(activeSection);

		const currentActive = document.querySelector('.section.active');
		if (!currentActive) {
			const first = document.querySelector('.nav-link[data-section]')?.getAttribute('data-section');
			if (first) showSection(first);
		}
	});

	window.addEventListener('resize', () => {
		clearTimeout(window.__ifr_rsz_t);
		window.__ifr_rsz_t = setTimeout(() => resizeIframes(getActiveSection()), 150);
	});
})();
