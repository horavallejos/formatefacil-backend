from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Inicializar FastAPI
app = FastAPI(title="FormateFácil API", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ENDPOINTS

@app.get("/")
async def root():
    return {"message": "FormateFácil API Running 🚀"}

# 1. GET all courses
@app.get("/api/courses")
async def get_courses():
    try:
        response = supabase.table("courses").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. GET specific course
@app.get("/api/courses/{course_id}")
async def get_course(course_id: str):
    try:
        response = supabase.table("courses").select("*").eq("course_id", course_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Course not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. POST save lead
@app.post("/api/leads")
async def save_lead(email: str, name: str, phone: str, course_id: str):
    try:
        response = supabase.table("leads").upsert({
            "email": email,
            "name": name,
            "phone": phone,
            "course_id": course_id
        }).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. POST Hotmart webhook
@app.post("/api/webhooks/hotmart")
async def hotmart_webhook(email: str, course_id: str, transaction_id: str):
    try:
        response = supabase.table("purchases").insert({
            "email": email,
            "course_id": course_id,
            "hotmart_transaction_id": transaction_id,
            "status": "completed"
        }).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
