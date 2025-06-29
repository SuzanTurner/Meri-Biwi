from pydantic import BaseModel

class Phonepay(BaseModel):
    id : str
    merchant_transaction_id : str
    status : str

    