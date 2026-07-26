import chess, numpy as np
FEATURE_NAMES=['queen_usage','knight_usage','bishop_usage','pawn_aggression','avg_move_time','capture_frequency','center_control','castling_preference','check_frequency','sacrifice_score','opening_variety','endgame_activity','games','win_rate']
def extract(moves:list[dict],result:str='*')->dict[str,float]:
 b=chess.Board();counts={p:0 for p in range(1,7)};caps=checks=center=castle=pawn_pushes=0;times=[]
 for d in moves:
  try:m=chess.Move.from_uci(d['uci']);p=b.piece_at(m.from_square)
  except Exception:continue
  if not p:continue
  counts[p.piece_type]+=1;caps+=int(b.is_capture(m));castle+=int(b.is_castling(m));pawn_pushes+=int(p.piece_type==1 and chess.square_rank(m.to_square) in (3,4));times.append(d.get('elapsed_ms',0));b.push(m);checks+=int(b.is_check());center+=int(m.to_square in [chess.D4,chess.E4,chess.D5,chess.E5])
 n=max(len(moves),1);return {'queen_usage':counts[5]/n,'knight_usage':counts[2]/n,'bishop_usage':counts[3]/n,'pawn_aggression':pawn_pushes/n,'avg_move_time':float(np.mean(times) if times else 0),'capture_frequency':caps/n,'center_control':center/n,'castling_preference':castle,'check_frequency':checks/n,'sacrifice_score':0.,'opening_variety':len(set(x['uci'][:2] for x in moves[:10]))/10,'endgame_activity':sum(1 for _ in moves[60:])/n,'games':1.,'win_rate':1. if result=='1-0' else .5 if result=='1/2-1/2' else 0.}
def vector(metrics:dict[str,float])->list[float]:return [float(metrics.get(k,0)) for k in FEATURE_NAMES]
