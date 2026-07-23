import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client

# 1. Load environment variables from .env file
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing Supabase credentials! Please check your .env file.")

# 2. Initialize the Supabase Client
# This client will act as our bridge to the Identity Provider
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Successfully initialized Supabase client.")
except Exception as e:
    raise RuntimeError(f"Failed to initialize Supabase client: {str(e)}")

# 3. Initialize the FastAPI App
app = FastAPI(
    title="Auth Guard API",
    description="A secure CRUD API protected by Supabase JWT Authentication.",
    version="1.0.0"
)

# --- STAGE 0: SERVER & IDENTITY PROVIDER HEALTH CHECK ---

@app.get("/", summary="API Root")
def read_root():
    """Returns basic metadata about the Auth API."""
    return {
        "name": "Auth Guard API",
        "version": "1.0.0",
        "status": "active",
        "identity_provider": "Supabase"
    }

@app.get("/health", summary="Health Check")
def health_check():
    """
    Verifies that the server is alive and successfully connected to Supabase.
    """
    # We ping Supabase by checking our client initialization
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client is not connected.")
    
    return {
        "server": "ok",
        "supabase": "connected",
        "message": "Guard tower operational. Ready to authenticate users."
    }