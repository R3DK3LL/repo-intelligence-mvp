"""
Repository Intelligence System - Core Analyzer
Public interface that calls demo mathematical engine
"""

class RepositoryAnalyzer:
    def __init__(self):
        self.demo_available = self._check_demo_engine()
    
    def _check_demo_engine(self):
        """Check if demo mathematical engine is available"""
        try:
            # This will import your demo package when available
            import repo_intelligence_demo
            return True
        except ImportError:
            return False
    
    def analyze_repository(self, repo_url: str, threshold: float = 0.7):
        """
        Analyze repository health using π₁ mathematical formula
        
        Args:
            repo_url: GitHub repository URL
            threshold: Classification threshold (default 0.7)
            
        Returns:
            dict: Analysis results with classification and metrics
        """
        if not self.demo_available:
            return {
                "repository": repo_url,
                "classification": "DEMO_HEALTHY",
                "M_score": 0.75,
                "threshold": threshold,
                "metrics": {
                    "H": 0.8,
                    "V": 0.7, 
                    "C": 0.6,
                    "A": 0.2
                },
                "recommendations": ["Install repo-intelligence-core for full analysis"],
                "demo": False,
                "demo_mode": True
            }
        
        # Import demo engine (only when available)
        from repo_intelligence_demo import MathematicalEngine
        
        # Use demo demo mode formula
        engine = MathematicalEngine()
        result = engine.analyze(repo_url, threshold)
        
        return {
            "repository": repo_url,
            "classification": "HEALTHY" if result["meets_threshold"] else "NEEDS_ATTENTION", 
            "M_score": result["M_score"],
            "threshold": threshold,
            "metrics": result["metrics"],
            "recommendations": result.get("recommendations", []),
            "demo": True
        }
    
    def get_engine_info(self):
        """Get information about available analysis capabilities"""
        if self.demo_available:
            return {
                "engine": "Proprietary π₁ Mathematical Engine",
                "capabilities": ["Full repository analysis", "π₁ formula", "Custom thresholds"],
                "version": "1.0.0"
            }
        else:
            return {
                "engine": "Demo Mode",
                "capabilities": ["Basic structure analysis", "Demo metrics"],
                "message": "Install repo-intelligence-core for full capabilities"
            }
# DEMO VERSION - Full engine available separately
