# Radeon SML AI - Production-Ready AI Ethics Assistant

[![Production Status](https://img.shields.io/badge/status-production-green)](https://radeon-ai-frontend.netlify.app)
[![API Status](https://img.shields.io/badge/API-active-blue)](https://radeon-ai-960026900565.us-central1.run.app)
[![GitHub](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> **A comprehensive AI knowledge assistant covering robotics, automation, artificial intelligence, and ethics, built from scratch on consumer gaming hardware.**

## 🚀 Quick Links

- **🌐 Live Demo**: https://radeon-ai-frontend.netlify.app
- **🔌 API Endpoint**: https://radeon-ai-960026900565.us-central1.run.app
- **📖 Full Journey**: [docs/project-management/JOURNEY_README.md](docs/project-management/JOURNEY_README.md)
- **🎨 Visual Journey**: [docs/project-management/journey.html](docs/project-management/journey.html)

## 📊 Project Metrics

| Metric | Value |
|--------|-------|
| **Knowledge Base** | 339+ articles, 1M+ words |
| **Response Time** | 2.1s average |
| **Uptime** | 99.7% (30-day) |
| **User Satisfaction** | 4.2/5 |
| **Concurrent Users** | 100+ supported |

## 🏗️ Architecture Overview

```
React Frontend (Netlify) → FastAPI Gateway → Enhanced Reasoning Agent → Vector Database
     ↓                         ↓                      ↓                      ↓
  CDN + PWA               Google Cloud Run      Multiple AI Models      PostgreSQL + Redis
```

**Tech Stack:**
- **Frontend**: Next.js 14, React 18, Tailwind CSS
- **Backend**: FastAPI, Python 3.11, PostgreSQL, Redis
- **AI/ML**: OpenAI API, Vector Search, Custom NLP Pipeline
- **Infrastructure**: Docker, Google Cloud Run, Netlify CDN
- **Monitoring**: Cloud Operations Suite, Custom Analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)
- Google Cloud CLI (for deployment)

### Local Development
```bash
# Clone repository
git clone https://github.com/GeorgeRCAdamJohnson/radeon_SML.git
cd radeon_SML

# Setup Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start development server
python server.py
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Production Deployment
See [docs/deployment/DEPLOY_INSTRUCTIONS.txt](docs/deployment/DEPLOY_INSTRUCTIONS.txt) for comprehensive deployment guide.

## 📁 Project Structure

```
radeon_SML/
├── 📄 README.md                 # This file - project overview
├── 🐳 Dockerfile               # Container configuration
├── 🔧 docker-compose.yml       # Multi-service setup
├── 📋 requirements.txt         # Python dependencies
├── 🚫 .gitignore              # Git exclusions
│
├── 🔌 server.py                # Main API server
├── 🔌 server_enhanced.py       # Enhanced API server
├── 🧠 reasoning_agent.py       # AI reasoning engine
├── 🔍 enhanced_search_utils.py # Search utilities
├── 🕷️ enhanced_wikipedia_crawler.py # Data collection
│
├── 📊 data/                    # Knowledge base and cache
├── 🌐 src/                     # Frontend source code
├── 📝 static/                  # Static assets
├── 🧪 tests/                   # All test files
├── 🔧 scripts/                 # Utility scripts
├── ⚙️ config/                  # Configuration files
│
└── 📚 docs/                    # Documentation (see structure below)
```

## 📚 Documentation Structure

### 🏗️ [docs/architecture/](docs/architecture/)
- `DESIGN_DOCUMENT.md` - Comprehensive system design
- `architecture_overview.md` - High-level architecture
- `knowledge_base_er_diagram.html` - Database schema

### 🚀 [docs/deployment/](docs/deployment/)
- `DEPLOY_INSTRUCTIONS.txt` - Step-by-step deployment
- `setup-ci-cd.md` - CI/CD pipeline setup
- `setup-workload-identity.md` - GCP authentication
- `gcp_security_checklist.md` - Security guidelines

### 📋 [docs/project-management/](docs/project-management/)
- `JOURNEY_README.md` - Complete development journey
- `journey.html` - Visual project narrative
- `LESSONS_LEARNED_v2.md` - Technical lessons learned
- `RADEON-AI-V2-MASTER-PLAN.md` - Version 2 roadmap

### 📊 [docs/reviews/](docs/reviews/)
- `amazon-q-review.md` - External technical assessment
- `amazon-q-v2.md` - Version 2 analysis and roadmap
- `co-pilot-review.md` - Development process review

### 🔧 [docs/hardware/](docs/hardware/)
- `radeon-lowvram-ai.md` - Hardware optimization guide
- `dxdiag_gpu.txt` - System specifications
- Hardware constraint solutions

## 🧪 Testing

### Run Test Suite
```bash
# API tests
python tests/test_api.py

# Reasoning tests  
python tests/test_reasoning.py

# Performance tests
python tests/test_phi2_performance.py

# Deployment validation
python tests/test_deployment.py
```

### Test Coverage
- ✅ API endpoint validation
- ✅ Knowledge base integrity
- ✅ Performance benchmarking
- ✅ Production deployment verification
- ✅ AI reasoning quality checks

## 🔧 Configuration

### Environment Variables
```bash
# API Configuration
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# Deployment
GOOGLE_CLOUD_PROJECT=your_project
NETLIFY_SITE_ID=your_site_id
```

### Configuration Files
- `config/Procfile` - Process definitions
- `config/railway.json` - Railway deployment
- `config/render.yaml` - Render deployment
- `docker-compose.yml` - Local development

## 🛠️ Scripts

### Deployment Scripts ([scripts/deployment/](scripts/deployment/))
```bash
scripts/deployment/deploy_gcp.bat        # Google Cloud deployment
scripts/deployment/docker_deploy.bat     # Docker deployment  
scripts/deployment/start_server.bat      # Local server start
```

### Maintenance Scripts ([scripts/maintenance/](scripts/maintenance/))
```bash
scripts/maintenance/clean_knowledge_base.py  # Knowledge base cleanup
scripts/maintenance/validate_knowledge.py    # Data validation
scripts/maintenance/run_crawler.py          # Update knowledge base
```

## 🚀 Version 3 Roadmap

### Planned Enhancements
- 🎯 **Multi-Modal AI**: Image and video processing
- 🔗 **Real-Time Updates**: Live knowledge base synchronization
- 📱 **Mobile App**: Native iOS/Android applications
- 🤝 **Collaborative Features**: Team workspaces
- 📊 **Advanced Analytics**: User behavior insights
- 🔐 **Enterprise Security**: SSO and audit logging

### Technical Improvements
- 🏗️ **Microservices**: Service-oriented architecture
- ⚡ **Performance**: Sub-second response times
- 🌍 **Multi-Language**: Internationalization support
- 🔄 **Auto-Scaling**: Dynamic resource management

## 🤝 Contributing

### For Human Contributors
1. Read [docs/project-management/development_workflow.md](docs/project-management/development_workflow.md)
2. Check [docs/project-management/maintenance_guide.md](docs/project-management/maintenance_guide.md)
3. Follow testing guidelines in [tests/README.md](tests/README.md)

### For AI Agents
1. Review [docs/architecture/DESIGN_DOCUMENT.md](docs/architecture/DESIGN_DOCUMENT.md)
2. Understand the journey in [docs/project-management/JOURNEY_README.md](docs/project-management/JOURNEY_README.md)
3. Check current metrics and status endpoints
4. Follow established patterns in codebase

### Development Guidelines
- ✅ Write tests for new features
- ✅ Update documentation for changes
- ✅ Follow existing code patterns
- ✅ Test locally before submitting
- ✅ Include performance considerations

## 📞 Support & Contact

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Documentation**: All docs are in the `docs/` directory
- **Community**: Check discussions for Q&A and feature discussions
- **Security**: Report security issues via GitHub Security tab

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎖️ Acknowledgments

- Built with determination on consumer gaming hardware (Legion Go + Radeon Graphics)
- Powered by open-source technologies and cloud platforms
- Validated by external technical assessments (Amazon Q Reviews)
- Community-driven development and feedback

---

**📍 Status**: Production Ready | **🔄 Version**: 2.1 | **📅 Last Updated**: November 2025

*Built with persistence, powered by curiosity, deployed with pride.*