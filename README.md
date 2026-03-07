# Tugas 3 Web Lanjutan: CRUD Dasar FastAPI

Repositori ini berisi implementasi endpoint `GET /items/` dan `GET /items/{id}` menggunakan FastAPI dan SQLAlchemy, dengan database SQLite dan validasi Pydantic. Tugas ini disusun untuk memenuhi tugas mata kuliah Pemrograman Web Lanjutan.

## 📁 Struktur File
* **`database.py`**: Konfigurasi koneksi ke database SQLite (`tugas.db`).
* **`models.py`**: Definisi struktur tabel `items` (kolom id, name, description) menggunakan SQLAlchemy.
* **`schemas.py`**: Validasi skema data input dan output menggunakan Pydantic.
* **`main.py`**: File utama berisi rute endpoint API.

## 🛠️ Teknologi yang Digunakan
* FastAPI
* SQLAlchemy (ORM)
* Pydantic
* SQLite
* Uvicorn (Server)

## 🚀 Cara Menjalankan Project

Buka terminal, pastikan berada di direktori project, lalu jalankan perintah berikut secara berurutan untuk menginstal *library* dan menyalakan server lokal:

```bash
    1. pip install fastapi uvicorn sqlalchemy pydantic
Setelah itu jalankan di terminal menggunakan periintah ini :  
    2. uvicorn main:app --reload
