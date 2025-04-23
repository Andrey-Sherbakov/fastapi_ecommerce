from sqlalchemy import Column, Integer, Text, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.backend.db import Base


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    comment = Column(Text, nullable=True)
    comment_date = Column(Date)
    grade = Column(Float)
    is_active = Column(Boolean, default=True)

    customer = relationship('User', back_populates='reviews')
    product = relationship('Product', back_populates='reviews')
