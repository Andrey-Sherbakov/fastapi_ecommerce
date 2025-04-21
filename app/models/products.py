from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.backend.db import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    slug = Column(String(100), unique=True, index=True)
    description = Column(Text)
    price = Column(Integer)
    image_url = Column(String)
    stock = Column(Integer)
    category_id = Column(Integer, ForeignKey('categories.id'))
    supplier_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    rating = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)

    category = relationship('Category', back_populates='products')
    supplier = relationship('User', back_populates='products')
