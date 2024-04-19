from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



#อยู่ใน database
# DATABASE_URL = "mysql+pymysql://root:@localhost:3306/sql"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
app = FastAPI()

#อยู่ใน model
# class Room(Base):
#     __tablename__ = 'rooms'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)

# class Booking(Base):
#     __tablename__ = 'bookings'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     guest_name = Column(String(100), nullable=False)
#     room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    

# #สร้างตาราง
# Base.metadata.create_all(bind=engine)

        
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/rooms/")
def create_room(name: str, db: Session = Depends(get_db)):
    new_room = Room(name=name)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return {"id": new_room.id, "name": new_room.name}


@app.post("/bookings/")
def create_booking(guest_name: str, room_id: int, db: Session = Depends(get_db)):
    new_booking = Booking(guest_name=guest_name, room_id=room_id)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return {"id": new_booking.id, "guest_name": new_booking.guest_name, "room_id": new_booking.room_id}

@app.get("/bookings/{booking_id}")
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking is None:
        return {"error": "Booking not found"}
    return booking

@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking is None:
        return {"error": "Booking not found"}
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}