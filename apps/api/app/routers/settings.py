from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import get_session
from ..deps import get_current_user
from ..models import User
from ..schemas import SettingsResponse, UpdateSettingsRequest

router = APIRouter(prefix="/api", tags=["settings"])


@router.get("/settings", response_model=SettingsResponse)
def get_settings(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return user


@router.patch("/settings", response_model=SettingsResponse)
def update_settings(
    payload: UpdateSettingsRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    user.gatekeeper_enabled = payload.gatekeeper_enabled
    user.gatekeeper_threshold = payload.gatekeeper_threshold
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
