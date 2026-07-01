from jose import jwt
from jose.exceptions import JWTError
import requests
from app.core.config import settings

JWKS_URL = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"

def verify_auth0_token(token: str):
    header = jwt.get_unverified_header(token)

    jwks = requests.get(JWKS_URL).json()

    rsa_key = None
    for key in jwks["keys"]:
        if key["kid"] == header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
            break

    if rsa_key is None:
        raise JWTError("Unable to find appropriate key")

    payload = jwt.decode(
        token,
        rsa_key,
        algorithms=["RSA256"],
        audience=settings.AUTH0_AUDIENCE,
        issuer=f"https://{settings.AUTH0_DOMAIN}/"
    )

    return payload


def decode_auth0_token(token: str):
    return verify_auth0_token(token)
