from pydantic import BaseModel


class TicketBaseSchema(BaseModel):
    message: str
    user: str 

class TicketRetrieveSchema(TicketBaseSchema):
    id: str


    