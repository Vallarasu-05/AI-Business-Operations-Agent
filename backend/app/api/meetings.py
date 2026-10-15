from fastapi import APIRouter, Depends, HTTPException
from app.security.auth import require_api_key
from app.services import meeting_service

router = APIRouter(dependencies=[Depends(require_api_key)])


@router.get("/tomorrow")
def tomorrow():
    d = meeting_service.tomorrow()
    return {"date": d, "meetings": meeting_service.meetings_for(d)}


@router.get("/{meeting_id}")
def one(meeting_id: str):
    m = meeting_service.find_meeting(meeting_id)
    if not m:
        raise HTTPException(404, "Meeting not found")
    return m
