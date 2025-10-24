# Development Workflow

## Local Development Setup

### 1. Environment Setup
```bash
cd C:\Users\biges\OneDrive\Desktop\amd_ai\radeon-ai
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Run Locally
```bash
python server.py
# Access: http://localhost:8000
```

### 3. Test Changes
- Frontend: Edit `src/react/deploy/index.html`
- Backend: Edit `server.py` or `reasoning_agent.py`
- Refresh browser to see changes

## Making Changes

### Adding New Knowledge Domain
1. **Update Entity Patterns** (`reasoning_agent.py`)
```python
self.entity_patterns = {
    "new_domain": [r"keyword1", r"keyword2"],
}
```

2. **Add Response Content** (`reasoning_agent.py`)
```python
elif any("new_domain" in e.lower() for e in entities):
    return """DETAILED RESPONSE CONTENT"""
```

3. **Test Locally**
```bash
python server.py
# Test queries containing new keywords
```

### Updating UI Content
1. **Edit Frontend** (`src/react/deploy/index.html`)
2. **Update Metrics** (lines 89-91, 180-182)
3. **Modify Styling** (CSS section)
4. **Test Responsiveness** (mobile/desktop)

### Modifying API Behavior
1. **Edit Endpoints** (`server.py`)
2. **Update Response Format**
3. **Test with Frontend**
4. **Verify Error Handling**

## Git Workflow

### Standard Process
```bash
# 1. Make changes
# 2. Test locally
git add .
git status  # Review changes
git commit -m "Descriptive message"
git push
```

### Deployment
```bash
# After git push, deploy to Cloud Run
"/c/Users/biges/AppData/Local/Google/Cloud SDK/google-cloud-sdk/bin/gcloud.cmd" run deploy radeon-ai --source . --platform managed --region us-central1 --allow-unauthenticated --port 8000 --memory 1Gi --cpu 1 --timeout 300 --max-instances 10
```

## Testing Checklist

### Before Deployment
- [ ] Local server runs without errors
- [ ] Frontend loads and displays correctly
- [ ] API endpoints return expected responses
- [ ] Mobile responsiveness works
- [ ] New features function as intended
- [ ] No console errors in browser

### After Deployment
- [ ] Production URL accessible
- [ ] All features work in production
- [ ] Performance acceptable (<2s response)
- [ ] No server errors in logs
- [ ] Mobile/desktop compatibility

## Common Issues

### Local Development
- **Port conflicts**: Change port in `server.py`
- **Module imports**: Ensure `reasoning_agent.py` in same directory
- **CORS errors**: Check middleware configuration

### Deployment
- **Build failures**: Check Dockerfile and requirements.txt
- **Import errors**: Verify all files committed to git
- **Memory issues**: Increase memory allocation in deploy command

### Frontend
- **API connection**: Check endpoint URLs in JavaScript
- **Styling issues**: Test across browsers
- **Mobile layout**: Verify responsive design breakpoints