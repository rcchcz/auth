from argon2 import PasswordHasher
import random
from database import first_insert, insert_new_records

# this identifies the client using the api (rabbit, database, etc)
first_insert_id_hash = ['dashboards', 'cache_manager', 'rabbitmq',
                       'data_and_schedule', 'data_access', 'ckan',
                       'dkan', 'socrata', 'authentication']

id_hash = ['test']
data = []
ph = PasswordHasher()

# this is the second part of the auth token
# random.getrandbits(128) generates a pseudo-random integer with 128 bits
for id in id_hash:
    hash = random.getrandbits(128)
    raw_token = f'{id}:{hash}'
    hash = ph.hash(raw_token)
    data.append({'microservice': id, 'token': hash})
    print(f'{id:<20} | {raw_token}')

insert_new_records(data)

# this is the second part of the auth token
# random.getrandbits(128) generates a pseudo-random integer with 128 bits
# hash = random.getrandbits(128)

# raw_token = f'{id_hash}:{hash}'
# print(f'raw_token: {raw_token}')

# ph = PasswordHasher()
# hash = ph.hash(raw_token) # this would be stored in database as pass for rabbit microservice
# print(f'hash: {hash}')
# print(ph.verify(hash, raw_token)) # verify password, raises exception if wrong
