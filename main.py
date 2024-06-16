from argon2.exceptions import VerifyMismatchError
from fastapi import FastAPI, HTTPException
import argon2

from database import Auth, SessionLocal


# mock_db = {
#     'rabbitmq': '$argon2id$v=19$m=65536,t=3,p=4$gmTWdyaVioaDzoXi+Zi7CA$CqPj7mGICVcM4uCcExDH1zacKUMF6ShrirBrt99DH2U',
#     'database': '$argon2id$v=19$m=65536,t=3,p=4$13a6vnlRHiR2jjC6u/Rc6w$LJuTeTRFhplfm87cs8t8k3dt7fRMJpaNllsvFKxNPnE',
#     'dns': '$argon2id$v=19$m=65536,t=3,p=4$EgOOQAdv7q8Rok6muE0Jrw$1P92xuM/XYjdlbN58Fv1lQLLa8FTsvJboMnuitWZHX8'
# }

def get_microservice_id(user_token: str):
    colon_index = user_token.find(':')
    return user_token[:colon_index]


app = FastAPI()
ph = argon2.PasswordHasher()


@app.post('/token/{token}', status_code=200)
async def login(token: str):
    session = SessionLocal()
    ms = get_microservice_id(token)
    ms_db = session.query(Auth).filter_by(microservice=ms).one_or_none()
    session.close()

    if ms_db:
        try:
            print(f'{ms_db.microservice} | {ms}')
            print(f'{ms_db.token} | {token}')
            ph.verify(ms_db.token, token)
            return f"Authentiction succeed for {ms}"
        except VerifyMismatchError:
            raise HTTPException(status_code=403, detail=f"Incorrect token for user {ms}")
    else:
        raise HTTPException(status_code=404, detail="Unrecognized microservice")
