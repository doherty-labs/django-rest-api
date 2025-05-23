import json
from functools import wraps

import jwt
import requests
from django.contrib.auth import authenticate
from django.http import HttpRequest, JsonResponse
from jwt import algorithms
from rest_framework.exceptions import APIException, status

from django.conf import settings


def jwt_get_username_from_payload_handler(payload: dict) -> str:
    username = payload.get("sub").replace("|", ".")
    authenticate(remote_user=username)
    return username


NOT_FOUND = "Public key not found."


def jwt_decode_token(token: str) -> dict:
    header = jwt.get_unverified_header(token)
    jwks = requests.get(
        "https://" + settings.AUTH0_DOMAIN + "/.well-known/jwks.json", timeout=30
    ).json()
    public_key = None
    for jwk in jwks["keys"]:
        if jwk["kid"] == header["kid"]:
            public_key = algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise APIException(
            NOT_FOUND,
            code=status.HTTP_400_BAD_REQUEST,
        )

    return jwt.decode(
        token,
        public_key,
        audience=settings.AUTH0_IDENTIFIER,
        issuer="https://" + settings.AUTH0_DOMAIN + "/",
        algorithms=["RS256"],
    )


def get_token_auth_header(request: HttpRequest) -> str:
    """Obtains the Access Token from the Authorization Header"""
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    return parts[1]


def requires_scopes(required_scopes: list[str]):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """

    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[1])
            decoded = jwt_decode_token(token)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                scope_checks = [scope in token_scopes for scope in required_scopes]
                if all(scope_checks):
                    return f(*args, **kwargs)
            response = JsonResponse(
                {"message": "You don't have access to this resource"},
            )
            response.status_code = 403
            return response

        return decorated

    return require_scope
