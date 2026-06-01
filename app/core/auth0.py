from jose import jwt


def verify_auth0_token(token: str):
    return jwt.get_unverified_claims(token)


def decode_auth0_token(token: str):
    return jwt.get_unverified_claims(token)
