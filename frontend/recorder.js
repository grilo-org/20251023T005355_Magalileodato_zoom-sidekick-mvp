/**
 * recorder.js - Captura áudio e envia para FastAPI
 * -------------------------------------------------
 * Funcionalidades:
 * 1. Captura do microfone usando MediaRecorder API.
 * 2. Envio do áudio para o backend FastAPI via POST.
 * 3. Atualiza transcrição, resumo e toca áudio da próxima pergunta.
 */

let mediaRecorder;
let audioChunks = [];

const recordButton = document.getElementById("record-btn");
const transcriptionDiv = document.getElementById("transcription");
const summaryDiv = document.getElementById("summary");
const audioPlayer = document.getElementById("next-question-audio");

// URL do backend FastAPI
const BACKEND_URL = "http://127.0.0.1:8000";

async function initMicrophone() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
            audioChunks = [];
            recordButton.disabled = true; // desabilita enquanto envia
            await sendAudio(audioBlob);
            recordButton.disabled = false;
        };
    } catch (error) {
        console.error("Erro ao acessar microfone:", error);
        alert("Não foi possível acessar o microfone.");
    }
}

async function sendAudio(audioBlob) {
    const formData = new FormData();
    formData.append("audio", audioBlob, "response.webm");

    try {
        const response = await fetch(`${BACKEND_URL}/answer`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Erro ao enviar áudio: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();

        // Atualiza a interface com a transcrição e resumo
        transcriptionDiv.textContent = data.transcription || "Sem transcrição";
        summaryDiv.textContent = data.summary || "Sem resumo";

        // Reproduz o áudio da próxima pergunta
        if (data.next_question_audio) {
            audioPlayer.src = `${BACKEND_URL}/play_audio/${data.next_question_audio}`;
            audioPlayer.play();
        }

    } catch (error) {
        console.error("Erro ao processar áudio:", error);
        alert("Ocorreu um erro ao processar a resposta.");
    }
}

recordButton.addEventListener("click", () => {
    if (!mediaRecorder) {
        alert("Microfone não inicializado");
        return;
    }

    if (mediaRecorder.state === "inactive") {
        mediaRecorder.start();
        recordButton.textContent = "Parar Gravação";
    } else if (mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        recordButton.textContent = "Iniciar Gravação";
    }
});

window.addEventListener("DOMContentLoaded", initMicrophone);
