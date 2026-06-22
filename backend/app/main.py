from fastapi import FastAPI
from app.core.config import settings
from sqlalchemy import text
from app.db.database import engine
from app.db.base import Base
from app.db.database import engine
from sqlalchemy import inspect

import app.models

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return{
        "message": "TradeMindAI Backend Running"
    }

@app.get("/health")
def health():
    return{
        "status": "healthy"
    }

@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as connections:
            result = connections.execute(
                text("SELECT 1")
            )

            return {
                "database": "connected",
                "result": result.scalar()
            }
    except Exception as e:
        return{
            "database": "failed",
            "error": str(e)
        }
    
@app.get("/tables")
def get_tables():
    inspector = inspect(engine)
    return {
        "tables": inspector.get_table_names()
    }