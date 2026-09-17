
# 🔬 ResearchMind AI

### Multi-Agent AI Research Assistant

ResearchMind AI is a multi-agent research assistant that uses artificial intelligence to search the web, extract useful information, read online sources, generate research reports, and review the final report.

## 🚀 Features

- 🔎 AI-powered web search
- 🔗 Automatic source URL extraction
- 📖 Webpage reading using a Reader Agent
- ✍️ Automated research report generation
- 🧐 AI-powered report criticism
- 🌐 Interactive Streamlit interface
- 📥 Downloadable research reports

## 🏗️ Project Architecture

```text
User enters a topic
        │
        ▼
   Search Agent
        │
        ▼
  Source Extraction
        │
        ▼
   Reader Agent
        │
        ▼
   Writer Agent
        │
        ▼
   Critic Agent
        │
        ▼
 Final Research Report
```

## 🛠️ Technologies Used

- Python
- LangChain
- LangGraph
- Groq
- Tavily
- Streamlit
- BeautifulSoup
- Requests

## 📂 Project Structure

```text
Multi Agent AI System/
│
├── agents.py
├── app.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/amankumar6387/multi-agent-research-system.git
cd multi-agent-research-system
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Do not upload your `.env` file to GitHub.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open at:

```text
http://localhost:8501
```

## 🔄 How It Works

1. The Search Agent searches for relevant information.
2. The system extracts source URLs.
3. The Reader Agent reads selected web sources.
4. The Writer Agent generates a structured report.
5. The Critic Agent evaluates the report.

## 👨‍💻 Author

**Aman Kumar**

B.Tech Computer Science and Engineering

GitHub: [amankumar6387](https://github.com/amankumar6387)

## 📄 License

This project is intended for educational and research purposes.