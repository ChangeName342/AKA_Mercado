const links = document.querySelectorAll('.custom-link');

links.forEach(link => {
    link.addEventListener('mouseenter', () => {
        link.classList.add('animate-hover');
    });

    link.addEventListener('mouseleave', () => {
        link.classList.remove('animate-hover');
    });
});

