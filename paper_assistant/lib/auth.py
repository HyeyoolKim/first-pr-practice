import bcrypt

from lib import db


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def sign_up(username: str, password: str) -> int:
    username = username.strip()
    if not username or not password:
        raise ValueError("아이디와 비밀번호를 모두 입력해주세요.")
    if len(username) < 2:
        raise ValueError("아이디는 2자 이상이어야 해요.")
    if len(password) < 4:
        raise ValueError("비밀번호는 4자 이상이어야 해요.")
    if db.get_user_by_username(username):
        raise ValueError("이미 사용 중인 아이디입니다.")
    return db.create_user(username, hash_password(password))


def login(username: str, password: str):
    user = db.get_user_by_username(username.strip())
    if not user or not verify_password(password, user["password_hash"]):
        return None
    return user
