(function () {
    const doc = document;

    // 1) Page load reveal
    doc.querySelectorAll('.section, .section_padding, .card').forEach((el, idx) => {
        setTimeout(() => el.classList.add('fade-in'), 60 * idx);
    });

    // 2) Theme toggle with localStorage
    const themeToggle = doc.querySelector('[data-theme-toggle]');
    const applyTheme = (theme) => {
        if (theme === 'dark') {
            doc.documentElement.setAttribute('data-theme', 'dark');
        } else {
            doc.documentElement.removeAttribute('data-theme');
        }
        localStorage.setItem('theme', theme);
    };
    const savedTheme = localStorage.getItem('theme');
    applyTheme(savedTheme === 'dark' ? 'dark' : 'light');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const isDark = doc.documentElement.getAttribute('data-theme') === 'dark';
            applyTheme(isDark ? 'light' : 'dark');
        });
    }

    // 3) Accordion
    doc.querySelectorAll('.accordion-trigger').forEach((btn) => {
        btn.addEventListener('click', () => {
            const item = btn.closest('.accordion-item');
            if (item) item.classList.toggle('is-open');
        });
    });

    // 4) Modal open/close
    const modal = doc.querySelector('.modal');
    doc.querySelectorAll('[data-modal-open]').forEach((btn) => {
        btn.addEventListener('click', () => modal && modal.classList.add('is-open'));
    });
    doc.querySelectorAll('[data-modal-close]').forEach((btn) => {
        btn.addEventListener('click', () => modal && modal.classList.remove('is-open'));
    });

    // 5) Sticky header shadow
    const header = doc.querySelector('.site-header');
    window.addEventListener('scroll', () => {
        if (!header) return;
        header.classList.toggle('has-shadow', window.scrollY > 10);
    });

    // 6) Live filter for lists
    const filterInput = doc.querySelector('[data-filter-input]');
    const filterList = doc.querySelector('[data-filter-list]');
    if (filterInput && filterList) {
        filterInput.addEventListener('input', () => {
            const value = filterInput.value.toLowerCase();
            filterList.querySelectorAll('[data-filter-item]').forEach((item) => {
                const text = item.textContent.toLowerCase();
                item.style.display = text.includes(value) ? '' : 'none';
            });
        });
    }

    // 7) Character counter for textarea
    doc.querySelectorAll('textarea[data-counter]').forEach((textarea) => {
        const counter = doc.getElementById(textarea.dataset.counter);
        const update = () => { if (counter) counter.textContent = textarea.value.length; };
        textarea.addEventListener('input', update);
        update();
    });

    // 8) Simple tab switcher
    doc.querySelectorAll('[data-tab-trigger]').forEach((trigger) => {
        trigger.addEventListener('click', () => {
            const target = trigger.dataset.tabTrigger;
            doc.querySelectorAll('[data-tab-panel]').forEach((panel) => {
                panel.classList.toggle('is-active', panel.dataset.tabPanel === target);
            });
        });
    });

    // 9) Scroll to top button
    const scrollBtn = doc.getElementById('scrollTop');
    if (scrollBtn) {
        scrollBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    // 10) Save filter state in localStorage
    const filterForm = doc.querySelector('.filter-bar');
    if (filterForm) {
        const key = 'filters';
        filterForm.addEventListener('change', () => {
            const data = Array.from(filterForm.elements).reduce((acc, el) => {
                if (el.name) acc[el.name] = el.value;
                return acc;
            }, {});
            localStorage.setItem(key, JSON.stringify(data));
        });
    }

    // 11) Highlight invalid fields on submit
    doc.querySelectorAll('form').forEach((form) => {
        form.addEventListener('submit', () => {
            form.querySelectorAll('[required]').forEach((field) => {
                field.classList.toggle('is-invalid', !field.value);
            });
        });
    });

    // 12) Auto-fill current year
    const yearEl = doc.querySelector('.js-year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    // 13) Toggle password visibility
    doc.querySelectorAll('[data-toggle-password]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const target = doc.getElementById(btn.dataset.togglePassword);
            if (target) target.type = target.type === 'password' ? 'text' : 'password';
        });
    });

    // 14) Auto-hide messages
    doc.querySelectorAll('.message').forEach((msg) => {
        setTimeout(() => msg.classList.add('is-hidden'), 4000);
    });

    // 15) Smooth anchor scroll
    doc.querySelectorAll('a[href^="#"]').forEach((link) => {
        link.addEventListener('click', (e) => {
            const target = doc.querySelector(link.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
})();
