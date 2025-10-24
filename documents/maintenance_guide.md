# Radeon AI Maintenance Guide

## Quick Reference

### Key Files
- **server.py** - Main FastAPI backend with reasoning agent integration
- **reasoning_agent.py** - Enhanced reasoning system with semantic understanding
- **src/react/deploy/index.html** - Frontend React application
- **Dockerfile** - Container configuration for deployment

### Common Changes

#### 1. Adding New Response Types
**File**: `reasoning_agent.py`
**Location**: `FactualReasoningStrategy.analyze()`
```python
elif any("new_topic" in e.lower() for e in entities):
    return """NEW TOPIC - COMPREHENSIVE ANALYSIS
    
Your detailed content here...
"""
```

#### 2. Updating UI Metrics
**File**: `src/react/deploy/index.html`
**Lines**: 89-91, 180-182
```html
<div class="metric-value">900+</div>
<div class="metric-label">Articles</div>
```

#### 3. Adding New Knowledge Domains
**File**: `reasoning_agent.py`
**Location**: `SemanticAnalyzer.__init__()`
```python
self.entity_patterns = {
    "new_domain": [r"pattern1", r"pattern2"],
    # existing patterns...
}
```

#### 4. Modifying API Responses
**File**: `server.py`
**Location**: `/api/chat` endpoint
```python
return {
    "new_field": "value",
    # existing fields...
}
```

## Deployment Process

### 1. Local Testing
```bash
cd C:\Users\biges\OneDrive\Desktop\amd_ai\radeon-ai
python server.py
# Test at http://localhost:8000
```

### 2. Git Commit
```bash
git add .
git commit -m "Description of changes"
git push
```

### 3. Google Cloud Deploy
```bash
"/c/Users/biges/AppData/Local/Google/Cloud SDK/google-cloud-sdk/bin/gcloud.cmd" run deploy radeon-ai --source . --platform managed --region us-central1 --allow-unauthenticated --port 8000 --memory 1Gi --cpu 1 --timeout 300 --max-instances 10
```

## Troubleshooting

### Response Issues
- Check `reasoning_agent.py` for entity detection patterns
- Verify response generation in `FactualReasoningStrategy`
- Test semantic analysis with debug prints

### Deployment Issues
- Ensure all files committed to git (Cloud Run builds from repo)
- Check Dockerfile includes new dependencies
- Verify gcloud authentication: `gcloud auth list`

### Frontend Issues
- Check `index.html` for JavaScript errors
- Verify API endpoints match backend routes
- Test connection fallback system

## Performance Monitoring

### Key Metrics
- Response time (target: <2s)
- Confidence scores (target: >0.7)
- Error rates (target: <1%)
- Memory usage (limit: 1Gi)

### Monitoring Commands
```bash
# Check service status
gcloud run services describe radeon-ai --region us-central1

# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=radeon-ai" --limit 50
```