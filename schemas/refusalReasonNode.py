from pydantic import BaseModel


class refusalReasonNode(BaseModel):
    title: str = ""
    id: str = ""