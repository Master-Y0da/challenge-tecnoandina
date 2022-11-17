from config.config import SessionLocal


# Session DB
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
