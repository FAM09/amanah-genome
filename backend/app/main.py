"""
FastAPI Application Entrypoint for Amanah-Genome (أمانة للجينوم)
Zero-Knowledge Pre-Marital Genetic Compatibility & Cultural Care Bridge.
Target: Future Health Digital Innovation Challenge 2026 (Abu Dhabi - GITEX 2026).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_counselor import router as counselor_router
from app.api.routes_session import router as session_router
from app.bio.panel import get_all_panel_genes

app = FastAPI(
    title="Amanah-Genome API (أمانة للجينوم)",
    description=(
        "Zero-Knowledge Pre-Marital Genetic Compatibility Screening and "
        "Cultural AI Pre-Conception Care Bridge (Abu Dhabi DoH Guidelines)."
    ),
    version="1.0.0",
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(session_router)
app.include_router(counselor_router)


@app.get("/")
def root():
    return {
        "project": "Amanah-Genome (أمانة للجينوم)",
        "mission": "Zero-Knowledge Pre-Marital Genetic Compatibility & Cultural Care Bridge",
        "competition": "Future Health Digital Innovation Challenge 2026 (Abu Dhabi)",
        "status": "Operational",
        "version": "1.0.0",
        "docs_url": "/docs",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "amanah-genome-backend",
        "crypto_engine": "AES/HMAC-SHA256 Private Set Intersection",
        "panel_count": len(get_all_panel_genes()),
    }


@app.get("/api/panel")
def get_uae_recessive_panel():
    """Retrieve full clinical metadata for the UAE Priority Recessive Disorder Panel."""
    return {
        "region": "United Arab Emirates & GCC",
        "guideline_authority": "Department of Health Abu Dhabi (DoH)",
        "panel_count": len(get_all_panel_genes()),
        "genes": get_all_panel_genes(),
    }
