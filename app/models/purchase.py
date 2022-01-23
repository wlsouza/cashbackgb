from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from app.database.base import Base

# I preferred to keep the cashbask value instead of the percentage because in
# a possible sum of purchases it would be expensive (in computational
# resources) to calculate the cashback value of each purchase.
# And in the reverse scenario (sum of the percentages) it makes no sense.


class Purchase(Base):

    __tablename__ = "purchase"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True, unique=True, nullable=False)
    value = Column(Numeric, nullable=False)
    date = Column(Date, nullable=False)
    cashback_value = Column(Numeric, nullable=False)
    status_id = Column(Integer, ForeignKey("purchase_status.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    time_created = Column(
        DateTime, nullable=False, default=datetime.utcnow()
    )
    time_updated = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
    )

    status = relationship("PurchaseStatus", back_populates="purchases")
    user = relationship("User", back_populates="purchases")
