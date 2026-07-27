# 🛡️ Supabase JWT Authentication Guard API

A secure REST API built with **Python**, **FastAPI**, and **Supabase Authentication**. This project demonstrates enterprise-grade user authentication using **Supabase Auth**, **JWT (JSON Web Tokens)**, and reusable **FastAPI dependency guards** to secure protected API endpoints.

---

## 🚀 Features

- 🔐 User Registration (Sign Up)
- 🔑 User Login (JWT Authentication)
- 🚪 User Logout
- 🛡️ Protected Routes using FastAPI Dependencies
- ✅ JWT Bearer Token Validation
- 📄 Interactive Swagger UI Documentation
- ⚡ Environment Variable Configuration
- 🔒 Secure Secret Management with `.env`
- 🏗️ Clean and Scalable Project Structure

---

# 💡 The Big Idea in 60 Seconds: The Trust Triangle

Traditional applications store user passwords themselves.

Modern applications don't.

Instead, authentication responsibility is delegated to an **Identity Provider (Supabase)** while your FastAPI application only verifies signed access tokens.

That creates a trust triangle:

- **Client** → sends credentials
- **Supabase** → authenticates the user and issues a signed JWT
- **FastAPI Server** → verifies the JWT before allowing access

```text
                +--------------------+
                |     Supabase       |
                | Identity Provider  |
                +--------------------+
                    ▲            │
     Email/Password │            │ Signed JWT
                    │            ▼
+-----------+ ----------------> +----------------+
|  Client   |                   | FastAPI Server |
+-----------+ <---------------- +----------------+
       ▲          Protected APIs        │
       └──────── Authorization: Bearer JWT
```

---

## 🔄 Authentication Flow

| Step | Actor | Description |
|------|-------|-------------|
| 1 | Client | Sends email & password to Supabase |
| 2 | Supabase | Validates credentials |
| 3 | Supabase | Returns signed JWT Access Token |
| 4 | Client | Sends JWT in Authorization Header |
| 5 | FastAPI | Validates JWT |
| 6 | FastAPI | Grants or denies access |

---

# 📁 Project Structure

```text
.
├── app/
│   ├── main.py
│   └── __init__.py
│
├── images/
│   ├── swagger-padlocks.png
│   ├── profile-200.png
│   ├── login-success.png
│   ├── signup-success.png
│   └── swagger-authorize.png
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| FastAPI | REST API Framework |
| Supabase | Authentication Provider |
| JWT | Authentication Tokens |
| Uvicorn | ASGI Server |
| python-dotenv | Environment Variables |
| HTTPBearer | Authentication Middleware |

---

# ⚙️ Getting Started

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git

cd YOUR_REPOSITORY_NAME
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Copy the template

```bash
cp .env.example .env
```

or on Windows

```cmd
copy .env.example .env
```

Then edit your `.env`

```env
SUPABASE_URL=https://your-project-id.supabase.co

SUPABASE_KEY=your-anon-public-key

PORT=8000
```

> **⚠️ Security Warning**
>
> Never upload your `.env` file to GitHub.
>
> Never expose your `service_role` key.
>
> Only use the **anon public key**.

---

## 5️⃣ Run the Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

ReDoc Documentation

```
http://localhost:8000/redoc
```

---

# 🌐 API Endpoints

| Method | Endpoint | Description | Authentication |
|---------|----------|-------------|----------------|
| GET | / | API Root | ❌ Public |
| GET | /health | Health Check | ❌ Public |
| POST | /auth/signup | Register User | ❌ Public |
| POST | /auth/login | Login User | ❌ Public |
| POST | /auth/logout | Logout User | ✅ Bearer Token |
| GET | /public/info | Public Endpoint | ❌ Public |
| GET | /protected/profile | Protected Profile | ✅ Bearer Token |
| GET | /protected/dashboard | Protected Dashboard | ✅ Bearer Token |

---

# 🔑 Authentication

Protected endpoints require the following HTTP header

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Example

```http
GET /protected/profile HTTP/1.1

Host: localhost:8000

Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

# 📸 Screenshot Gallery

Follow the complete authentication workflow below, from creating a new account to logging out of the application.

---

## 👤 1. User Registration (Sign Up)

Create a new user account using a valid email address and password.

![User Registration](images/signup.png)

---

## 🔓 2. User Login

Authenticate using your registered credentials. A successful login returns a JWT access token and refresh token.

![User Login](images/login.png)

---

## 🔑 3. Authorize with JWT Bearer Token

Click the **Authorize** button in the Swagger UI and paste your JWT access token in the format:

```text
Bearer YOUR_ACCESS_TOKEN
```

Once authorized, Swagger automatically includes the token in all protected requests.

![JWT Bearer Authorization](images/authbearer.png)

---

## 👤 4. View Authenticated Profile Information

Access the authenticated user's profile information after successful JWT verification.

![Profile Information](images/profileinfo.png)

---

## ✅ 5. Protected Profile Endpoint

Successfully access the protected profile endpoint, demonstrating that the JWT has been verified and the request is authorized.

![Protected Profile](images/protectprofile.png)

---

## 📊 6. Protected Dashboard

Access the protected dashboard endpoint. This endpoint is accessible only after successful authentication using a valid JWT Bearer token.

![Protected Dashboard](images/dashboard.png)

---

## 🚪 7. User Logout

Terminate the authenticated session by calling the logout endpoint with a valid Bearer token.

![User Logout](images/logout.png)

---
# 🔐 JWT Authentication Flow

```text
            User
              │
              │ Email + Password
              ▼
       +----------------+
       |   Supabase     |
       +----------------+
              │
              │ Verify Credentials
              ▼
      Generate JWT Token
              │
              ▼
         Client Stores JWT
              │
              │
Authorization: Bearer JWT
              │
              ▼
      +----------------+
      |   FastAPI API  |
      +----------------+
              │
     Verify JWT Signature
              │
      ┌───────┴────────┐
      │                │
   Valid JWT      Invalid JWT
      │                │
      ▼                ▼
200 OK          401 Unauthorized
```

---

# 📦 Dependencies

```text
fastapi
uvicorn
supabase
python-dotenv
```

Install everything with

```bash
pip install -r requirements.txt
```

---

# 🔒 Security Best Practices

- Never commit `.env`
- Never expose the `service_role` key
- Always validate JWTs before granting access
- Use HTTPS in production
- Store secrets using environment variables
- Keep dependencies updated

---

# 🧪 Testing the API

### Create User

```
POST /auth/signup
```

↓

### Login

```
POST /auth/login
```

↓

### Copy Access Token

↓

### Click **Authorize** in Swagger

↓

### Paste

```
Bearer YOUR_ACCESS_TOKEN
```

↓

### Access

```
GET /protected/profile
```

↓

```
200 OK
```

---

# 📚 Learning Objectives

This project demonstrates how to:

- Build authentication APIs with FastAPI
- Integrate Supabase Authentication
- Validate JWT access tokens
- Protect endpoints using dependency injection
- Configure environment variables securely
- Build reusable authentication middleware
- Generate interactive API documentation

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push the branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is released under the **MIT License**.

Feel free to use, modify, and distribute it for learning and development purposes.

---

# 👨‍💻 Author

**Rohan Das P**

Computer Science Engineer

Python • FastAPI • Supabase • REST APIs • Backend Development


---

⭐ If you found this project useful, consider giving it a **Star** on GitHub!