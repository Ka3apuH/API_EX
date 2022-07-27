from typing import List

from pydantic import BaseModel


class passForms(BaseModel):
    title: str = ""
    id: str = ""


class entranceDiscipline(BaseModel):
    id: str = ""
    title: str = ""
    shortTitle: str = ""
    priority: str = ""
    examType: str = ""
    passMarkMultipliedBy1000: str = ""
    passForms: List[passForms] = []
