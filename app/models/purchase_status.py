from datetime import datetime
from enum import unique

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class PurchaseStatus(Base):

    __tablename__ = "purchase_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    description = Column(String, index=False)
    time_created = Column(
        DateTime, nullable=False, default=datetime.utcnow()
    )
    time_updated = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
    )

    purchases_ = relationship("Purchase", back_populates="status_", lazy="joined")

    # __mapper_args__ = {"eager_defaults": True}