
# 🧠 AI Skill Gap Analysis

This project is a **Django-based web application** designed to analyze the **skill gap between job requirements and an individual's current skills**. It recommends personalized **AI-generated courses** to bridge that gap using **Natural Language Processing (NLP)** and **machine learning** techniques.

---

## 🚀 Features

- 🔐 **User Authentication** – Register, Login, and Manage Profile  
- 🧩 **Skill Analysis** – Upload or input skills to analyze AI-detected gaps  
- 🎯 **Course Recommendations** – Get smart course suggestions from dataset  
- 📊 **Dashboard** – Visual overview of progress and insights  
- 📁 **Database Seed Script** – Auto-seed job roles and courses data  
- 🌐 **Responsive Frontend** – Clean HTML + Django templates  

---

## 🗂️ Project Structure

```

AI_SKILL_GAP_ANALYSIS/
│
├── ai_skill_gap/                 # Django project directory
│   ├── **init**.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                         # Core app containing logic and data
│   ├── **init**.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── utils.py
│   ├── views.py
│   │
│   ├── data/                     # Datasets for job roles and courses
│   │   ├── course_data.csv
│   │   └── job_roles.csv
│   │
│   ├── management/commands/      # Custom Django commands
│   │   └── seed_job_roles.py
│   │
│   ├── migrations/
│   └── static/images/            # Static assets
│
├── templates/                    # HTML templates
│   ├── base.html
│   ├── course_recommendations.html
│   ├── dashboard.html
│   ├── login.html
│   ├── my_profile.html
│   ├── register.html
│   └── skill_analysis.html
│
├── media/                        # Uploaded media files (if any)
│
├── venv/                         # Virtual environment (not uploaded to GitHub)
│
├── db.sqlite3                    # SQLite database
│
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── Design.png                    # Project design or mockup image
└── README.md                     # You are here 😄

````

---

## ⚙️ Installation & Setup Guide

Follow these steps to set up the project locally:

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/AI_SKILL_GAP_ANALYSIS.git
cd AI_SKILL_GAP_ANALYSIS
````

### 2️⃣ Create and Activate Virtual Environment

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Seed Initial Job Roles & Courses Data

```bash
python manage.py seed_job_roles
```

### 6️⃣ Run the Development Server

```bash
python manage.py runserver
```

Then open your browser and go to 👉
**[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🧠 Tech Stack

* **Backend:** Django 5.1
* **Frontend:** HTML, CSS (Django Templates)
* **Database:** SQLite
* **Libraries Used:**

  * pandas, numpy, scikit-learn, nltk
  * transformers, sentence-transformers
  * torch, openai, PyPDF2
  * tqdm, regex, requests


---

## 🧩 Core Functionalities Overview

| Feature                | Description                                                 |
| ---------------------- | ----------------------------------------------------------- |
| **Skill Analysis**     | Compares user-entered skills with job role data from CSV    |
| **Recommendations**    | Suggests best-fit online courses using NLP-based similarity |
| **Profile Management** | Users can update skill sets and preferences                 |
| **Data Handling**      | Uses Pandas for dataset management and analysis             |
| **AI Integration**     | Uses Sentence Transformers for semantic matching            |

---

## 💡 Future Enhancements

* Add user dashboard analytics with charts
* Integrate real-time AI course fetching using APIs
* Improve UI with Bootstrap or Tailwind CSS
* Deploy on Render / Google Cloud

---
