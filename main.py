from argon2.exceptions import VerifyMismatchError
from fastapi import FastAPI, status
import argon2

mock_db = {
    'rabbitmq': '$argon2id$v=19$m=65536,t=3,p=4$gmTWdyaVioaDzoXi+Zi7CA$CqPj7mGICVcM4uCcExDH1zacKUMF6ShrirBrt99DH2U',
    'database': '$argon2id$v=19$m=65536,t=3,p=4$13a6vnlRHiR2jjC6u/Rc6w$LJuTeTRFhplfm87cs8t8k3dt7fRMJpaNllsvFKxNPnE',
    'dns': '$argon2id$v=19$m=65536,t=3,p=4$EgOOQAdv7q8Rok6muE0Jrw$1P92xuM/XYjdlbN58Fv1lQLLa8FTsvJboMnuitWZHX8'
}

def get_password_hash_for_user(user_token: str):
    colon_index = user_token.find(':')
    return user_token[:colon_index]

app = FastAPI()
ph = argon2.PasswordHasher()

@app.post('/token/{token}', status_code=204)
async def login(token: str):
    user = get_password_hash_for_user(token)
    hash = mock_db.get(user)
    print(user)

    if hash:
        try:
            ph.verify(hash, token)
            return status.HTTP_204_NO_CONTENT
        except(VerifyMismatchError):
            return status.HTTP_403_FORBIDDEN
    else:
        return status.HTTP_404_NOT_FOUND
