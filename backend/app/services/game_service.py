from datetime import datetime
from sqlalchemy.orm import Session
from ..db.models import Player,Match,PlayerMetric,PolicyEpisode
from ..chess_engine.engine import AdaptiveGame,GameError
from ..features.extractor import extract,vector
from ..rl.selector import RuleSelector
def profile(db:Session,pid:int)->dict:
 rows=db.query(PlayerMetric).filter_by(player_id=pid).all()
 if not rows:return {}
 keys=rows[0].values.keys();return {k:sum(float(r.values.get(k,0)) for r in rows)/len(rows) for k in keys}
def start(db:Session,pid:int,requested:list[int]|None):
 if not db.get(Player,pid):raise GameError('Player not found.')
 metrics=profile(db,pid);ids,why=RuleSelector().select(metrics)
 if requested: AdaptiveGame(requested);ids=requested;why='You manually selected these rules. They are fixed for this match.'
 m=Match(player_id=pid,active_rules=ids,rule_explanation=why);db.add(m);db.commit();db.refresh(m);return state(m)
def load(m:Match):
 g=AdaptiveGame(m.active_rules)
 for d in m.moves:g.move(d['uci'],d.get('elapsed_ms',0))
 return g
def state(m:Match):
 g=load(m);return {'id':m.id,'player_id':m.player_id,'fen':g.board.fen(),'turn':'white' if g.board.turn else 'black','status':m.status,'result':m.result,'active_rules':g.rules.payload(),'explanation':m.rule_explanation,'moves':m.moves,'legal_moves':[x.uci() for x in g.rules.legal_moves(g.board)]}
def play(db:Session,mid:int,uci:str,elapsed:int):
 m=db.get(Match,mid)
 if not m or m.status!='active':raise GameError('Active match not found.')
 g=load(m);g.move(uci,elapsed);m.moves=g.move_log;m.result=g.outcome()
 if m.result!='*':
  m.status='finished';m.ended_at=datetime.utcnow();metrics=extract(m.moves,m.result);db.add(PlayerMetric(player_id=m.player_id,match_id=m.id,values=metrics));reward=0.4+min(len(m.moves)/100,0.3)+(0.2 if m.result=='1/2-1/2' else .1);db.add(PolicyEpisode(player_id=m.player_id,rule_ids=m.active_rules,reward=reward,state=vector(metrics)))
 db.commit();db.refresh(m);return state(m)
