# Backend - FastAPI
Run locally:
```bash
pip install -r requirements.txt
cp .env.example .env     # update credentials
uvicorn app.main:app --reload --port 8000
```
This seeds a default admin: `admin` / `admin123` if table is empty.
