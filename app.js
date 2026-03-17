let currentChallenge = null;
let selectedOption = null;

async function fetchChallenge() {
    const container = document.getElementById('challenge-container');
    const progress = document.getElementById('progress');
    document.getElementById('challenge-container').innerHTML = '<div class="animate-pulse text-center">Cargando nuevo reto...</div>';

    // Reset de estado
    selectedOption = null;
    progress.style.width = "15%";

    try {
        const response = await fetch('/api/challenge');
        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        currentChallenge = data;
        renderChallenge(data);
        progress.style.width = "40%";
    } catch (error) {
        console.error("Error:", error);
        container.innerHTML = `
            <div class="text-center p-8 bg-red-900/20 rounded-2xl border border-red-500/50">
                <i class="fa-solid fa-triangle-exclamation text-red-500 text-4xl mb-4"></i>
                <p class="text-red-200 font-bold">La IA está descansando</p>
                <button onclick="fetchChallenge()" class="mt-4 text-sm underline opacity-70 hover:opacity-100">Reintentar</button>
            </div>`;
    }
}

function renderChallenge(data) {
    const container = document.getElementById('challenge-container');
    container.innerHTML = `
        <div class="fade-in">
            <h2 class="text-2xl font-bold mb-6">${data.question || 'Selecciona la opción correcta:'}</h2>
            
            <div class="bg-gray-800/50 p-8 rounded-3xl mb-8 border-2 border-gray-700 shadow-xl">
                <p class="text-2xl text-center font-medium leading-relaxed">
                    ${data.content}
                </p>
            </div>

            <div id="options-grid" class="space-y-3">
                ${data.options.map((opt, i) => `
                    <button onclick="select(${i})" class="option-btn" id="opt-${i}">
                        <div class="flex items-center gap-4">
                            <span class="w-8 h-8 rounded-lg bg-gray-700 flex items-center justify-center text-sm font-bold">${i + 1}</span>
                            ${opt}
                        </div>
                    </button>
                `).join('')}
            </div>
        </div>
    `;
}

function select(index) {

    document.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('selected'));


    const btn = document.getElementById(`opt-${index}`);
    if (btn) btn.classList.add('selected');

    selectedOption = index;
}

function checkAnswer() {
    const btn = document.getElementById('action-btn');

    if (selectedOption === null) {

        btn.classList.add('bg-red-500', 'border-red-700');
        setTimeout(() => btn.classList.remove('bg-red-500', 'border-red-700'), 500);
        return;
    }


    const isCorrect = selectedOption === currentChallenge.answer;
    const progress = document.getElementById('progress');

    if (isCorrect) {
        progress.style.width = "100%";
        alert("✨ ¡Excelente! Respuesta correcta.");
    } else {
        alert(`❌ ¡Casi! La respuesta correcta era: ${currentChallenge.options[currentChallenge.answer]}`);
    }


    fetchChallenge();
}


window.onload = fetchChallenge;