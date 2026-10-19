# 🩸 AI-Powered Blood Report Analyzer

An interactive healthcare-focused prototype that uses **Google Gemini's multimodal AI** to help users understand information in blood test reports through readable summaries and general dietary guidance.

## ✨ Features

- **Report Input:** Paste blood report text or upload a report image.
- **AI-Powered Extraction:** Uses a vision-capable Gemini model to interpret supported report images and identify laboratory values.
- **Readable Summaries:** Presents extracted results in a more accessible format.
- **Reference-Range Context:** Organizes reported values, units, reference ranges, and status where available in the report.
- **General Dietary Guidance:** Generates general food suggestions, including an Indian-food context.
- **Interactive Interface:** Built with Streamlit for a simple, browser-based user experience.

## 🛠️ Tech Stack

- **Language:** Python
- **Frontend:** Streamlit
- **AI Model:** Google Gemini (`gemini-2.5-flash`)
- **AI Integration:** LangChain and `langchain-google-genai`
- **Configuration:** `python-dotenv`

## 📁 Project Structure

```text
blood-work-analyzer/
├── app.py
├── analyzer.png
├── requirements.txt
└── .gitignore
```

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ananion1/blood-work-analyzer.git
cd blood-work-analyzer
```

### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key

Create a `.env` file in the project root:

```text
GOOGLE_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own API key. Keep `.env` private and never commit it to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

The application should open in your browser. If it doesn't, follow the local URL shown in your terminal.

## 🔒 Privacy, Safety and Limitations

- This project is an educational prototype, not a medical device or diagnostic system.
- AI-generated summaries and dietary suggestions may be incomplete or incorrect.
- Laboratory results should be interpreted by a qualified healthcare professional in the context of symptoms, medical history, and appropriate reference ranges.
- Do not use this application to make medical decisions or change medication or treatment.
- Avoid uploading identifiable medical reports or sensitive personal health information to an AI service unless you understand and have consent for the applicable data handling.

## 🚀 Future Improvements

- Add a downloadable summary report.
- Improve handling of unclear scans and missing reference ranges.
- Add input validation and clearer error messages.
- Develop a more comprehensive test suite.
- Explore deployment with Streamlit Community Cloud.

## 👩‍💻 Author

**Ananya**

Built as a learning project exploring generative AI, multimodal input processing, Python, and interactive application development.

---

*This project is intended for educational and informational purposes only. It does not replace professional medical advice.*
