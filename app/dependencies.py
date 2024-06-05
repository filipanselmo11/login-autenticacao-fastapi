from app.database.connection import Session

def get_db_sesion():
    try:
        session = Session()
        yield session
    finally:
        session.close()