import requests
import jwt
from jwt import PyJWKClient
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError


class Auth0Authenticator:
    def __init__(self, auth0_domain, auth0_audience):
        """
        Initialize the Auth0 Authenticator.

        Args:
            auth0_domain (str): Auth0 domain (e.g., 'your-tenant.auth0.com').
            auth0_audience (str): Auth0 API audience identifier.
        """
        self.auth0_domain = auth0_domain
        self.auth0_audience = auth0_audience
        self.jwk_client = PyJWKClient(
            f"https://{auth0_domain}/.well-known/jwks.json")

    def verify_api_key(self, token):
        """
        Verify the provided API key (JWT) by querying Auth0's JWKS.

        Args:
            token (str): The JWT token to verify.

        Returns:
            dict: Decoded payload if verification is successful.

        Raises:
            ValueError: If the token is invalid or expired.
        """
        try:
            signing_key = self.jwk_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.auth0_audience,
                issuer=f"https://{self.auth0_domain}/"
            )
            return payload
        except (InvalidTokenError, ExpiredSignatureError, DecodeError) as e:
            raise ValueError("Invalid or expired token") from e
