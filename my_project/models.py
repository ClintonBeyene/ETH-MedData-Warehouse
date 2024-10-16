from sqlalchemy import Column, Integer, Text, TIMESTAMP, INT, String, Float, DateTime
from database import Base

class Products(Base):
    __tablename__ = "Products"

    ID = Column(INT, primary_key=True, index=True)
    Product = Column(Text, index=True)
    Prescription = Column(Text, index=True)
    Price = Column(INT, index=True)
    Address = Column(Text, index=True)
    PhoneNumber = Column(Text, index=True)



class Telegram(Base):
    __tablename__ = "Telegram"

    Channel_username = Column(Text)
    Date = Column(DateTime)
    Media_path = Column(Text)
    ID = Column(INT, primary_key=True)


class Detected_Images(Base):
    __tablename__ = "detected_images"

    Image = Column(String)
    ID = Column(INT, primary_key=True)
    confidence = Column(Float)
    label = Column(String)
    x_max = Column(Float)
    x_min = Column(Float)
    y_max = Column(Float)
    y_min = Column(Float)