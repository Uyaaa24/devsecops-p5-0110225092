# Task Manager API

## 1. Nama Aplikasi & Fungsi
**Task Manager API** adalah REST API sederhana untuk mengelola daftar tugas
(membuat, melihat, mengubah, menghapus, dan memfilter task berdasarkan status).
Data disimpan in-memory.

## 2. Bahasa & Framework
- Bahasa: Python 3.12
- Framework: Flask
- Testing: `unittest` (bawaan Python)
- SAST: Bandit

## 3. Cara Menjalankan
```bash
git clone https://github.com/<username>/devsecops-task-api.git
cd devsecops-task-api
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m unittest discover -s tests -v   # jalankan unit test
python run.py                              # http://localhost:5000
```

| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /health | Cek status aplikasi |
| GET | /api/tasks?status=todo | Daftar task (filter opsional) |
| GET | /api/tasks/<id> | Detail task |
| POST | /api/tasks | Buat task `{"title":"Belajar"}` |
| PUT | /api/tasks/<id> | Ubah task |
| DELETE | /api/tasks/<id> | Hapus task |

## 4. Overview Pipeline CI/CD
Pipeline ada di `.github/workflows/devsecops.yml`, berjalan otomatis pada
**push** dan **pull_request** ke branch `main`, memakai runner `ubuntu-latest`.

| Job | Fungsi |
|-----|--------|
| `build` | Checkout, setup Python 3.12, install dependency dari `requirements.txt`, jalankan unit test |
| `sast-scan` | Berjalan setelah `build` sukses (`needs: build`). Menjalankan **Bandit** untuk memindai kerentanan pada kode Python, lalu mengunggah laporan JSON sebagai artifact |

Alur: `Push/PR → build → sast-scan`