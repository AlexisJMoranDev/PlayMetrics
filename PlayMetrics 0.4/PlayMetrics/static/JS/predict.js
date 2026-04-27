document.addEventListener('DOMContentLoaded', function() {
    const configuracion = {
        removeItemButton: true,
        searchPlaceholderValue: 'Buscar...',
        noResultsText: 'No se encontraron resultados',
        itemSelectText: '', 
        shouldSort: false 
    };

    const categoriesChoice = new Choices('#categories_select', configuracion);
    const genresChoice = new Choices('#genres_select', configuracion);
    const tagsChoice = new Choices('#tags_select', configuracion);

    const form = document.getElementById('predict-form');
    
    form.addEventListener('submit', function(evento) {
        evento.preventDefault(); 

        const btnGuardar = document.getElementById('btn-guardar');
        const msgGuardado = document.getElementById('msg-guardado');
        if (btnGuardar && msgGuardado) {
            btnGuardar.disabled = false;
            btnGuardar.textContent = 'Guardar Proyecto';
            msgGuardado.style.display = 'none';
            msgGuardado.textContent = '';
        }
        
        const checkboxes = document.querySelectorAll('.platform-checkbox:checked');
        if (checkboxes.length === 0) {
            alert("¡Atención! Debes seleccionar al menos una plataforma (Windows, Mac o Linux).");
            return;
        }

        const plataformas = Array.from(checkboxes).map(cb => cb.value);

        const categories = categoriesChoice.getValue(true);
        const genres = genresChoice.getValue(true);
        const tags = tagsChoice.getValue(true);
        const allCombinedTags = [...new Set([...categories, ...genres, ...tags])];

        const requestData = {
            price: parseFloat(document.getElementById('price').value),
            min_age: parseInt(document.getElementById('min_age').value),
            release_month: parseInt(document.getElementById('release_month').value),
            num_languages: parseInt(document.getElementById('num_languages').value),
            platforms: plataformas,
            combined_tags: allCombinedTags
        };

        const btnSubmit = form.querySelector('button[type="submit"]');
        const textoOriginal = btnSubmit.innerHTML;
        btnSubmit.innerHTML = "Procesando...";
        btnSubmit.disabled = true;

        fetch('/api/hacer_prediccion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            btnSubmit.innerHTML = textoOriginal;
            btnSubmit.disabled = false;

            if(data.status === "success") {
                
                const contenedorResultados = document.getElementById('resultados-prediccion');
                contenedorResultados.classList.remove('d-none'); 
                
                const prob = data.lgbm.probabilidad_exito;
                document.getElementById('res-probabilidad').innerText = prob + '%';
                document.getElementById('res-nivel').innerText = data.lgbm.nivel;
                document.getElementById('res-usuarios').innerText = data.lgbm.usuarios_estimados.toLocaleString();

                const barra = document.getElementById('res-barra');
                barra.style.width = prob + '%';
                barra.innerText = prob + '%';
                barra.setAttribute('aria-valuenow', prob);
                
                barra.className = 'progress-bar progress-bar-striped progress-bar-animated'; 
                if(prob >= 60) {
                    barra.classList.add('bg-success'); 
                } else if(prob >= 35) {
                    barra.classList.add('bg-warning', 'text-dark'); 
                } else {
                    barra.classList.add('bg-danger'); 
                }

                const knnContainer = document.getElementById('knn-cards-container');
                knnContainer.innerHTML = ''; 
                
                data.knn.forEach(juego => {
                    let plataformasHtml = '';
                    if(juego.windows) plataformasHtml += '<span class="badge bg-primary me-1">Win</span>';
                    if(juego.mac) plataformasHtml += '<span class="badge bg-secondary me-1">Mac</span>';
                    if(juego.linux) plataformasHtml += '<span class="badge bg-dark me-1">Lin</span>';
                    
                    let success_formateado = (juego.success_score || 0).toFixed(1);

                    const cardHtml = `
                        <div class="col-md-4 col-lg-2" style="min-width: 200px;">
                            <div class="card h-100 shadow-sm border-0 text-center px-2 py-3">
                                <h6 class="card-title fw-bold text-truncate" title="${juego.name}">${juego.name}</h6>
                                <div class="mb-2">
                                    ${plataformasHtml}
                                </div>
                                <div class="mt-auto pt-2 border-top">
                                    <span class="badge bg-info text-dark">${juego.tags_coincidentes} tags en común</span>
                                </div>
                            </div>
                        </div>
                    `;
                    knnContainer.innerHTML += cardHtml;
                });

                setTimeout(() => {
                    contenedorResultados.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100); 
            }
        })
        .catch(error => {
            console.error('Error al conectar con el servidor:', error);
            btnSubmit.innerHTML = textoOriginal;
            btnSubmit.disabled = false;
            alert("Ocurrió un error al procesar la predicción.");
        });
    });
});