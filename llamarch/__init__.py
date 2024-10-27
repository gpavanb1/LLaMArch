import os
from .auth.authenticator import Auth0Authenticator

# Fetch the API key from environment variables or any secure source
API_KEY = os.getenv("LLAMARCH_API_KEY")

# Initialize Auth0 details
AUTH0_DOMAIN = "your-tenant.auth0.com"  # Replace with your Auth0 domain
AUTH0_AUDIENCE = "your-api-audience"  # Replace with your API audience

# Initialize the Auth0Authenticator
authenticator = Auth0Authenticator(
    auth0_domain=AUTH0_DOMAIN, auth0_audience=AUTH0_AUDIENCE)

# Check API key validity on package import
if API_KEY is None:
    raise ValueError(
        "API key not found. Please set the LLAMARCH_API_KEY environment variable.")

try:
    payload = authenticator.verify_api_key(API_KEY)
    print("API key is valid.")
except ValueError as e:
    raise ImportError(f"Invalid API key: {e}")
