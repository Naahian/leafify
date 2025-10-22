from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from typing import Dict, Any
import time

from app.models.user_model import User
from app.routes.auth_route import get_current_user
from database import get_db, engine

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def basic_health_check():
    """
    Basic health check - just confirms API is running
    Use this for simple uptime monitoring
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Plant Store API",
    }


@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Detailed health check - verifies all critical services

    Checks:
    - API status
    - Database connection
    - Database query performance
    - System timestamp
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {},
    }

    # 1. API Check (always passes if we get here)
    health_status["checks"]["api"] = {"status": "healthy", "message": "API is running"}

    # 2. Database Connection Check
    try:
        start_time = time.time()
        db.execute(text("SELECT 1"))
        db_response_time = (time.time() - start_time) * 1000  # Convert to ms

        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful",
            "response_time_ms": round(db_response_time, 2),
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}",
        }

    # 3. Database Read Check (verify tables exist)
    try:
        start_time = time.time()
        # Try to count users (will fail if table doesn't exist)
        result = db.execute(text("SELECT COUNT(*) FROM users"))
        user_count = result.scalar()
        query_time = (time.time() - start_time) * 1000

        health_status["checks"]["database_tables"] = {
            "status": "healthy",
            "message": "Database tables accessible",
            "user_count": user_count,
            "query_time_ms": round(query_time, 2),
        }
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["database_tables"] = {
            "status": "degraded",
            "message": f"Database tables check failed: {str(e)}",
        }

    # 4. System Time Check
    health_status["checks"]["system"] = {
        "status": "healthy",
        "server_time": datetime.utcnow().isoformat(),
        "timezone": "UTC",
    }

    return health_status


@router.get("/live")
async def liveness_check():
    """
    Liveness check - for Kubernetes/container orchestration
    Returns 200 if app is alive (even if dependencies are down)
    This should almost never fail
    """
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}


@router.get("/db-stats")
async def database_statistics(
    db: Session = Depends(get_db),
    #   current_user: User = Depends(get_current_user),
):
    """
    Database statistics - useful for monitoring
    """
    try:
        stats = {}

        # Count records in each table
        tables = [
            "users",
            "products",
            "plants",
            "accessories",
            "plant_guides",
            "orders",
        ]

        for table in tables:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                stats[table] = result.scalar()
            except Exception as e:
                stats[table] = f"Error: {str(e)}"

        # Database size (PostgreSQL specific)
        try:
            result = db.execute(text("SELECT pg_database_size(current_database())"))
            db_size_bytes = result.scalar()
            stats["database_size_mb"] = round(db_size_bytes / (1024 * 1024), 2)
        except:
            stats["database_size_mb"] = "N/A"

        return {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "statistics": stats,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.utcnow().isoformat(),
        }
