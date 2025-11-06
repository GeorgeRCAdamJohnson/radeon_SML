# Radeon AI Documentation

## Overview
Enhanced AI knowledge base with reasoning capabilities for robotics, AI, and technology topics.

## Quick Start

### Local Development
```bash
cd radeon-ai
python server.py
# Access: http://localhost:8000
```

### Deployment
```bash
git add . && git commit -m "Changes" && git push
"/c/Users/biges/AppData/Local/Google/Cloud SDK/google-cloud-sdk/bin/gcloud.cmd" run deploy radeon-ai --source . --platform managed --region us-central1 --allow-unauthenticated --port 8000 --memory 1Gi --cpu 1 --timeout 300 --max-instances 10
```

## Documentation

### Core Documents
- **[Maintenance Guide](maintenance_guide.md)** - How to make changes and deploy
- **[Architecture Overview](architecture_overview.md)** - System design and components
- **[Development Workflow](development_workflow.md)** - Development process and best practices
- **[API Reference](api_reference.md)** - Complete API documentation

### Key Features
- **Enhanced Reasoning Engine** - Semantic understanding and multi-turn context
- **Dynamic Response Generation** - No hardcoded templates
- **Mobile Responsive UI** - Works on all devices
- **Real-time Confidence Scoring** - Evidence-based confidence calculation
- **Multi-domain Knowledge** - 900+ articles across 28 domains

## File Structure
```
radeon-ai/
├── server.py                    # Main FastAPI backend
├── reasoning_agent.py           # Enhanced reasoning system
├── src/react/deploy/index.html  # Frontend application
├── Dockerfile                   # Container configuration
├── requirements.txt             # Python dependencies
├── documents/                   # Documentation
└── scripts/                     # Data collection scripts
```

## Common Tasks

### Add New Response Type
Edit `reasoning_agent.py` → `FactualReasoningStrategy.analyze()`

### Update UI Metrics
Edit `src/react/deploy/index.html` → lines 89-91, 180-182

### Modify API Response
Edit `server.py` → `/api/chat` endpoint

### Deploy Changes
1. Test locally
2. Git commit & push
3. Run gcloud deploy command

## Support
- Check logs: `gcloud logging read "resource.type=cloud_run_revision"`
- Monitor performance: `gcloud run services describe radeon-ai`
- Debug locally: Add print statements and run `python server.py`