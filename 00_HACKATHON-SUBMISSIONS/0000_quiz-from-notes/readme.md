Quiz from Notes - README

📘 Quiz from Notes

An AI-powered application that generates quizzes from your uploaded notes (PDFs or text).  
It helps students and educators quickly create practice questions for revision.



## 🚀 Features
- Upload notes (PDF/text) and auto-generate quizzes.
- AI-powered question generation.
- Clean and responsive frontend (React + Vite).
- Flask-based backend with PDF parsing utilities.
- Easy to deploy and extend.



## 🛠️ Tech Stack
- **Frontend:** React, Vite, JavaScript
- **Backend:** Python, Flask
- **Libraries:** PyMuPDF / pdfminer, Flask-CORS, dotenv
- **Other:** Node.js, npm



## 📂 Project Structure
0000_quiz-from-notes/
│── frontend/       # React + Vite frontend
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
│── backend/        # Flask backend
│   ├── quiz_generator.py
│   ├── pdf_utils.py
│   ├── storage.py
│   └── app.py
│
│── README.md       # Project documentation


## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/quiz-from-notes.git
cd quiz-from-notes
```

### 2. Backend Setup
```bash
cd backend
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
pip install -r requirements.txt
flask run
```
Backend will start at `http://127.0.0.1:5000/`

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend will start at `http://127.0.0.1:5173/`


## 🖥️ Usage
1. Start both backend and frontend servers.  
2. Open the frontend in your browser.  
3. Upload a PDF/text file with notes.  
4. The system will generate quiz questions for practice.


## 📌 Future Improvements
- Export quizzes as PDF/CSV.  
- Add multiple-choice and short-answer options.  
- Authentication for saving user progress.  


## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss.  


## 📄 License
This project is licensed under the MIT License.


