from argon2 import PasswordHasher
import random

# this identifies the client using the api (rabbit, database, dns etc)
id_hash = 'dns'

# this is the second part of the auth token
# random.getrandbits(128) generates a pseudo-random integer with 128 bits
hash = random.getrandbits(128)

raw_token = f'{id_hash}:{hash}'
print(f'raw_token: {raw_token}')

ph = PasswordHasher()
hash = ph.hash(raw_token) # this would be stored in database as pass for rabbit microservice
print(f'hash: {hash}')
print(ph.verify(hash, raw_token)) # verify password, raises exception if wrong
