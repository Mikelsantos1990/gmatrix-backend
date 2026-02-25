from pydantic import BaseModel
from typing import List, Dict, Optional

class Mitarbeiter(BaseModel):
    vorname: str
    nachname: str
    geburtstag: Optional[str] = None
    stunden_pro_woche: Optional[float] = None




class TagesEintrag(BaseModel):
    schicht: Optional[str] = ""
    notiz: Optional[str] = ""
    mitarbeiter: List[str] = []


class UebersichtEintrag(BaseModel):
    filiale: str
    tage: Dict[str, TagesEintrag]


class UebersichtPayload(BaseModel):
    mode: str
    data: List[UebersichtEintrag]