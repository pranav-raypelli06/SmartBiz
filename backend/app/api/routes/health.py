from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.app.db.session import get_db, engine
from backend.app.core.config import settings

router = APIRouter()

@router.get("/health")
def get_health(db: Session = Depends(get_db)):
    db_connected = False
    table_count = 0
    server_version = "Unknown"

    try:
        res = db.execute(text("SELECT VERSION();")).fetchone()
        if res:
            server_version = str(res[0])
            db_connected = True

        tables_res = db.execute(text("SHOW TABLES;")).fetchall()
        table_count = len(tables_res)
    except Exception as e:
        db_connected = False
        server_version = f"Error: {str(e)}"

    return {
        "status": "healthy" if db_connected else "degraded",
        "database_connected": db_connected,
        "database_type": "MySQL 8.x (InnoDB)",
        "database_name": settings.DB_NAME,
        "database_host": settings.DB_HOST,
        "database_port": settings.DB_PORT,
        "server_version": server_version,
        "tables_found": table_count,
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }
