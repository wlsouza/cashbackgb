from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated_="auto")


def  get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def  verify_password(raw_password: str, hashed_password:str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)