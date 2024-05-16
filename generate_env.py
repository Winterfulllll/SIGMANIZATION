from cryptography.fernet import Fernet
import secrets

secret_key = secrets.token_urlsafe(32)
fernet_key = Fernet.generate_key().decode()
kinopoisk_api_key = ""  # Insert the key to access the Kinopoisk API here
gigachat_api_key = ""  # Insert the key to access the GigaChat API here

with open('.env', 'w') as env_file:
    env_file.write(f'SECRET_KEY="{secret_key}"\n')
    env_file.write(f'FERNET_KEY="{fernet_key}"\n')
    env_file.write('MOVIES_API=""\n')
    env_file.write('GIGACHAT_AUTH=""\n')

print('File ".env" is created with the following variables:\n')
print(f'SECRET_KEY: "{secret_key}"')
print(f'FERNET_KEY: "{fernet_key}"')
print(f'MOVIES_API: "{kinopoisk_api_key}"')
print(f'GIGACHAT_AUTH: "{gigachat_api_key}"')
