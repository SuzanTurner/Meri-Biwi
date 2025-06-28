from pydantic import BaseModel
from typing import Optional

class Notifications(BaseModel):
    title : str
    msg : str
    msg_type : Optional[str] = None