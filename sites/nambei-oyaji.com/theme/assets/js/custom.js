/**
 * 南米おやじ Child Theme - Custom JS
 */

document.addEventListener('DOMContentLoaded', () => {

  // ============================================
  // Hamburger Menu
  // ============================================
  const hamburger = document.getElementById('js-hamburger');
  const nav = document.getElementById('js-nav');

  if (hamburger && nav) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('active');
      nav.classList.toggle('open');
    });
  }

  // ============================================
  // Sidebar Tab Switching
  // ============================================
  document.querySelectorAll('.tab-nav__btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const parent = btn.closest('.sidebar-widget');
      const targetId = btn.dataset.tab;

      // Deactivate all tabs
      parent.querySelectorAll('.tab-nav__btn').forEach(b => b.classList.remove('active'));
      parent.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

      // Activate clicked tab
      btn.classList.add('active');
      const panel = parent.querySelector('#' + targetId);
      if (panel) panel.classList.add('active');
    });
  });

  // ============================================
  // Scroll-to-Top Button
  // ============================================
  const scrollTopBtn = document.getElementById('js-scroll-top');

  if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
      scrollTopBtn.classList.toggle('visible', window.scrollY > 400);
    });

    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ============================================
  // Scroll Fade-in Animation
  // ============================================
  const fadeElements = document.querySelectorAll('.scroll-fade');

  if (fadeElements.length > 0 && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );

    fadeElements.forEach(el => observer.observe(el));
  } else {
    // Fallback: show all immediately
    fadeElements.forEach(el => el.classList.add('is-visible'));
  }

  // ============================================
  // Smooth scroll for anchor links
  // ============================================
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (targetId === '#') return;

      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const headerHeight = document.querySelector('.site-header')?.offsetHeight || 70;
        const top = target.getBoundingClientRect().top + window.scrollY - headerHeight - 20;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });

});
