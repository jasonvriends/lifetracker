from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, FastAPI, HTTPException

from config.fief_client import FiefAccessTokenInfo, FiefUserInfo, auth


def user_timezone(
    user: FiefUserInfo = Depends(auth.current_user()),
) -> str:
    """
    Returns the user timezone or UTC if one is not set.
    """

    if "fields" in user and "timezone" in user["fields"]:
        user_timezone = user["fields"]["timezone"]
    else:
        user_timezone = "UTC"

    return user_timezone
