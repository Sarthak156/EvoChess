"""Create a local demo profile."""
from app.db.session import SessionLocal
from app.db.models import Player
db=SessionLocal()
if not db.query(Player).filter_by(name='Explorer').first():db.add(Player(name='Explorer'));db.commit()
print('Demo player ready: Explorer')
