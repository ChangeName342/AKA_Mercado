const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

navLinks.forEach(link => {
    link.addEventListener('mouseenter', () => {
        link.style.transition = 'transform 0.4s ease, color 0.4s ease, box-shadow 0.4s ease, text-shadow 0.4s ease';
        link.style.transform = 'translateY(-6px) scale(1.1) rotate(-3deg)';
        link.style.color = '#ff5722';
        link.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.3)';
        link.style.textShadow = '0 0 12px rgba(255, 255, 255, 0.7)';
    });

    link.addEventListener('mouseleave', () => {
        link.style.transition = 'transform 0.4s ease, color 0.4s ease, box-shadow 0.4s ease, text-shadow 0.4s ease';
        link.style.transform = 'translateY(0) scale(1) rotate(0)';
        link.style.color = '#ffffff';
        link.style.boxShadow = 'none';
        link.style.textShadow = '0 0 8px rgba(255, 255, 255, 0.5)';
    });
});
