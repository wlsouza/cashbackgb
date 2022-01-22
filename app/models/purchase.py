from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime, Date
from sqlalchemy.orm import relationship 

from app.database.base import Base

# TODO: Insert column to get datetime of the last update.

class Purchase(Base):

    __tablename__ = "purchase"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    value = Column(Numeric, unique=True, index=True, nullable=False)
    date = Column(Date, nullable=False)
    status_id = Column(Integer, ForeignKey("purchase_status.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    time_created = Column(
        DateTime, index=False, nullable=False, default=datetime.utcnow()
    )
    time_updated = Column(
        DateTime, index=False, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )

    status = relationship("PurchaseStatus", back_populates="purchases")
    user = relationship("User", back_populates="purchases")
