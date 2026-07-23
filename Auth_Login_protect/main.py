import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
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
    """
    Registers a new user with Supabase Auth.
    - Validates that email and password are provided.
    - Returns 201 Created with user metadata on success.
    """
    email = payload.get("email")
    password = payload.get("password")

    # Business Rule #1: Server never trusts the client. Validate input immediately.
    if not email or not password or not str(email).strip() or not str(password).strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required and cannot be empty."}
        )

    try:
        # Pass credentials to Supabase Identity Provider
        response = supabase.auth.sign_up({
            "email": str(email).strip(),
            "password": str(password).strip()
        })
        
        # Format the user receipt
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
        # Catch Supabase rejections (e.g., weak password, invalid email format)
        return JSONResponse(status_code=400, content={"error": str(e)})


@app.post("/auth/login", summary="Authenticate and obtain a JWT")
def log_in(payload: dict):
    """
    Authenticates a user and issues a JSON Web Token (JWT).
    - Returns 400 if fields are empty.
    - Returns 401 if Supabase rejects the login credentials.
    - Returns 200 with access_token (JWT) on success.
    """
    email = payload.get("email")
    password = payload.get("password")

    # Validate empty inputs
    if not email or not password or not str(email).strip() or not str(password).strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required and cannot be empty."}
        )

    try:
        # Request Supabase to verify credentials and issue a session token
        response = supabase.auth.sign_in_with_password({
            "email": str(email).strip(),
            "password": str(password).strip()
        })
        
        if not response.session:
            return JSONResponse(status_code=401, content={"error": "Invalid login credentials"})

        # Return the JWT access token and refresh token
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer",
            "expires_in": response.session.expires_in
        }
    except Exception:
        # If Supabase throws an AuthApiError (wrong password/user not found), return 401
        return JSONResponse(status_code=401, content={"error": "Invalid login credentials"})