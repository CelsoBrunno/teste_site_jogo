const inputArquivo = document.getElementById('arquivo');
const listaArquivos = document.getElementById('lista-arquivos');


inputArquivo.addEventListener('change', () => {
    const arquivos = inputArquivo.files;
    if (arquivos.length > 0) {
        const lista = document.createElement('ul');
        for (const arquivo of arquivos) {
            const item = document.createElement('li');
            item.textContent = arquivo.name;

            const btnRemover = document.createElement('button');
            btnRemover.textContent = 'X';

            btnRemover.addEventListener('click', () => {
                item.remove(); 
            });

            item.appendChild(btnRemover);


            lista.appendChild(item);
        }
        listaArquivos.appendChild(lista);
    } else {
        listaArquivos.textContent = 'Nenhum arquivo selecionado.';
    }
});
