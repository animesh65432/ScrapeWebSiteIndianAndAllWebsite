# Government Announcement Scraper & Multilingual Translator

A Python-based pipeline to **scrape government announcements**, **normalize content**, and **translate it into multiple Indian languages** using **Ollama (local LLM)** and optional **SerpAPI**. Designed for reliability, async performance, and zero/low-cost infrastructure.

---

## ✨ Features

- 🌐 Scrape static & dynamic websites (HTML, PDFs, SERP-based discovery)
- ⚡ Async networking with `httpx`
- 🤖 Local LLM translations using **Ollama** (Gemma / other models)
- 🗣️ Multi-language support (English, Hindi, Bengali, Tamil, Telugu, etc.)
- 🧠 Government-context–aware translation prompts
- 🗄️ MongoDB integration with duplicate/similarity checks
- 🧩 Modular, extensible architecture

---

## 🧱 Tech Stack

- **Python 3.10+**
- **httpx (async)** – network requests
- **BeautifulSoup4** – HTML parsing
- **Ollama** – For Translations
- **MongoDB / MongoDB Atlas / MongoDB Compass**
- **Groq** – For Classification
- **SerpAPI** – dynamic content scraping
- **FaissService** – vector similarity checks

---

## 📁 Project Structure

```text
.
├── main.py
├── services/
├── Scrapers
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Start Ollama

```bash
ollama serve
ollama pull gemma3:1b
```

> You can change the model in `call_ollama.py`

---

## ⚙️ Configuration

### Ollama

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:1b"
```

## ▶️ Running the Pipeline

```bash
python3 main.py
```

Example output:

```text
🔄 Translating to English...
✅ Successfully translated
🔄 Translating to Hindi...
✅ Successfully translated
✅ All tasks completed successfully!
```

---

## 🧠 Duplicate / Similarity Detection

Uses MongoDB `$text` search or cosine similarity to avoid re-processing already translated announcements.

---

## 🌍 Supported Languages

-English
-Hindi
-Bengali
-Tamil
-Telugu
-Marathi
-Gujarati
-Kannada
-Malayalam
-Punjabi

- (Easily extendable)

---

## 🆓 Free & Low-Cost Friendly

- ✅ Runs fully **offline** with Ollama
- ✅ No paid APIs required
- ⚠️ SerpAPI free tier is optional and rate-limited

---

## 🛠️ Common Issues

### Ollama timeout

Increase timeout in `call_ollama.py`:

```python
timeout=120
```

### SerpAPI 404 / IP issue

Ensure privacy settings allow free-tier access or switch to HTML scraping.

---

## 📌 Roadmap

- [ ] Docker support
- [ ] Scheduler / cron integration
- [ ] Admin dashboard
- [ ] Vector DB (FAISS) similarity

---

## 🤝 Contributing

Pull requests are welcome. Please open an issue for major changes.

---

## 📜 License

MIT License

---

## 👤 Author

**Animesh Dutta**
Full Stack Developer | LLM & Automation

---

> If you want this README customized exactly to your repo files, paste the code or repo link and I’ll refine it.
