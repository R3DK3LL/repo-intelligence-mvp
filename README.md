Repository Intelligence System MVP

A framework for analyzing git repositories using mathematical metrics to assess development health, collaboration patterns, and process quality.

Overview

This system applies quantitative analysis to repository data, examining commit patterns, collaboration dynamics, and development practices through a structured mathematical approach. The framework provides both programmatic interfaces and command-line tools for repository assessment.

Architecture

The system employs a hybrid design separating the analytical framework from the computational core:

- **Public Framework**: Data collection, API endpoints, CLI tools, and integration scaffolding
- **Analytical Core**: Mathematical engine implementing specialized algorithms (separate distribution)

Current Capabilities

Demo Mode Operation
- Repository data extraction and preprocessing
- Structural analysis of development patterns  
- Collaboration network assessment
- Process health indicators
- Standardized scoring and classification

Interfaces Available
- **REST API**: Programmatic access with JSON responses
- **Command Line**: Direct terminal-based analysis
- **Python Library**: Importable modules for custom applications

Quick Start

Installation
```bash
git clone https://github.com/R3DK3LL/repo-intelligence-mvp.git
cd repo-intelligence-mvp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Command Line Usage
```bash
# Get system information
python cli/analyze.py info

# Analyze a repository
python cli/analyze.py analyze https://github.com/user/repository

# Custom threshold analysis
python cli/analyze.py analyze https://github.com/user/repo -t 0.8 --format summary
```

API Usage
```bash
# Start the API server
python -m uvicorn src.api.main:app --reload

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/demo/analyze

# Interactive documentation
# Visit: http://localhost:8000/docs
```

Programmatic Usage
```python
from src.core.analyzer import RepositoryAnalyzer

analyzer = RepositoryAnalyzer()
result = analyzer.analyze_repository("https://github.com/user/repo")

print(f"Classification: {result['classification']}")
print(f"Score: {result['M_score']:.3f}")
```

Mathematical Foundation

The system implements a structured approach to repository analysis, incorporating:

- **Entropy Measures**: Distribution analysis of development activity
- **Velocity Metrics**: Temporal patterns and development pace assessment  
- **Collaboration Indices**: Network analysis of contributor interactions
- **Process Quality Indicators**: Anti-pattern detection and workflow assessment

The analytical core employs constraint-based optimization and validated mathematical models to ensure consistent, interpretable results across diverse repository types.

Research Applications

This framework supports investigations into:
- Software engineering process optimization
- Development team dynamics and productivity patterns
- Code quality correlation with organizational metrics
- Scalability patterns in open source ecosystems
- Comparative analysis of development methodologies

Professional Use Cases

- **Engineering Management**: Quantitative insights into team productivity and process health
- **DevOps Assessment**: Data-driven evaluation of development workflow efficiency  
- **Quality Assurance**: Systematic identification of process improvement opportunities
- **Research & Analytics**: Empirical foundation for software engineering studies

System Requirements

- Python 3.8+
- Network access for repository data collection
- Optional: GitHub API token for enhanced rate limits

Extensibility

The framework provides extension points for:
- Additional data source integration (GitLab, Bitbucket, etc.)
- Custom metric implementations
- Alternative scoring algorithms
- Export format customization

Contributing

This project follows standard open source contribution practices. The public framework welcomes community improvements while the analytical core remains separately maintained.

License

MIT License - see LICENSE file for details.

The mathematical models and specialized algorithms are subject to separate licensing terms.

Limitations & Considerations

- Demo mode provides representative analysis patterns but not production-grade insights
- GitHub API rate limiting may affect data collection for large repositories
- Full analytical capabilities require the separately distributed computational core
- Repository analysis quality depends on commit history completeness and metadata availability

Support & Documentation

- API Documentation: Available at `/docs` endpoint when running the server
- Examples: See `examples/` directory for usage patterns
- Issues: GitHub issue tracker for framework-related questions

---

*This framework represents active research in quantitative software engineering analysis and process optimization. Results should be interpreted within appropriate methodological contexts.*
