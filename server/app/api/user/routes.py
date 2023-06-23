from typing import List, Optional

from beanie import init_beanie
from fastapi import APIRouter, Depends, FastAPI, HTTPException

from api.consumable.models import Consumable
from config.fief_client import FiefAccessTokenInfo, FiefUserInfo, auth

router = APIRouter()


@router.get("/info")
async def get_user(user: FiefUserInfo = Depends(auth.current_user())):
    return user


@router.get("/token")
async def get_user(
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
):
    return access_token_info
