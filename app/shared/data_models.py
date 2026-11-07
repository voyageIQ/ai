from pydantic import BaseModel, Field
from constants import DEFAULT_CURRENCY, CURRENCY_SYMBOLS
from typing import Optional

class HotelOffer(BaseModel):
    room_type: str
    quantity: int = Field(..., gt=0, description="Must be greater than 0")
    offer_id: str
    hotel_id: str
    hotel_name: str
    supplier_name: str
    price: float = Field(..., gt=0, description="Must be greater than 0")
    currency: str = Field(default=DEFAULT_CURRENCY)
    nights: int = Field(default=1, ge=1)
    days: int = Field(default=1, ge=1)
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    location: str = Field(..., description="Location of the hotel")
    country: str = Field(..., description="Country of the hotel")
    contact_no: Optional[str] = Field(..., description="Contact number of the hotel")
    contact_email: Optional[str] = Field(..., description="Contact email of the hotel")
    image_url: Optional[str] = Field(..., description="Image URL of the hotel")