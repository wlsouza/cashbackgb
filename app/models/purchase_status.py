from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database.base import Base

class PurchaseStatus(Base):

    __tablename__ = "purchase_status"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    time_created = Column(
        DateTime, index=False, nullable=False, default=datetime.utcnow()
    )
    time_updated = Column(
        DateTime, index=False, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )

    purchases = relationship("Purchase", back_populates="status")