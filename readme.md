# Government Announcement Scraper & Multilingual Translator

A Python-based pipeline to **scrape government announcements**, **normalize content**, and **translate it into multiple Indian languages** using **ai4bharat** and optional **Aws(Ec2)**. Designed for reliability, async performance, and zero/low-cost infrastructure.

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
- **MongoDB / MongoDB Atlas / MongoDB Compass**
- **Groq** – For Classification
- **FaissService** – vector similarity checks
- **Aws Ec2 / Local Machine** – hosting
- **seleunium** - for dynamic website scraping
- **ai4bharat** - for multilingual translation

---

## 📁 Project Structure

```text

├── services/ (all service related code)
├── Scrapers (Mostly state wise scraper code)
├── requirements.txt
├── InsertAnnoucments (All states to insert annoucments to mongodb)
├── prompts (All prompt related code)
├── utils (all utility code)
├── config
├── .github/workflows
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

```bash
python3  Scrape.WEST_INDIA (Based on your Which state want to scarpe choice).py
```

## 🧠 Duplicate / Similarity Detection

Uses paraphrase-mpnet-base-v2 from Sentence Transformers to compute embeddings and Faiss for similarity search to avoid duplicate announcements.

---

## 🌍 Supported Languages

-English
-Assamese
-Bengali
-Bodo
-Dogri
-Gujarati
-Hindi
-Kannada
-Kashmiri
-Maithili
-Malayalam
-Manipuri (Meitei)
-Marathi
-Nepali
-Odia
-Punjabi
-Sanskrit
-Santali
-Sindhi
-Tamil
-Telugu
-Urdu

- (Easily extendable)

---

## 🆓 Free & Low-Cost Friendly

- ✅ No paid APIs required

---

## 🤝 Contributing

Pull requests are welcome. Please open an issue for major changes.

---

## 📜 License

MIT License

---

## 👤 Author

**Animesh Dutta**
