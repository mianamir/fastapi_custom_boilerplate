from passlib.context import CryptContext

# hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:

    def get_pass_bcrypt(password: str):
        hashed_password = pwd_context.hash(password)

        return hashed_password

    def verify(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

