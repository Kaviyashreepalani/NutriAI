import os
import base64
import json
from typing import Any, Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.core.config import settings


class ColumnEncryptor:
    """Provides AES-256-GCM authenticated encryption for sensitive health fields."""

    def __init__(self, key_b64: Optional[str] = None):
        raw_key = key_b64 or settings.ENCRYPTION_KEY
        try:
            self._key = base64.b64decode(raw_key)
            if len(self._key) != 32:
                # Pad or hash to 32 bytes if necessary for dev environments
                import hashlib
                self._key = hashlib.sha256(raw_key.encode()).digest()
            self._aesgcm = AESGCM(self._key)
        except Exception as e:
            import hashlib
            self._key = hashlib.sha256(str(raw_key).encode()).digest()
            self._aesgcm = AESGCM(self._key)

    def encrypt(self, plaintext: str) -> str:
        """Encrypts a string and returns a base64-encoded payload (nonce + ciphertext + tag)."""
        if not plaintext:
            return ""
        nonce = os.urandom(12)  # 96-bit nonce standard for GCM
        ciphertext = self._aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
        # Store as base64: nonce + ciphertext
        return base64.b64encode(nonce + ciphertext).decode("utf-8")

    def decrypt(self, encoded_payload: str) -> str:
        """Decrypts a base64-encoded payload."""
        if not encoded_payload:
            return ""
        try:
            raw_payload = base64.b64decode(encoded_payload.encode("utf-8"))
            if len(raw_payload) < 28:  # 12-byte nonce + 16-byte tag minimum
                return ""
            nonce = raw_payload[:12]
            ciphertext = raw_payload[12:]
            decrypted_bytes = self._aesgcm.decrypt(nonce, ciphertext, None)
            return decrypted_bytes.decode("utf-8")
        except Exception:
            return ""

    def encrypt_json(self, data: Any) -> str:
        if data is None:
            return ""
        return self.encrypt(json.dumps(data))

    def decrypt_json(self, encoded_payload: str) -> Any:
        raw = self.decrypt(encoded_payload)
        if not raw:
            return None
        try:
            return json.loads(raw)
        except Exception:
            return None


encryptor = ColumnEncryptor()

