# Tugas 4 Pemrograman Web Lanjutan: Automated Testing dengan Pytest

Proyek ini adalah implementasi pengujian otomatis pada layanan Microservice FastAPI. 

## Fitur yang Diuji:
1. **Autentikasi**: Register dan Login untuk mendapatkan JWT Token.
2. **CRUD Operasional**: Menambah dan membaca data Item.
3. **RBAC (Role-Based Access Control)**: Memastikan User biasa tidak bisa menambah data (Access Denied) dan hanya Admin yang bisa.

## Cara Menjalankan Tes:
1. Install dependencies: `pip install -r requirements.txt`
2. Jalankan pytest: `pytest test_main.py -v`
