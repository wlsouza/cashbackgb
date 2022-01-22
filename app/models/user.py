from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database.base import Base

class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True, unique=True, nullable=False)
    cpf = Column(String(11),index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    time_created = Column(
        DateTime, index=False, nullable=False, default=datetime.utcnow()
    )
    time_updated = Column(
        DateTime, index=False, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )

    purchases = relationship("Purchase", back_populates="user")