"""
add_user.py — Script tiện ích để thêm/xóa/liệt kê user trong users.json

Dùng:
    python add_user.py list                          # Xem danh sách user
    python add_user.py add <email> <password> <name> # Thêm user mới
    python add_user.py remove <email>                # Xóa user
    python add_user.py passwd <email> <new_password> # Đổi mật khẩu
"""

import hashlib
import json
import sys
from pathlib import Path

USERS_FILE = Path(__file__).parent / "users.json"


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load() -> dict:
    try:
        return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"users": []}


def save(data: dict):
    USERS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_list():
    data = load()
    users = data.get("users", [])
    if not users:
        print("Chưa có user nào.")
        return
    print(f"{'Email':<35} {'Tên':<20} {'Role'}")
    print("-" * 65)
    for u in users:
        print(f"{u.get('email',''):<35} {u.get('name',''):<20} {u.get('role','user')}")


def cmd_add(email: str, password: str, name: str, role: str = "user"):
    data = load()
    email = email.strip().lower()
    if any(u["email"].lower() == email for u in data["users"]):
        print(f"❌ Email '{email}' đã tồn tại.")
        return
    data["users"].append({
        "email": email,
        "password_hash": _hash(password),
        "name": name,
        "role": role,
    })
    save(data)
    print(f"✅ Đã thêm user: {name} ({email})")


def cmd_remove(email: str):
    data = load()
    email = email.strip().lower()
    before = len(data["users"])
    data["users"] = [u for u in data["users"] if u.get("email","").lower() != email]
    if len(data["users"]) == before:
        print(f"❌ Không tìm thấy user '{email}'.")
    else:
        save(data)
        print(f"✅ Đã xóa user: {email}")


def cmd_passwd(email: str, new_password: str):
    data = load()
    email = email.strip().lower()
    for u in data["users"]:
        if u.get("email","").lower() == email:
            u["password_hash"] = _hash(new_password)
            save(data)
            print(f"✅ Đã đổi mật khẩu cho: {email}")
            return
    print(f"❌ Không tìm thấy user '{email}'.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "list":
        cmd_list()
    elif args[0] == "add" and len(args) >= 4:
        role = args[4] if len(args) > 4 else "user"
        cmd_add(args[1], args[2], args[3], role)
    elif args[0] == "remove" and len(args) >= 2:
        cmd_remove(args[1])
    elif args[0] == "passwd" and len(args) >= 3:
        cmd_passwd(args[1], args[2])
    else:
        print(__doc__)
