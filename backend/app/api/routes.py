from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Player,Match,PlayerMetric,PolicyEpisode
from app.schemas.contracts import *
from app.services.game_service import start,play,state,profile
from app.chess_engine.rules import RULES
from app.chess_engine.engine import GameError
router=APIRouter(prefix='/api')
def err(e):raise HTTPException(400,str(e))
@router.post('/players',response_model=PlayerOut)
def create_player(x:PlayerCreate,db:Session=Depends(get_db)):
 p=Player(name=x.name);db.add(p)
 try:db.commit();db.refresh(p);return p
 except Exception:db.rollback();raise HTTPException(409,'Player name already exists.')
@router.get('/players',response_model=list[PlayerOut])
def players(db:Session=Depends(get_db)):return db.query(Player).all()
@router.post('/matches',response_model=MatchOut)
def new_match(x:NewMatch,db:Session=Depends(get_db)):
 try:return start(db,x.player_id,x.requested_rules)
 except GameError as e:err(e)
@router.get('/matches/{match_id}',response_model=MatchOut)
def get_match(match_id:int,db:Session=Depends(get_db)):
 m=db.get(Match,match_id)
 if not m:raise HTTPException(404,'Match not found')
 return state(m)
@router.post('/matches/{match_id}/moves',response_model=MatchOut)
def move(match_id:int,x:MoveRequest,db:Session=Depends(get_db)):
 try:return play(db,match_id,x.uci,x.elapsed_ms)
 except GameError as e:err(e)
@router.get('/rules')
def rules():return [{'id':x.id,'name':x.name,'description':x.description,'counters':x.counters} for x in RULES.values()]
@router.get('/players/{player_id}/analytics')
def analytics(player_id:int,db:Session=Depends(get_db)):
 return {'profile':profile(db,player_id),'matches':db.query(Match).filter_by(player_id=player_id).count(),'episodes':[{'reward':x.reward,'rules':x.rule_ids,'at':x.created_at} for x in db.query(PolicyEpisode).filter_by(player_id=player_id).order_by(PolicyEpisode.id.desc()).limit(50)]}
@router.get('/dashboard')
def dashboard(db:Session=Depends(get_db)):
 eps=db.query(PolicyEpisode).all();usage={str(i):0 for i in RULES}
 for e in eps:
  for i in e.rule_ids:usage[str(i)]+=1
 return {'episode_count':len(eps),'average_reward':sum(x.reward for x in eps)/len(eps) if eps else 0,'rule_usage':usage,'reward_curve':[x.reward for x in eps[-100:]],'policy':'PPO-ready contextual rule selection'}
