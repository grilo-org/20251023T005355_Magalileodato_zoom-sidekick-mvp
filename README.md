# 🎯 Zoom Sidekick MVP

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.99-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT-blueviolet)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Status](https://img.shields.io/badge/Status-MVP-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)


## 🚀 Descrição do Projeto

O **Zoom Sidekick MVP** é uma solução de **entrevista automatizada com IA**, capaz de:

* 🎙️ Capturar áudio do usuário em tempo real
* 📝 Transcrever respostas (STT - Whisper)
* 🧠 Resumir respostas (GPT - OpenAI)
* 🔊 Gerar áudio da próxima pergunta (TTS - gTTS)
* 🤖 Conduzir entrevistas completas de forma automatizada

> MVP funcional, com **backend modular** e **frontend responsivo**, pronto para integração com Zoom ou Google Meet.


## 🗂 Estrutura do Projeto

```bash
zoom-sidekick-mvp/
├── backend/
│   ├── transcription.py                 # Processamento de áudio auxiliar
│   ├── app/
│   │   ├── main.py                      # Entry point FastAPI
│   │   ├── routes.py                    # Endpoints da API
│   │   ├── services/
│   │   │   ├── stt_service.py           # 🎙️ Áudio → Texto (Whisper)
│   │   │   ├── tts_service.py           # 🔊 Texto → Áudio (gTTS)
│   │   │   ├── summary_service.py       # 🧠 Resumo de respostas (GPT)
│   │   │   └── bot_service.py           # 🤖 Orquestra o fluxo da entrevista
│   │   └── utils/
│   │       ├── logger.py                # Logs estruturados
│   │       └── config.py                # Configurações globais da aplicação
│   ├── tests/
│   │   └── __init__.py                  # Inicializa o pacote de testes
│   ├── requirements.txt                 # Dependências do backend
│   └── Dockerfile                       # Configuração do container backend
├── frontend/
│   ├── index.html                        # Interface do usuário
│   ├── recorder.js                       # Captura áudio
│   └── style.css                         # Estilo moderno e responsivo
├── .env.example                          # Variáveis de ambiente de exemplo
├── .gitignore                            # Arquivos ignorados
├── docker-compose.yml                     # Orquestração de containers
└── README.md                              # Documentação
```

## ⚙️ Tecnologias Utilizadas

| Serviço     | Tecnologia              | Função                                  |
| ----------- | ----------------------- | --------------------------------------- |
| STT 🎙️      | Whisper (OpenAI)        | Transcrição de áudio                    |
| TTS 🔊      | gTTS                    | Conversão de texto em áudio             |
| Resumo 🧠   | OpenAI GPT              | Resumir respostas do candidato          |
| Backend 🖥️  | Python 3.11 + FastAPI   | API rápida e modular                    |
| Frontend 🌐 | HTML5, CSS3, JS         | Captura áudio e interação com o usuário |
| Deploy 🐳   | Docker & Docker Compose | Containerização                         |

## Instalação de Dependências

O projeto tem suporte a Windows e Linux/Mac.
Escolha o arquivo de requirements correspondente ao seu sistema:

Windows (CPU only)

Instalação:

pip install -r requirements-windows.txt


Exemplo de requirements-windows.txt:

# Backend
fastapi==0.103.2
uvicorn[standard]==0.23.2
pydantic==2.5.1

# OpenAI / IA
openai==1.32.0
whisper==1.1.10
torch==2.3.1         # CPU / Windows

# TTS
gTTS==2.3.2

# Manipulação de áudio
pydub==0.25.1
ffmpeg-python==0.2.0
soundfile==0.12.1

# Utilitários
python-dotenv==1.0.1
loguru==0.7.0
requests==2.31.0

Linux / WSL / Mac

Instalação:

pip install -r requirements-linux.txt


Exemplo de requirements-linux.txt:

# Backend
fastapi==0.103.2
uvicorn[standard]==0.23.2
pydantic==2.5.1

# OpenAI / IA
openai==1.32.0
whisper==1.1.10
torch==2.3.1         # Linux/Mac (CPU por padrão)
# Para suporte CUDA/GPU, consulte a documentação do PyTorch

# TTS
gTTS==2.3.2

# Manipulação de áudio
pydub==0.25.1
ffmpeg-python==0.2.0
soundfile==0.12.1

# Utilitários
python-dotenv==1.0.1
loguru==0.7.0
requests==2.31.0


⚠️ Observação:

No Windows, a versão usada do torch é apenas para CPU.

No Linux/Mac você pode instalar suporte a GPU caso tenha CUDA disponível.


## 📈 Fluxo da Entrevista

```mermaid
flowchart TD
    A[Usuário inicia entrevista] --> B[Bot faz pergunta via TTS 🔊]

    B --> C[Usuário responde via microfone 🎙️]

    C --> D[STT: Transcreve áudio para texto 📝]

    D --> E[Summary: Resume resposta 🧠]

    E --> F[Próxima pergunta do bot 🔊]

    F --> B

    F --> G[Fim da entrevista]
```

💡 Fluxo contínuo até todas as perguntas serem feitas.
Cada resposta é transcrita, resumida e o bot segue o próximo passo automaticamente.


## 🏃‍♂️ Como Rodar o Projeto

### 📥 Clone o repositório

```bash
git clone https://github.com/magali-leodato/zoom-sidekick-mvp.git
cd zoom-sidekick-mvp
```

### 📄 Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e configure:

```bash
OPENAI_API_KEY=your_openai_api_key
```

### 🔧 Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend disponível em: 👉 `http://localhost:8000`

### 🎨 Frontend

```bash
cd frontend
```

Abra `index.html` no navegador ou use a extensão **Live Server** no VSCode.

### 🐳 Docker (opcional)

```bash
docker-compose up --build
```

## 🧪 Testes

Para rodar os testes unitários:

```bash
pytest backend/tests/
```


## 📦 requirements.txt (backend)

Seu arquivo já está atualizado, mas certifique-se de conter pelo menos:

fastapi==0.99.0
uvicorn[standard]
openai
gtts
pytest
python-dotenv
```

Se estiver usando Whisper localmente, adicione:

```
whisper
```

E se estiver rodando em Docker, lembre-se de incluir também:

```
gunicorn
```

## 🔜 Próximos Passos

* 📹 Captura de áudio diretamente do Zoom / Google Meet

* 🎨 Melhorar UI/UX com feedback visual em tempo real

* 🔒 Adicionar autenticação e sessões de usuário

* 🗄️ Persistir respostas em banco de dados

* ✉️ Funções de follow-up (enviar e-mails, criar tarefas)


## 📹 Demonstração do MVP


[![▶ Assista ao vídeo](https://img.youtube.com/vi/ymPnv9S1TAE/0.jpg)](https://youtu.be/ymPnv9S1TAE)



## 👩‍💻 Desenvolvedor(a)

**Magali Leodato**

🔗 [LinkedIn](http://www.linkedin.com/in/magali-santos-leodato)
💻 [GitHub](http://github.com/magali-leodato)


## 📜 Licença

Este projeto está sob a licença MIT.
Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

