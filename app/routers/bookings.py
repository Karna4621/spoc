from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import BookingCreate, BookingRead
from ..models import Booking, AvailabilitySlot
from ..dependencies import get_db

router = APIRouter()

@router.post('/bookings', response_model=BookingRead)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    # Check if slot available
    slot = db.query(AvailabilitySlot).filter(
        AvailabilitySlot.slot_id == booking.slot_id,
        AvailabilitySlot.is_booked == False
    ).first()
    if not slot:
        raise HTTPException(status_code=400, detail="Selected slot is not available")
    # Mark slot as booked
    slot.is_booked = True
    # Generate meeting link (placeholder)
    meeting_link = f"https://meet.example.com/{booking.spoc_id}-{booking.slot_id}"
    # Create booking record
    new_booking = Booking(
        spoc_id=booking.spoc_id,
        slot_id=booking.slot_id,
        client_name=booking.client_name,
        meeting_link=meeting_link
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking