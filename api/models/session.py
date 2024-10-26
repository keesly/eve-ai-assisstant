from pydantic import BaseModel

class SessionRequest(BaseModel):
    email: str