import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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
    description="A secure API protected by Supabase JWT Authentication with Swagger UI support.",
    version="1.0.0"
)

# Global Exception Handler to ensure standard {"error": "..."} JSON formatting
@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


# --- STAGE 5: SWAGGER UI SECURITY SCHEME ---
# Setting auto_error=False lets us keep our custom 401 JSON error messages
security = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Stage 5 Upgraded Dependency:
    - Uses HTTPBearer so FastAPI generates the Authorize padlock icon in Swagger UI.
    - Verifies the extracted token cryptographically with Supabase.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Access token required")
    
    token = credentials.credentials
        
    try:
        # Cryptographically verify the token with Supabase
        response = supabase.auth.get_user(token)
        if not response.user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return response.user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# --- STAGE 0: HEALTH CHECKS ---

@app.get("/", summary="API Root")
def read_root():
    return {"name": "Auth Guard API", "version": "1.0.0", "status": "active"}

@app.get("/health", summary="Health Check")
def health_check():
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client is not connected.")
    return {"server": "ok", "supabase": "connected"}


# --- STAGE 1: OPEN AUTH ENDPOINTS ---

@app.post("/auth/signup", status_code=201, summary="Create a new user account")
def sign_up(payload: dict):
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password or not str(email).strip() or not str(password).strip():
        raise HTTPException(status_code=400, detail="Email and password are required and cannot be empty.")

    try:
        response = supabase.auth.sign_up({"email": str(email).strip(), "password": str(password).strip()})
        user_data = {
            "id": response.user.id if response.user else None,
            "email": response.user.email if response.user else email,
            "created_at": str(response.user.created_at) if response.user else None
        }
        return JSONResponse(status_code=201, content={"message": "User registered successfully.", "user": user_data})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/login", summary="Authenticate and obtain a JWT")
def log_in(payload: dict):
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password or not str(email).strip() or not str(password).strip():
        raise HTTPException(status_code=400, detail="Email and password are required and cannot be empty.")

    try:
        response = supabase.auth.sign_in_with_password({"email": str(email).strip(), "password": str(password).strip()})
        if not response.session:
            raise HTTPException(status_code=401, detail="Invalid login credentials")

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer",
            "expires_in": response.session.expires_in
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid login credentials")


# --- STAGE 4 & 5: PROTECTED ROUTES & LOGOUT ---

@app.post("/auth/logout", status_code=204, summary="End the user's session")
def log_out(user = Depends(get_current_user)):
    """
    Protected endpoint: Verifies the token via middleware, signs out, and returns 204 No Content.
    """
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    return Response(status_code=204)


@app.get("/public/info", summary="Read public, open data")
def public_info():
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile", summary="Read private profile data")
def protected_profile(user = Depends(get_current_user)):
    """
    Protected route: Now features the Swagger UI padlock icon!
    """
    return {
        "message": "Access granted. Welcome to the VIP room!",
        "user": {
            "id": user.id,
            "email": user.email,
            "created_at": str(user.created_at)
        }
    }


@app.get("/protected/dashboard", summary="User dashboard")
def protected_dashboard(user = Depends(get_current_user)):
    """
    Second protected route sharing the exact same HTTPBearer security scheme.
    """
    return {
        "message": f"Welcome to your dashboard, {user.email}!",
        "status": "active_session",
        "user_id": user.id
    }