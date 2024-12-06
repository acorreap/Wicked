import bcrypt

class EncryptionManager:

    def __init__(self, salt_rounds: int = 12):
        self.salt_rounds = salt_rounds

    def hash_data(self, data: str) -> str:
        data_bytes = data.encode('utf-8')

        salt = bcrypt.gensalt(rounds=self.salt_rounds)

        hashed = bcrypt.hashpw(data_bytes, salt)

        return hashed.decode('utf-8')

    def verify_data(self, data: str, hashed: str) -> bool:
        data_bytes = data.encode('utf-8')

        hashed_bytes = hashed.encode('utf-8')

        return bcrypt.checkpw(data_bytes, hashed_bytes)

    def is_hash_outdated(self, hashed: str) -> bool:
        hashed_bytes = hashed.encode('utf-8')

        return not bcrypt.hashpw(b'example', hashed_bytes).startswith(b"$2b$" + str(self.salt_rounds).encode('utf-8'))


manager = EncryptionManager(12)