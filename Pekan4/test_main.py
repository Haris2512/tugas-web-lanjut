from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from database import Base

# 1. SETUP DATABASE TESTING (Biar tidak merusak data tugas.db aslimu)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tugas.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Variabel untuk menyimpan token
user_token = ""
admin_token = ""

# --- 1. PENGUJIAN ALUR AUTENTIKASI (REGISTER & LOGIN) ---
def test_register_user():
    response = client.post(
        "/register",
        json={"email": "user@example.com", "password": "password123", "role": "user"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"

def test_login_user():
    global user_token
    response = client.post(
        "/login",
        data={"username": "user@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    user_token = response.json()["access_token"]
    assert "access_token" in response.json()

def test_register_admin():
    response = client.post(
        "/register",
        json={"email": "admin@example.com", "password": "adminpass", "role": "admin"}
    )
    assert response.status_code == 200

def test_login_admin():
    global admin_token
    response = client.post(
        "/login",
        data={"username": "admin@example.com", "password": "adminpass"}
    )
    assert response.status_code == 200
    admin_token = response.json()["access_token"]


# --- 2. PENGUJIAN RBAC (ACCESS DENIED) ---
def test_user_cannot_create_item():
    # Akses ditolak karena yang login adalah User biasa, bukan Admin (Error 403)
    response = client.post(
        "/items/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"name": "Laptop", "description": "Laptop Gaming"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Akses ditolak: Hanya untuk Admin"


# --- 3. PENGUJIAN CRUD OPERASIONAL ---
def test_admin_can_create_item():
    # Create berhasil karena yang login adalah Admin (Status 200)
    response = client.post(
        "/items/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Mouse", "description": "Mouse Wireless"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Mouse"

def test_user_can_read_items():
    # Read (GET) berhasil karena User biasa diizinkan melihat data
    response = client.get(
        "/items/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0