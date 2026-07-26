from pydantic import BaseModel,Field
from typing import Any
class PlayerCreate(BaseModel): name:str=Field(min_length=1,max_length=80)
class PlayerOut(BaseModel): id:int; name:str
class NewMatch(BaseModel): player_id:int; requested_rules:list[int]|None=None
class MoveRequest(BaseModel): uci:str; elapsed_ms:int=0; promotion:str|None=None
class MatchOut(BaseModel): id:int; player_id:int; fen:str; turn:str; status:str; result:str; active_rules:list[dict[str,Any]]; explanation:str; moves:list[dict[str,Any]]; legal_moves:list[str]
