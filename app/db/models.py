from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base

class WalletQuery(Base):
    __tablename__ = "wallet_queries"

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, index=True)
    bandwidth = Column(Integer)
    energy = Column(Integer)
    trx_balance = Column(Integer)
    query_time = Column(DateTime, default=datetime.utcnow)