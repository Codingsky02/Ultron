# 🤖 ULTRON — Personal AI Voice Assistant

> **A lightweight, modular, voice-controlled AI assistant for Windows, built in Python.**

ULTRON is a personal AI assistant designed to interact with your computer through **natural voice commands**.

It combines **wake-word detection, speech recognition, AI-powered command understanding, and predefined computer-control tools** into a modular Python architecture.

The goal of ULTRON is simple:

**Talk naturally → ULTRON understands → ULTRON performs the action.**

---

## ✨ Features

### 🎙️ Voice Activation

* Custom wake word: **"Hey Jarvis"**
* Continuous wake-word listening
* Activation sound when ULTRON is triggered
* Automatically listens for commands after activation

### 🧠 AI Command Understanding

ULTRON uses Google's Gemini models to understand natural-language commands.

For example:

```text
"Hey Jarvis, please open YouTube."

"Hey Jarvis, what time is it?"

"Hey Jarvis, open Chrome."
```

Instead of requiring strict commands, ULTRON converts natural speech into structured actions.

### 🖥️ Windows Automation

ULTRON currently supports predefined tools for tasks such as:

* Opening applications
* Opening websites
* Checking the time
* Executing supported computer actions

The system uses a **controlled tool architecture** rather than allowing the AI to execute arbitrary code.

### 🗣️ Speech Pipeline

ULTRON's voice pipeline includes:

```text
Microphone
    ↓
Wake Word Detection
    ↓
Activation
    ↓
Speech Recording
    ↓
Gemini Speech / Command Processing
    ↓
Structured Action
    ↓
Tool Manager
    ↓
Windows Action
```

### 🖥️ Graphical Interface

ULTRON includes a CustomTkinter-based interface with:

* Dark futuristic UI
* ULTRON visual interface
* Full-screen / maximized experience
* Responsive window behavior
* Activation state
* Modular frontend architecture

---

# 🏗️ Architecture

ULTRON is divided into separate components so that individual systems can be improved without rewriting the entire assistant.

```text
ULTRON
│
├── Frontend
│   ├── Ui.py
│   └── Static/
│
├── Backend
│   ├── wakeword.py
│   ├── speech.py
│   ├── ai.py
│   └── tools.py
│
└── main.py
```

### Main Components

| Component             | Responsibility                                |
| --------------------- | --------------------------------------------- |
| `main.py`             | Main application loop and system coordination |
| `Frontend/Ui.py`      | ULTRON graphical interface                    |
| `Backend/wakeword.py` | Wake-word detection                           |
| `Backend/speech.py`   | Audio recording and speech processing         |
| `Backend/ai.py`       | AI command interpretation                     |
| `Backend/tools.py`    | Executes predefined actions                   |
| `Frontend/Static/`    | UI assets and activation sounds               |

---

# 🔄 How ULTRON Works

When ULTRON starts, the application initializes its core systems.

```text
1. ULTRON starts
       ↓
2. UI initializes
       ↓
3. Wake-word listener starts
       ↓
4. User says "Hey Jarvis"
       ↓
5. Wake word detected
       ↓
6. Activation sound plays
       ↓
7. ULTRON records the command
       ↓
8. AI interprets the command
       ↓
9. Structured action is generated
       ↓
10. Tool Manager validates the action
       ↓
11. Windows performs the requested task
```

Example:

```text
User:
"Hey Jarvis, open YouTube."

        ↓

Wake Word:
"Hey Jarvis"

        ↓

AI:
{
    "action": "open_website",
    "target": "youtube"
}

        ↓

Tool Manager:
open_website("youtube")

        ↓

Browser:
YouTube opens
```

---

# 🧠 AI Architecture

ULTRON does **not** give the AI unrestricted access to the computer.

Instead, the AI produces a structured command that is handled by ULTRON's tool system.

For example:

```json
{
    "action": "open_website",
    "target": "youtube"
}
```

The Tool Manager then decides whether that action is supported.

This approach provides a cleaner separation between:

```text
AI Reasoning
     ↓
Action Selection
     ↓
Tool Execution
```

This architecture also makes it easier to add new capabilities safely.

---

# 🛠️ Technology Stack

### Programming Language

**Python**

### AI

**Google Gemini**

Used for natural-language understanding and speech/command processing.

### Wake Word

**OpenWakeWord**

Used to detect the custom activation phrase.

### Audio

* `sounddevice`
* `soundfile`

Used for microphone input and temporary audio processing.

### GUI

**CustomTkinter**

Used to create the ULTRON interface.

### Image Processing

**Pillow**

Used for UI images and visual assets.

### Runtime

Designed primarily for:

**Windows 10 / Windows 11**

---

# 📦 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ultron.git
cd ultron
```

## 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Configuration

ULTRON requires access to the AI service used by the project.

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

> **Never commit your API key to GitHub.**

Make sure `.env` is included in `.gitignore`.

Example:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

# ▶️ Running ULTRON

After installing the dependencies and configuring your API key:

```bash
python main.py
```

ULTRON will initialize its interface and begin listening for the wake word.

Say:

```text
Hey Jarvis
```

Then give your command.

---

# 🎤 Example Commands

### Open a website

```text
Hey Jarvis, open YouTube.
```

### Open an application

```text
Hey Jarvis, open Chrome.
```

### Ask for the time

```text
Hey Jarvis, what time is it?
```

ULTRON is designed to understand natural variations of supported commands rather than requiring one exact sentence.

---

# 📁 Project Structure

```text
ultron/
│
├── Backend/
│   ├── __init__.py
│   ├── ai.py
│   ├── speech.py
│   ├── tools.py
│   └── wakeword.py
│
├── Frontend/
│   ├── __init__.py
│   ├── Ui.py
│   └── Static/
│       ├── Activation.wav
│       └── ...
│
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
└── .env
```

---

# 🔐 Safety & Design Philosophy

ULTRON is intentionally designed around **controlled actions**.

The AI does not directly receive unrestricted access to the operating system.

Instead:

```text
Natural Language
       ↓
AI
       ↓
Structured Command
       ↓
Validation
       ↓
Supported Tool
       ↓
Action
```

This makes the system easier to debug, extend, and control.

---

# 🚧 Current Limitations

ULTRON is an actively developed project.

Current limitations may include:

* Wake-word detection can occasionally produce false activations.
* Speech recognition depends on microphone quality and background noise.
* AI interpretation depends on the configured Gemini model/API.
* Only predefined tools are available.
* Windows-specific functionality limits portability to other operating systems.
* Some dependencies may require additional configuration depending on the Python version and system environment.

---

# 🗺️ Roadmap

Future versions may introduce:

### Voice

* [ ] Better speech detection
* [ ] Improved command confirmation
* [ ] More natural responses
* [ ] Faster voice pipeline

### AI

* [ ] Better intent detection
* [ ] Context-aware conversations
* [ ] Conversation memory
* [ ] Improved error recovery

### Computer Control

* [ ] More Windows applications
* [ ] System controls
* [ ] File operations
* [ ] Media controls
* [ ] More browser actions

### Interface

* [ ] Improved animations
* [ ] Voice activity visualization
* [ ] System status indicators
* [ ] More responsive UI

### Architecture

* [ ] Better plugin/tool architecture
* [ ] Improved logging
* [ ] Automated testing
* [ ] Configuration system
* [ ] Performance optimization

---

# 📈 Version History

## v1.57 — Current Development

ULTRON continues development toward a more polished and reliable voice-command loop.

### Previous milestone

## v1.47 — Real Voice Command Engine

Introduced the core real-world voice command pipeline.

Key components included:

* Voice command recording
* AI-powered command interpretation
* Structured actions
* Tool execution
* Improved main application loop

Example flow:

```text
Wake Word
   ↓
Voice Recording
   ↓
AI Processing
   ↓
Command
   ↓
Tool
   ↓
Action
```

---

# 🤝 Contributing

ULTRON is primarily a personal development project, but suggestions, bug reports, and improvements are welcome.

If you find a bug:

1. Reproduce the issue.
2. Check the terminal output/logs.
3. Open an issue with:

   * What you expected
   * What actually happened
   * Error message
   * Python version
   * Windows version

---

# ⚠️ Disclaimer

ULTRON is an experimental personal AI assistant.

It is not intended to replace system security software or provide unrestricted autonomous control over a computer.

Use automation features responsibly.

---

# 👨‍💻 Author

**Vansh**

Student developer building ULTRON as a long-term Python + AI project.

GitHub:

`https://github.com/YOUR_USERNAME`

---

# ⭐ Project

If you find ULTRON interesting, consider giving the repository a ⭐.

```text
ULTRON
Personal AI Voice Assistant
Built with Python + AI + Voice
```

> **"Systems are operational. Awaiting your command."**

