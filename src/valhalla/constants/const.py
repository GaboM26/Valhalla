DEFAULT= "DEFAULT"
DECRYPT = "dec"
ENCRYPT = "enc"
DEFAULT_SECRET_PATH = "src/valhalla/config/secrets.yaml"
MAX_RETRIES_ALLOWED = 3

# Master Fields
MASTER_TABLE_NAME = 'valhalla_warriors'
MASTER_FIELD_NAME = 'username'
HASHED_MASTER_PASSWORD_FIELD_NAME = 'password'

# Honir automatization
HONIR_REL_PATH = 'src/Honir'
CRYPTO_TOOLS_PATH = "bin/"
HASHER = 'hmac'
ENCRYPTOR = 'aes-encrypt'
DECRYPTOR = 'aes-decrypt'
AVAILABLE_CRYPTO_TOOLS = [
    HASHER,
    ENCRYPTOR,
    DECRYPTOR
]