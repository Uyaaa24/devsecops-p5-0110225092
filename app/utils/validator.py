VALID_STATUS = ["todo", "in_progress", "done"]


def validate_task(data):
    """Validasi payload task. Mengembalikan (valid, daftar_error)."""
    errors = []

    if not isinstance(data, dict):
        return False, ["body harus berupa JSON object"]

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append("title wajib diisi")
    elif len(title) > 100:
        errors.append("title maksimal 100 karakter")

    if "status" in data and data["status"] not in VALID_STATUS:
        errors.append("status harus salah satu dari: " + ", ".join(VALID_STATUS))

    return len(errors) == 0, errors
