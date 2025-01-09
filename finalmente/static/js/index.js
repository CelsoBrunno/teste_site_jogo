document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.depoimentos_cartao');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    const fadeInElements = document.querySelectorAll('.fade-in');
    
    let currentIndex = 0;

    // Função para exibir o cartão ativo
    const showCard = (index) => {
        cards.forEach((card, i) => {
            card.classList.remove('active');
            if (i === index) {
                card.classList.add('active');
            }
        });
    };

    // Função de visibilidade para os elementos com fade-in
    const checkVisibility = () => {
        fadeInElements.forEach(element => {
            const rect = element.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom >= 0) {
                element.classList.add('visible');
            }
        });
    };

    // Botão para ir para o slide anterior
    prevButton.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + cards.length) % cards.length;
        showCard(currentIndex);
    });

    // Botão para ir para o próximo slide
    nextButton.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % cards.length;
        showCard(currentIndex);
    });

    // Exibe o primeiro cartão ao carregar
    showCard(currentIndex);

    // Detecta quando o usuário rola a página
    window.addEventListener('scroll', checkVisibility);

    // Verifica visibilidade dos elementos ao carregar a página
    checkVisibility();
});
