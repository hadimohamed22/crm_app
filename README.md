# 🚀 CRM App

A **FastAPI-based** CRM application with a reusable `core` module.

---

## 📦 **Setup**

### 1️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2️⃣ **Initialize the Database**
```bash
python -m src.models.db_init
```

---

## ▶️ **Running the App**

### **Development Mode (with auto-reload)**
Run the following command to start the application in development mode:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```
Alternatively, you can also run:
```bash
python -m src.run_dev
```

### **Production Mode**
To run the application in production mode:
```bash
python -m src.main
```

---

## 📜 **API Documentation**
FastAPI provides interactive API documentation:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc UI**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🛠 **Configuration**
Move key parameters and constants to a **config file** to improve maintainability. Modify database connection settings and environment variables as needed.

---

### ✅ **Features**
- FastAPI-based backend
- PostgreSQL as the database
- Swagger & Redoc API documentation
- Structured and modular project design

---

**Enjoy building with FastAPI! 🚀**

