from typing import Optional

import firebase_admin
from firebase_admin import auth, credentials

from .config import settings

# Initialize Firebase app if credentials are provided
if settings.FIREBASE_CREDENTIALS:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)
else:
    cred = None

def verify_firebase_token(id_token: str) -> Optional[dict]:
    """Verify a Firebase ID token and return the decoded claims."""
    if not cred:
        return None
    try:
        return auth.verify_id_token(id_token)
    except Exception:
        return None
