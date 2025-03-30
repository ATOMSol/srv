from .settings import *  # Import production settings and override for development

DEBUG = True
# ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ✅ Fix CSRF & CORS
# CSRF_TRUSTED_ORIGINS = [
#     "http://127.0.0.1:4003",
#     "http://localhost:4003",
# ]

# CORS_ALLOWED_ORIGINS = [
#     "http://127.0.0.1:4003",
#     "http://localhost:4003",
# ]

# CORS_ALLOW_CREDENTIALS = True  # Required for authentication


# Use local Redis if in debug mode
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0") if DEBUG else os.getenv("REDIS_URL")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}