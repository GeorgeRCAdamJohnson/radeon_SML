# Radeon AI Architecture Overview

## System Components

### Backend (Python FastAPI)
```
server.py
├── Enhanced Reasoning Agent Integration
├── API Endpoints (/api/chat, /api/status, /api/health)
├── Static File Serving
└── CORS Configuration
```

### Reasoning Engine
```
reasoning_agent.py
├── SemanticAnalyzer (Intent + Entity Detection)
├── ReasoningPipeline (Strategy Pattern)
├── ContextManager (Multi-turn Conversations)
└── PromptEngineer (Dynamic Prompt Construction)
```

### Frontend (React)
```
src/react/deploy/index.html
├── Chat Interface
├── Connection Fallback System
├── Mobile Responsive Design
└── Real-time Metrics Display
```

## Data Flow

1. **User Input** → Frontend captures message
2. **API Request** → POST to `/api/chat`
3. **Semantic Analysis** → Extract intent, entities, complexity
4. **Reasoning Pipeline** → Apply appropriate strategy
5. **Context Integration** → Build on conversation history
6. **Response Generation** → Dynamic content creation
7. **Frontend Display** → Render response with metadata

## Key Design Patterns

### Strategy Pattern (Reasoning)
```python
reasoning_strategies = {
    'factual': FactualReasoningStrategy(),
    'comparative': ComparativeReasoningStrategy(),
    'analytical': AnalyticalReasoningStrategy()
}
```

### Session Management
```python
session_contexts = {
    session_id: SessionContext(conversation_history, reasoning_history)
}
```

### Fallback System
```javascript
const endpoints = [
    'http://localhost:8000',
    'https://radeon-ai-production-url',
    'https://backup-server-url'
];
```

## Technology Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn
- **AI/ML**: Custom reasoning engine, semantic analysis
- **Frontend**: Vanilla JavaScript, CSS Grid, Responsive Design
- **Deployment**: Docker, Google Cloud Run
- **Data**: JSON-based knowledge storage
- **Version Control**: Git, GitHub