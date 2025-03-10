# CRM App
A FastAPI-based CRM application with a reusable `core` module.

## Setup
1. Install dependencies: `pip install -r requirements.txt`

## Running the App
- **Development Mode (with auto-reload)**:
  ```bash
  uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
  ```
  or
   ```bash
  python -m src.run_dev
  ```
- **Production Mode**:
  ```bash
  python -m src.main
  ```
