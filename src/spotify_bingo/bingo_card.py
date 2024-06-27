from dataclasses import dataclass
from typing import List

@dataclass
class Song:
    title: str
    artist: str
    image_path: str

@dataclass
class BingoCard:
    songs: List[Song]
    width: int
    height: int
    
