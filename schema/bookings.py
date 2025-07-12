from pydantic import BaseModel, ConfigDict

class GetBookings(BaseModel):
    id: int
    customer_id : str
    status : str

    model_config = ConfigDict(from_attributes= True)

