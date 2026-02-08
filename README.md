# 📌 REAL AI-Based Smart Attendance System

An **AI-powered Smart Attendance System** built with Django and Face Recognition that allows faculty to mark attendance automatically by capturing classroom images through a camera. The system detects student faces, matches them with stored images, and securely stores the attendance status as present/absent in the database.

---

## 🚀 Features

- 🔐 **Secure Login System** for Faculty/Admin  
- 🧑‍🏫 Class-wise and Subject-wise Attendance Management  
- 📷 Camera-based Attendance using Face Recognition  
- 🤖 AI-powered Face Detection and Face Matching  
- 🟢 Automatic Present / Absent Marking  
- 🗂️ Single Attendance Session Lock (Prevents duplicate attendance)  
- 📊 Dashboard with Attendance Statistics and summaries  
- 🗃️ Support for production-ready relational databases (e.g., PostgreSQL)  

---

## 🛠️ Tech Stack

### Frontend  
- HTML5  
- CSS3  
- JavaScript (Camera / Media APIs)

### Backend  
- Python  
- Django (3.x/4.x/5.x as per project setup)

### AI / ML  
- OpenCV  
- `face_recognition`  
- `dlib`  
- NumPy  

### Database  
- PostgreSQL (recommended) or other Django-supported databases  

### Tools  
- Anaconda / Virtual Environment  
- Git & GitHub  
- VS Code / PyCharm (optional)

---

## 📂 Project Structure

```bash
REAL-AI-BASED-SMART-ATTENDANCE-SYSTEM/
│
├── backend/
│   ├── ai/
│   │   └── face_ai.py          # Face detection & recognition logic
│   ├── migrations/             # Django migrations
│   ├── templates/              # HTML templates
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   └── attendance.html
│   ├── static/                 # CSS, JS, images (if configured)
│   ├── models.py               # Database models (Student, Attendance, etc.)
│   ├── views.py                # View functions / class-based views
│   ├── urls.py                 # URL routing
│   └── settings.py             # Django settings
│
├── manage.py
├── requirements.txt
└── README.md
```

*(Adjust folders/files above if your actual structure differs.)*

---

## ⚙️ How to Run This Project Locally

Follow these steps to set up and run the project on your system.

### ✅ Step 1: Clone the Repository

```bash
git clone https://github.com/sandeepkumar9760/REAL-AI-BASED-SMART-ATTENDANCE-SYSTEM.git
cd REAL-AI-BASED-SMART-ATTENDANCE-SYSTEM
```

### ✅ Step 2: Create & Activate Virtual/Conda Environment

Using Conda (recommended):

```bash
conda create -n ai310 python=3.10 -y
conda activate ai310
```

> ⚠️ **Note:** Python 3.10 is generally preferred for smooth installation of `dlib` and `face_recognition`.

Or using `venv`:

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### ✅ Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If `dlib` fails on Windows, try:

```bash
conda install -c conda-forge dlib
pip install face_recognition opencv-python numpy pillow psycopg2-binary
```

### ✅ Step 4: Configure Database (PostgreSQL Example)

In `backend/settings.py`, configure your database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'attendance_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

- Make sure PostgreSQL is installed and running.  
- Create the database `attendance_db` (or update the name above).

### ✅ Step 5: Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### ✅ Step 6: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### ✅ Step 7: Run the Development Server

```bash
python manage.py runserver
```

Open the application in your browser:

- http://127.0.0.1:8000/  

Admin panel (if configured in `urls.py`):

- http://127.0.0.1:8000/admin/

---

## 📷 How Camera-Based Attendance Works

1. Faculty logs in and selects **Class** and **Subject**.  
2. Faculty clicks on **"Take Attendance via Camera"**.  
3. The system captures a classroom image using the connected camera.  
4. The AI module detects faces and generates face encodings.  
5. Encodings are compared with stored student face encodings.  
6. Matching faces are marked **Present**, non-detected students are **Absent**.  
7. Attendance for that session is saved in the database with time and metadata.

---

## 🧠 AI Logic (High-Level Overview)

- Each student has one or more reference face images stored in the system.  
- During registration/enrollment, **face encodings** are generated using `face_recognition` and stored.  
- When a classroom photo is captured, the system:  
  - Detects all faces in the frame.  
  - Generates encodings for each detected face.  
  - Compares them with stored encodings using a similarity threshold.  
- If a match is found, the corresponding student is marked **Present** for that session; otherwise, they remain **Absent**.  

This approach combines **computer vision** and **feature-based face recognition** to automate attendance marking.

---

## 🧪 Sample Test Credentials

You can configure your own, but for demo purposes you may use something like:

- Username: `admin`  
- Password: `admin123`  

> 🔐 Make sure to change credentials in a real deployment.

---

## 🧾 Viva / Interview One-Liner

> "The system uses computer vision and face recognition to detect and identify student faces from a classroom image and automatically records their attendance in real time using Django and AI."

---

## 🔮 Future Enhancements

- 📊 Detailed Attendance Analytics & Report Generation (per student, per class, per subject)  
- 📩 Email / SMS Alerts to Parents for low attendance  
- 📱 Mobile Camera / Mobile App Support  
- 🎭 Mask Detection / Liveness Detection  
- ☁️ Cloud Deployment on AWS / Azure / GCP  
- 🧾 Export attendance as Excel/CSV/PDF  

---

## 👨‍💻 Author

**Sandeep Kumar**  
REAL AI-Based Smart Attendance System – AI Project  
Lovely Professional University  

---

## ⭐ Support

- If you find this project helpful, consider giving it a ⭐ on GitHub.  
- Feel free to **fork** the repo, open **issues**, or submit **pull requests** for improvements.
