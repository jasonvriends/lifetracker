from datetime import date, datetime, time
from typing import List, Optional
from zoneinfo import ZoneInfo

from beanie import PydanticObjectId, init_beanie
from fastapi import APIRouter, Depends, FastAPI, HTTPException

from api.consumable.models import Consumable
from config.fief_client import FiefAccessTokenInfo, FiefUserInfo, auth

router = APIRouter()


@router.get("/", response_model=List[Consumable])
async def get_consumables(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
    user: FiefUserInfo = Depends(auth.current_user()),
):
    """
    Retrieves a list of the user's consumables.

    **Args**:
    - **start_date** `Optional[datetime]` \n
      - Defaults to the current date in the user's timezone or UTC if none is provided.
    - **end_date** `Optional[datetime]` \n
      - Defaults to the current date in the user's timezone or UTC if none is provided.

    **Returns**:
    - `List[Consumable]` \n
      - A list of consumables consumed within the start_date and end_date.
    """

    # Set the start_date if it's None
    if start_date is None:
        start_date = datetime.combine(date.today(), time.min)

    # Set the end_date if it's None
    if end_date is None:
        end_date = datetime.combine(date.today(), time.max)

    # Retrieve consumables from the database
    result = await Consumable.find(
        Consumable.user_id == user["sub"],
        Consumable.consumed_at >= start_date,
        Consumable.consumed_at <= end_date,
    ).to_list()

    return result


@router.post("/", response_model=Consumable)
async def create_consumable(
    consumable: Consumable,
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
    user: FiefUserInfo = Depends(auth.current_user()),
):
    """
    Create a new consumable associated to the user.

    **Args**:
    - **consumable** `Consumable` \n

    **Returns**:
    - `Consumable` \n
    """

    # Set user_id to user
    consumable.user_id = user["sub"]

    # Insert consumable into the database
    await consumable.insert()

    # Return the consumable
    return consumable


@router.get("/{consumable_id}", response_model=Consumable)
async def get_consumable(
    consumable_id: PydanticObjectId,
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
    user: FiefUserInfo = Depends(auth.current_user()),
):
    """
    Retrieves a user's consumable by ID.

    **Args**:
    - **consumable_id** `PydanticObjectId` \n
      - The ID of the consumable item to retrieve.

    **Raises**:
    - `HTTPException` \n
      - 404: Consumable not found
      - 403: Unauthorized access

    **Returns**:
    - `Consumable` \n
    """

    # Retrive consumable from the database
    consumable = await Consumable.get(consumable_id)

    if not consumable:
        # Consumable not found
        raise HTTPException(status_code=404, detail="Consumable not found")

    # Verify consumable user_id and logged in user match
    if str(consumable.user_id) != str(user["sub"]):
        raise HTTPException(status_code=403, detail="Unauthorized access")

    # Return the consumable
    return consumable


@router.put("/{consumable_id}", response_model=Consumable)
async def update_consumable(
    consumable_id: PydanticObjectId,
    consumable: Consumable,
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
    user: FiefUserInfo = Depends(auth.current_user()),
):
    """
    Updates a user's consumable by ID.

    **Args**:
    - **consumable_id** `PydanticObjectId` \n
      - The ID of the consumable item to update.
    - **consumable** `Consumable` \n
      - The consumable to be updated.

    **Raises**:
    - `HTTPException` \n
      - 404: Consumable not found
      - 403: Unauthorized access

    **Returns**:
    - `Consumable` \n
    """

    # Retrive consumable from the database
    existing_consumable = await Consumable.get(consumable_id)

    if not existing_consumable:
        # Consumable not found
        raise HTTPException(status_code=404, detail="Consumable not found")

    # Verify consumable user_id and logged in user match
    if str(existing_consumable.user_id) != str(user["sub"]):
        raise HTTPException(status_code=403, detail="Unauthorized access")

    # Update only changed fields
    for field in consumable.__fields__:
        field_value = getattr(consumable, field)
        if field_value is not None:
            print({field: field_value})
            await existing_consumable.set({field: field_value})

    return existing_consumable


@router.delete("/{consumable_id}")
async def delete_consumable(
    consumable_id: PydanticObjectId,
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
    user: FiefUserInfo = Depends(auth.current_user()),
):
    """
    Deletes a user's consumable by ID.

    **Args**:
    - **consumable_id** `PydanticObjectId` \n
      - The ID of the consumable item to delete.

    **Raises**:
    - `HTTPException` \n
      - 404: Consumable not found
      - 403: Unauthorized access

    **Returns**:
    - `str` \n
    """

    # Retrive consumable from the database
    consumable = await Consumable.get(consumable_id)

    if not consumable:
        # Consumable not found
        raise HTTPException(status_code=404, detail="Consumable not found")

    # Verify consumable user_id and logged in user match
    if str(consumable.user_id) != str(user["sub"]):
        raise HTTPException(status_code=403, detail="Unauthorized access")

    await consumable.delete()

    return {"message": "Consumable deleted"}
