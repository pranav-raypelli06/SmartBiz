import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.db.session import engine, Base
import backend.app.models # Register all models with Base
from backend.app.api.routes import (
    health, dashboard, business, customers, forecasting,
    inventory, anomalies, algorithms, data_mgmt
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables are created
    try:
        Base.metadata.create_all(bind=engine)
        print("[STARTUP] MySQL database tables verified/created successfully.")
    except Exception as e:
        print(f"[STARTUP ERROR] Database table initialization error: {e}")
    yield
    # Shutdown
    print("[SHUTDOWN] Application shutting down.")

app = FastAPI(
    title="SmartBiz Analytics API",
    description="Full-stack business intelligence, predictive forecasting, inventory optimization, and Algorithm Lab API.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, allow frontend connections
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes Registration
app.include_router(health.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(business.router, prefix="/api")
app.include_router(customers.router, prefix="/api")
app.include_router(forecasting.router, prefix="/api")
app.include_router(inventory.router, prefix="/api")
app.include_router(anomalies.router, prefix="/api")
app.include_router(algorithms.router, prefix="/api")
app.include_router(data_mgmt.router, prefix="/api")

@app.get("/")
def root():
    return {
        "app": settings.PROJECT_NAME,
        "tagline": "Turn Business Data Into Smarter Decisions.",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=settings.API_PORT, reload=True)
