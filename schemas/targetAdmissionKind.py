from pydantic import BaseModel


class targetAdmissionKind(BaseModel):
    priority: str = ""
    used: str = ""
    shortTitle: str = ""
    title: str = ""
    id: str = ""
