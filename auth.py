"""
auth.py — Hệ thống xác thực email + mật khẩu
Mật khẩu được hash SHA-256, lưu trong users.json
"""

import hashlib
import json
from pathlib import Path

USERS_FILE = Path(__file__).parent / "users.json"


def _hash(password: str) -> str:
    """Hash mật khẩu bằng SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_users() -> list[dict]:
    """Đọc danh sách user từ users.json."""
    try:
        return json.loads(USERS_FILE.read_text(encoding="utf-8")).get("users", [])
    except Exception:
        return []


def verify_login(email: str, password: str) -> dict | None:
    """
    Kiểm tra email + mật khẩu.
    Trả về dict user nếu đúng, None nếu sai.
    """
    email = email.strip().lower()
    pw_hash = _hash(password)
    for user in load_users():
        if user.get("email", "").lower() == email and user.get("password_hash") == pw_hash:
            return user
    return None


def hash_password(password: str) -> str:
    """Tiện ích để tạo hash khi thêm user mới vào users.json."""
    return _hash(password)


# ── CLI helper: python auth.py <email> <password> ──────────────────────────
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        _, email, password = sys.argv
        result = verify_login(email, password)
        if result:
            print(f"✅ Đăng nhập thành công: {result['name']} ({result['role']})")
        else:
            print("❌ Email hoặc mật khẩu không đúng.")
    elif len(sys.argv) == 2 and sys.argv[1] == "--hash":
        pwd = input("Nhập mật khẩu cần hash: ")
        print(f"Hash: {hash_password(pwd)}")
    else:
        print("Dùng: python auth.py <email> <password>")
        print("      python auth.py --hash   (để tạo hash cho user mới)")
