from pydantic import BaseModel

class ReturnMsg(BaseModel):
    msg: str