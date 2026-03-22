from dataclasses import dataclass, field
from typing import List

@dataclass
class Card:
    id: int
    name: str
    card_type: str  # 'unit', 'spell', 'environment'
    cost: int
    groups: List[str] = field(default_factory=list)
    rarity: str = "Común"
    description: str = ""

    def __post_init__(self):
        # Limpia los grupos si vienen como un string sucio del CSV
        if isinstance(self.groups, str):
            self.groups = [g.strip() for g in self.groups.split(',') if g.strip()]