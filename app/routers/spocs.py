from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import SpocBase, AvailabilitySlotBase
from ..models import Spoc, AvailabilitySlot
from ..dependencies import get_db

router = APIRouter()

@router.get('/spocs', response_model=List[SpocBase])
def get_spocs(db: Session = Depends(get_db)):
    return db.query(Spoc).all()

@router.get('/spocs/{spoc_id}/availability', response_model=List[AvailabilitySlotBase])
def get_spoc_availability(spoc_id: int, db: Session = Depends(get_db)):
    slots = db.query(AvailabilitySlot).filter(
        AvailabilitySlot.spoc_id == spoc_id,
        AvailabilitySlot.is_booked == False
    ).all()
    if not slots:
        raise HTTPException(status_code=404, detail="No available slots for this SPOC")
    return slots
