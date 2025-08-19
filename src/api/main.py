"""
Repository Intelligence API
FastAPI application providing REST endpoints for repository analysis
"""
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
import os

from ..core.analyzer import RepositoryAnalyzer
from ..collectors.github_collector import GitHubCollector

app = FastAPI(
    title="Repository Intelligence API",
    description="Analyze GitHub repositories using mathematical metrics",
    version="1.0.0"
)

# Pydantic models
class AnalysisRequest(BaseModel):
    repo_url: HttpUrl
    threshold: Optional[float] = 0.7

class AnalysisResponse(BaseModel):
    repository: str
    classification: str
    M_score: float
    threshold: float
    metrics: Dict[str, float]
    recommendations: Optional[list] = []
    proprietary: bool = True
    demo_mode: Optional[bool] = False

class EngineInfoResponse(BaseModel):
    engine: str
    capabilities: list
    version: Optional[str] = None
    message: Optional[str] = None

# Dependency to get analyzer instance
def get_analyzer():
    return RepositoryAnalyzer()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Repository Intelligence API",
        "version": "1.0.0", 
        "description": "Analyze GitHub repositories using π₁ mathematical formula",
        "endpoints": {
            "analyze": "/analyze",
            "engine_info": "/engine/info",
            "health": "/health"
        }
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_repository(
    request: AnalysisRequest,
    analyzer: RepositoryAnalyzer = Depends(get_analyzer)
):
    """
    Analyze a GitHub repository
    
    Analyzes the repository using the π₁ mathematical formula and returns
    health classification, metrics breakdown, and recommendations.
    """
    try:
        result = analyzer.analyze_repository(str(request.repo_url), request.threshold)
        return AnalysisResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Analysis failed: {str(e)}")

@app.get("/engine/info", response_model=EngineInfoResponse)
async def get_engine_info(analyzer: RepositoryAnalyzer = Depends(get_analyzer)):
    """Get information about the analysis engine"""
    info = analyzer.get_engine_info()
    return EngineInfoResponse(**info)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    analyzer = RepositoryAnalyzer()
    return {
        "status": "healthy",
        "proprietary_engine_available": analyzer.proprietary_available,
        "version": "1.0.0"
    }

@app.get("/demo/analyze")
async def demo_analysis():
    """
    Demo endpoint showing example analysis result
    Useful for testing API integration without analyzing real repositories
    """
    return {
        "repository": "https://github.com/example/demo",
        "classification": "HEALTHY",
        "M_score": 0.782,
        "threshold": 0.7,
        "metrics": {
            "H": 0.85,  # High commit entropy (good distribution)
            "V": 0.72,  # Good velocity
            "C": 0.68,  # Decent collaboration
            "A": 0.15   # Low anti-patterns (good)
        },
        "recommendations": [
            "Consider increasing PR review coverage",
            "Monitor for long-lived feature branches"
        ],
        "proprietary": True,
        "demo_mode": True
    }

# Error handlers  
from fastapi.responses import JSONResponse

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "detail": "Check API documentation at /docs"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "Please try again later"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# This is the public demonstration framework
