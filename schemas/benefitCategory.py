from pydantic import BaseModel


class benefitCategory(BaseModel):
    shortTitle: str = ""
    title: str = ""
    id: str = ""
