from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import Mapped,mapped_column
from .session import Base
class Player(Base):
 __tablename__='players'; id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(80),unique=True); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Match(Base):
 __tablename__='matches'; id:Mapped[int]=mapped_column(primary_key=True); player_id:Mapped[int]=mapped_column(ForeignKey('players.id')); pgn:Mapped[str]=mapped_column(Text,default=''); result:Mapped[str]=mapped_column(String(12),default='*'); status:Mapped[str]=mapped_column(String(20),default='active'); active_rules:Mapped[list]=mapped_column(JSON,default=list); rule_explanation:Mapped[str]=mapped_column(Text,default=''); moves:Mapped[list]=mapped_column(JSON,default=list); started_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); ended_at:Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
class PlayerMetric(Base):
 __tablename__='player_metrics'; id:Mapped[int]=mapped_column(primary_key=True); player_id:Mapped[int]=mapped_column(ForeignKey('players.id')); match_id:Mapped[int]=mapped_column(ForeignKey('matches.id')); values:Mapped[dict]=mapped_column(JSON); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class PolicyEpisode(Base):
 __tablename__='policy_episodes'; id:Mapped[int]=mapped_column(primary_key=True); player_id:Mapped[int]=mapped_column(ForeignKey('players.id')); rule_ids:Mapped[list]=mapped_column(JSON); reward:Mapped[float]=mapped_column(Float); state:Mapped[list]=mapped_column(JSON); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
