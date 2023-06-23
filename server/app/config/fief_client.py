from fastapi.security import OAuth2AuthorizationCodeBearer
from fief_client import FiefAccessTokenInfo, FiefAsync, FiefUserInfo
from fief_client.integrations.fastapi import FiefAuth

from config.settings import app_configs, settings

# Fief settings
# https://docs.fief.dev/integrate/python/fastapi/
fief = FiefAsync(settings.FIEF_URL, settings.CLIENT_ID, settings.CLIENT_SECRET)

scheme = OAuth2AuthorizationCodeBearer(
    settings.AUTHORIZE_URL,
    settings.TOKEN_URL,
    scopes={"openid": "openid", "offline_access": "offline_access"},
    auto_error=False,
)

auth = FiefAuth(fief, scheme)
