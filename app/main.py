"""
SPOC Booking Platform - Complete Backend
All-in-one FastAPI application (no database, no separate files needed)
Perfect for quick demos and rapid prototyping
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
from uuid import uuid4

# =====================================================
# INITIALIZE FASTAPI APP
# =====================================================

app = FastAPI(
    title="SPOC Booking Platform API",
    description="Demo version - No database required",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# HARDCODED DATA - SPOCs
# =====================================================

SPOCS_DATA = [
    {
        "spoc_id": 1,
        "name": "Rajesh Sharma",
        "expertise": "Cloud Infrastructure",
        "specialization": "Enterprise Cloud Solutions & Migration",
        "email": "rajesh.sharma@company.com",
        "phone": "+91-9876543210"
    },
    {
        "spoc_id": 2,
        "name": "Priya Desai",
        "expertise": "Security Solutions",
        "specialization": "Regulatory & Data Protection",
        "email": "priya.desai@company.com",
        "phone": "+91-9876543211"
    },
    {
        "spoc_id": 3,
        "name": "Amit Patel",
        "expertise": "Data Analytics",
        "specialization": "Predictive Analytics & Business Intelligence",
        "email": "amit.patel@company.com",
        "phone": "+91-9876543212"
    }
]

# =====================================================
# HARDCODED DATA - SOLUTION TYPES
# =====================================================

SOLUTION_TYPES = [
    "Cloud Infrastructure",
    "Security Solutions",
    "Data Analytics",
    "Automation",
    "Custom Solutions"
]

# =====================================================
# GENERATE AVAILABILITY SLOTS (Auto-generated)
# =====================================================

def generate_availability_slots():
    """
    Auto-generate availability slots for next 14 days
    Each SPOC gets 3 time slots per day (10am, 2pm, 4pm)
    Total: 3 SPOCs × 14 days × 3 slots = 126 slots
    """
    slots = []
    slot_id = 1
    base_date = datetime.now() + timedelta(days=1)
    
    # For each SPOC
    for spoc_id in [1, 2, 3]:
        # For next 14 days
        for day_offset in range(14):
            current_date = base_date + timedelta(days=day_offset)
            
            # 3 time slots per day: 10am, 2pm, 4pm
            time_slots = [
                (10, 11),  # 10:00 AM - 11:00 AM
                (14, 15),  # 2:00 PM - 3:00 PM
                (16, 17)   # 4:00 PM - 5:00 PM
            ]
            
            for start_hour, end_hour in time_slots:
                start_time = current_date.replace(
                    hour=start_hour, minute=0, second=0, microsecond=0
                )
                end_time = current_date.replace(
                    hour=end_hour, minute=0, second=0, microsecond=0
                )
                
                slots.append({
                    "slot_id": slot_id,
                    "spoc_id": spoc_id,
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "is_booked": False
                })
                slot_id += 1
    
    return slots

# Initialize availability slots (126 total)
AVAILABILITY_SLOTS = generate_availability_slots()

# =====================================================
# RUNTIME DATA STORAGE (In-Memory)
# =====================================================

CLIENTS_DATA = []      # Clients created via API
BOOKINGS_DATA = []     # Bookings created via API

# =====================================================
# PYDANTIC SCHEMAS (Data Validation)
# =====================================================

class SPOCResponse(BaseModel):
    """Response schema for SPOC data"""
    spoc_id: int
    name: str
    expertise: str
    specialization: str
    email: str
    phone: str

class AvailabilitySlotResponse(BaseModel):
    """Response schema for availability slots"""
    slot_id: int
    start_time: str
    end_time: str

class SPOCWithAvailabilityResponse(BaseModel):
    """SPOC with their available time slots"""
    spoc_id: int
    name: str
    expertise: str
    specialization: str
    email: str
    available_slots: List[AvailabilitySlotResponse]

class ClientCreate(BaseModel):
    """Request schema for creating a client"""
    company_name: str
    contact_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    industry: Optional[str] = None
    budget_range: Optional[str] = None
    decision_timeline: Optional[str] = None
    solution_type: Optional[str] = None

class ClientResponse(BaseModel):
    """Response schema for client"""
    client_id: str
    company_name: str
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    created_at: str

class BookingCreate(BaseModel):
    """Request schema for creating a booking"""
    client_id: str
    spoc_id: int
    slot_id: int
    meeting_type: str

class BookingResponse(BaseModel):
    """Response schema for booking"""
    booking_id: str
    client_id: str
    spoc_id: int
    slot_id: int
    meeting_type: str
    booking_status: str
    meeting_link: str
    created_at: str

class BookingConfirmation(BaseModel):
    """Simplified response for booking confirmation"""
    booking_id: str
    message: str
    spoc_name: str
    meeting_link: str
    start_time: str

# =====================================================
# HEALTH & INFO ENDPOINTS
# =====================================================

@app.get("/")
async def root():
    """API root endpoint with basic info"""
    return {
        "message": "SPOC Booking Platform API (Demo - No Database)",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "note": "Using hardcoded in-memory data - perfect for demos"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "mode": "in-memory (no database)"
    }

@app.get("/api/v1/demo/info")
async def demo_info():
    """Get demo information and current status"""
    available_slots_count = len([s for s in AVAILABILITY_SLOTS if not s["is_booked"]])
    booked_slots_count = len([s for s in AVAILABILITY_SLOTS if s["is_booked"]])
    
    return {
        "mode": "in-memory",
        "data_storage": "Python dictionaries and lists",
        "persistence": "Lost on server restart",
        "total_spocs": len(SPOCS_DATA),
        "total_availability_slots": len(AVAILABILITY_SLOTS),
        "available_slots_count": available_slots_count,
        "booked_slots_count": booked_slots_count,
        "clients_created": len(CLIENTS_DATA),
        "bookings_created": len(BOOKINGS_DATA),
        "note": "Perfect for rapid prototyping and demos"
    }

# =====================================================
# SPOC ENDPOINTS
# =====================================================

@app.get("/api/v1/spocs", response_model=List[SPOCResponse])
async def get_spocs(
    solution_type: Optional[str] = Query(None, description="Filter by expertise"),
    expertise: Optional[str] = Query(None, description="Filter by specialization")
):
    """
    Get list of all SPOCs with optional filtering
    
    Query Parameters:
    - solution_type: Filter by solution type (e.g., "Cloud Infrastructure")
    - expertise: Filter by expertise keywords
    
    Returns: List of available SPOCs
    """
    # Start with all SPOCs
    spocs = SPOCS_DATA.copy()
    
    # Apply filters if provided
    if solution_type:
        spocs = [s for s in spocs 
                if solution_type.lower() in s["expertise"].lower()]
    
    if expertise:
        spocs = [s for s in spocs 
                if expertise.lower() in s["specialization"].lower()]
    
    if not spocs:
        raise HTTPException(
            status_code=404, 
            detail="No SPOCs found matching criteria"
        )
    
    return spocs

@app.get("/api/v1/spocs/{spoc_id}", response_model=SPOCResponse)
async def get_spoc_by_id(spoc_id: int):
    """
    Get detailed information about a specific SPOC
    
    Path Parameters:
    - spoc_id: SPOC identifier (1, 2, or 3)
    
    Returns: SPOC information
    """
    spoc = next((s for s in SPOCS_DATA if s["spoc_id"] == spoc_id), None)
    
    if not spoc:
        raise HTTPException(
            status_code=404, 
            detail=f"SPOC with ID {spoc_id} not found"
        )
    
    return spoc

@app.get("/api/v1/spocs/{spoc_id}/availability", response_model=SPOCWithAvailabilityResponse)
async def get_spoc_availability(
    spoc_id: int,
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)")
):
    """
    Get real-time availability for a specific SPOC
    
    This endpoint returns all unbooked time slots for the SPOC,
    optionally filtered by date range.
    
    Path Parameters:
    - spoc_id: SPOC identifier
    
    Query Parameters:
    - start_date: Filter slots starting from this date (ISO format)
    - end_date: Filter slots ending before this date (ISO format)
    
    Returns: SPOC info with available slots
    """
    # Verify SPOC exists
    spoc = next((s for s in SPOCS_DATA if s["spoc_id"] == spoc_id), None)
    if not spoc:
        raise HTTPException(
            status_code=404, 
            detail="SPOC not found"
        )
    
    # Get available slots for this SPOC
    available_slots = [
        s for s in AVAILABILITY_SLOTS
        if s["spoc_id"] == spoc_id and not s["is_booked"]
    ]
    
    # Apply date filters if provided
    if start_date:
        available_slots = [s for s in available_slots 
                          if s["start_time"] >= start_date]
    if end_date:
        available_slots = [s for s in available_slots 
                          if s["end_time"] <= end_date]
    
    # Sort by start time (earliest first)
    available_slots.sort(key=lambda x: x["start_time"])
    
    return {
        "spoc_id": spoc["spoc_id"],
        "name": spoc["name"],
        "expertise": spoc["expertise"],
        "specialization": spoc["specialization"],
        "email": spoc["email"],
        "available_slots": available_slots
    }

# =====================================================
# CLIENT ENDPOINTS
# =====================================================

@app.post("/api/v1/clients", response_model=ClientResponse, status_code=201)
async def create_client(client_data: ClientCreate):
    """
    Create a new client record
    
    When a sales rep fills out the client requirements form,
    this endpoint stores the data in memory and returns client_id
    
    Request Body:
    - company_name: Required
    - contact_name, email, phone: Optional
    - industry, budget_range, decision_timeline: For matching
    - solution_type: For SPOC matching
    
    Returns: Created client with generated client_id
    """
    # Generate unique client ID
    client_id = str(uuid4())[:8]
    
    # Create client record
    new_client = {
        "client_id": client_id,
        **client_data.dict(),
        "created_at": datetime.now().isoformat()
    }
    
    # Store in memory
    CLIENTS_DATA.append(new_client)
    
    return {
        "client_id": new_client["client_id"],
        "company_name": new_client["company_name"],
        "contact_name": new_client.get("contact_name"),
        "contact_email": new_client.get("contact_email"),
        "created_at": new_client["created_at"]
    }

@app.get("/api/v1/clients/{client_id}", response_model=ClientResponse)
async def get_client(client_id: str):
    """
    Get client details by ID
    
    Path Parameters:
    - client_id: Client identifier
    
    Returns: Client information
    """
    client = next(
        (c for c in CLIENTS_DATA if c["client_id"] == client_id), 
        None
    )
    
    if not client:
        raise HTTPException(
            status_code=404, 
            detail="Client not found"
        )
    
    return {
        "client_id": client["client_id"],
        "company_name": client["company_name"],
        "contact_name": client.get("contact_name"),
        "contact_email": client.get("contact_email"),
        "created_at": client["created_at"]
    }

@app.get("/api/v1/clients", response_model=List[ClientResponse])
async def list_clients(
    skip: int = 0,
    limit: int = 100
):
    """
    List all created clients with pagination
    
    Query Parameters:
    - skip: Number of records to skip
    - limit: Maximum records to return
    
    Returns: List of clients
    """
    clients = CLIENTS_DATA[skip:skip+limit]
    
    return [
        {
            "client_id": c["client_id"],
            "company_name": c["company_name"],
            "contact_name": c.get("contact_name"),
            "contact_email": c.get("contact_email"),
            "created_at": c["created_at"]
        }
        for c in clients
    ]

# =====================================================
# BOOKING ENDPOINTS
# =====================================================

@app.post("/api/v1/bookings", response_model=BookingConfirmation, status_code=201)
async def create_booking(booking_data: BookingCreate):
    """
    Create a new demo/POC booking
    
    Complete booking flow:
    1. Validate slot is available (not already booked)
    2. Validate SPOC exists and matches slot
    3. Validate client exists
    4. Generate meeting link
    5. Mark slot as booked
    6. Create booking record
    
    Request Body:
    - client_id: Client making the booking
    - spoc_id: SPOC to conduct the demo
    - slot_id: Time slot being booked
    - meeting_type: Type of meeting (Demo, POC, etc.)
    
    Returns: Booking confirmation with meeting link
    """
    # Step 1: Check slot availability
    slot = next(
        (s for s in AVAILABILITY_SLOTS
         if s["slot_id"] == booking_data.slot_id and not s["is_booked"]),
        None
    )
    
    if not slot:
        raise HTTPException(
            status_code=400, 
            detail="Slot not available or does not exist"
        )
    
    # Step 2: Validate SPOC exists and matches slot
    spoc = next(
        (s for s in SPOCS_DATA if s["spoc_id"] == booking_data.spoc_id),
        None
    )
    
    if not spoc:
        raise HTTPException(
            status_code=404, 
            detail="SPOC not found"
        )
    
    if slot["spoc_id"] != booking_data.spoc_id:
        raise HTTPException(
            status_code=400,
            detail="Selected slot does not belong to this SPOC"
        )
    
    # Step 3: Validate client exists
    client = next(
        (c for c in CLIENTS_DATA if c["client_id"] == booking_data.client_id),
        None
    )
    
    if not client:
        raise HTTPException(
            status_code=404, 
            detail="Client not found"
        )
    
    # Step 4: Generate unique booking ID and meeting link
    booking_id = str(uuid4())[:8]
    meeting_link = f"https://meet.example.com/booking/{booking_id}"
    
    # Step 5: Mark slot as booked
    slot["is_booked"] = True
    
    # Step 6: Create booking record
    new_booking = {
        "booking_id": booking_id,
        "client_id": booking_data.client_id,
        "spoc_id": booking_data.spoc_id,
        "slot_id": booking_data.slot_id,
        "meeting_type": booking_data.meeting_type,
        "booking_status": "Scheduled",
        "meeting_link": meeting_link,
        "created_at": datetime.now().isoformat()
    }
    
    # Store booking in memory
    BOOKINGS_DATA.append(new_booking)
    
    # Return confirmation
    return {
        "booking_id": booking_id,
        "message": "Booking created successfully",
        "spoc_name": spoc["name"],
        "meeting_link": meeting_link,
        "start_time": slot["start_time"]
    }

@app.get("/api/v1/bookings/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: str):
    """
    Get booking details by ID
    
    Path Parameters:
    - booking_id: Booking identifier
    
    Returns: Complete booking information
    """
    booking = next(
        (b for b in BOOKINGS_DATA if b["booking_id"] == booking_id),
        None
    )
    
    if not booking:
        raise HTTPException(
            status_code=404, 
            detail="Booking not found"
        )
    
    return booking

@app.get("/api/v1/bookings", response_model=List[BookingResponse])
async def list_bookings(
    status: Optional[str] = Query(None, description="Filter by status"),
    spoc_id: Optional[int] = Query(None, description="Filter by SPOC"),
    skip: int = 0,
    limit: int = 100
):
    """
    List all bookings with optional filters
    
    Query Parameters:
    - status: Filter by booking status (Scheduled, Completed, Cancelled)
    - spoc_id: Filter by assigned SPOC
    - skip, limit: Pagination
    
    Returns: List of bookings
    """
    bookings = BOOKINGS_DATA.copy()
    
    # Apply filters
    if status:
        bookings = [b for b in bookings if b["booking_status"] == status]
    
    if spoc_id:
        bookings = [b for b in bookings if b["spoc_id"] == spoc_id]
    
    # Sort by creation date (newest first)
    bookings.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Apply pagination
    return bookings[skip:skip+limit]

@app.post("/api/v1/bookings/{booking_id}/cancel")
async def cancel_booking(booking_id: str):
    """
    Cancel an existing booking
    
    Process:
    1. Find the booking
    2. Update status to "Cancelled"
    3. Free up the availability slot
    
    Path Parameters:
    - booking_id: Booking to cancel
    
    Returns: Cancellation confirmation
    """
    # Find booking
    booking = next(
        (b for b in BOOKINGS_DATA if b["booking_id"] == booking_id),
        None
    )
    
    if not booking:
        raise HTTPException(
            status_code=404, 
            detail="Booking not found"
        )
    
    if booking["booking_status"] == "Cancelled":
        raise HTTPException(
            status_code=400, 
            detail="Booking already cancelled"
        )
    
    # Update booking status
    booking["booking_status"] = "Cancelled"
    
    # Free up the slot
    slot = next(
        (s for s in AVAILABILITY_SLOTS if s["slot_id"] == booking["slot_id"]),
        None
    )
    
    if slot:
        slot["is_booked"] = False
    
    return {
        "message": "Booking cancelled successfully",
        "booking_id": booking_id,
        "status": "Cancelled"
    }

# =====================================================
# RUN THE SERVER
# =====================================================

# Run with:
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
#
# Then visit:
# - API Docs: http://localhost:8000/docs
# - Demo Info: http://localhost:8000/api/v1/demo/info
