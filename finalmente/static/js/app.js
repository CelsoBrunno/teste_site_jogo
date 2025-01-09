    document.addEventListener("DOMContentLoaded", function () {
        // Selecionando os itens de imagem e suas seções relacionadas
        const items = document.querySelectorAll('.container_imagens .item');

        // Funções de seleção para cada grupo de seções
        const frontEndSections = document.querySelectorAll('.grupo-front');
        const backEndSections = document.querySelectorAll('.grupo-back');
        const analiseSections = document.querySelectorAll('.grupo-analise');
        const scrumSections = document.querySelectorAll('.grupo-scrum');

        // Função para esconder todas as seções
        function esconderTodasAsSecoes() {
            frontEndSections.forEach(section => section.style.display = 'none');
            backEndSections.forEach(section => section.style.display = 'none');
            analiseSections.forEach(section => section.style.display = 'none');
            scrumSections.forEach(section => section.style.display = 'none');
        }

        // Adiciona evento de clique a cada item de imagem
        items.forEach(item => {
            item.addEventListener('click', function (e) {
                // Previne a navegação padrão
                e.preventDefault();

                // Esconde todas as seções antes de mostrar a correspondente
                esconderTodasAsSecoes();

                // Verifica o link do item clicado (href) e exibe a seção correspondente
                const targetId = item.querySelector('a').getAttribute('href').substring(1); // Remove o '#'

                let targetSection = null;

                // Define a seção que corresponde ao targetId
                if (targetId === "front-end") {
                    targetSection = frontEndSections[0];
                } else if (targetId === "back-end") {
                    targetSection = backEndSections[0];
                } else if (targetId === "analise-requisitos") {
                    targetSection = analiseSections[0];
                } else if (targetId === "scrum") {
                    targetSection = scrumSections[0];
                }

                // Exibe a seção correspondente
                if (targetSection) {
                    targetSection.style.display = 'block';

                    // Faz a tela rolar até a seção
                    targetSection.scrollIntoView({ behavior: 'smooth' });
                }
              })
            })
          });
