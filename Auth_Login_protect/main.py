import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from supabase import create_client, Client

# 1. Load secrets and initialize Supabase
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing Supabase credentials! Please check your .env file.")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    raise RuntimeError(f"Failed to initialize Supabase client: {str(e)}")

# 2. Initialize FastAPI App
app = FastAPI(
    title="Auth Guard API",
    description="A secure CRUD API protected by Supabase JWT Authentication.",
    version="1.0.0"
)

# --- STAGE 0: HEALTH CHECKS ---

@app.get("/", summary="API Root")
def read_root():
    """Returns basic API metadata."""
    return {"name": "Auth Guard API", "version": "1.0.0", "status": "active"}

@app.get("/health", summary="Health Check")
def health_check():
    """Verifies server and Identity Provider connectivity."""
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client is not connected.")
    return {"server": "ok", "supabase": "connected"}

# --- STAGE 1: OPEN AUTH ENDPOINTS (SIGN UP & LOG IN) ---

@app.post("/auth/signup", status_code=201, summary="Create a new user account")
def sign_up(payload: dict):
    """Registers a new user with Supabase Auth."""
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password or not str(email).strip() or not str(password).strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required and cannot be empty."}
        )

    try:
        response = supabase.auth.sign_up({
            "email": str(email).strip(),
            "password": str(password).strip()
        })
        user_data = {
            "id": response.user.id if response.user else None,
            "email": response.user.email if response.user else email,
            "created_at": str(response.user.created_at) if response.user else None
        }
        return JSONResponse(
            status_code=201, 
            content={"message": "User registered successfully.", "user": user_data}
        )
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@app.post("/auth/login", summary="Authenticate and obtain a JWT")
def log_in(payload: dict):
    """Authenticates a user and issues a JSON Web Token (JWT)."""
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password or not str(email).strip() or not str(password).strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required and cannot be empty."}
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": str(email).strip(),
            "password": str(password).strip()
        })
        
        if not response.session:
            return JSONResponse(status_code=401, content={"error": "Invalid login credentials"})

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer",
            "expires_in": response.session.expires_in
        }
    except Exception:
        return JSONResponse(status_code=401, content={"error": "Invalid login credentials"})

# --- STAGE 2: PUBLIC & PROTECTED GATES ---

@app.get("/public/info", summary="Read public, open data")
def public_info():
    """
    A completely open endpoint. No authentication required.
    """
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile", summary="Read private profile data (Unverified Gate)")
def protected_profile(request: Request):
    """
    A protected gate that checks for the presence of a Bearer token.
    - Returns 401 if the Authorization header is missing or malformed.
    - Returns a placeholder success message if a token string is present.
    """
    auth_header = request.headers.get("Authorization")

    # Business Rule: Header must exist, must start with 'Bearer ', and must have a token after the space
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"}
        )

    # Extract the token string (everything after 'Bearer ')
    token = auth_header.split(" ")[1].strip()

    if not token:
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"}
        )

    # Stage 2 Placeholder: We confirm a token was presented. 
    # (In Stage 3, we will pass this token to Supabase for cryptographic verification!)
    return {
        "message": "Token presented successfully.",
        "token_preview": f"{token[:10]}... (Unverified in Stage 2)"
    }