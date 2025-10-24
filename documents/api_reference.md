# API Reference

## Endpoints

### POST /api/chat
Main chat endpoint for processing user queries.

**Request Body:**
```json
{
  "message": "What is a robot?",
  "format": "detailed",
  "session_id": "web-session"
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "response": "Detailed response text",
  "timestamp": 1234567890,
  "confidence": 0.85,
  "intent": "factual",
  "sources": 4,
  "processing_time": 1.2,
  "from_cache": false,
  "safety_blocked": false,
  "reasoning_steps": [
    {
      "type": "knowledge_retrieval",
      "content": "Retrieved relevant sources",
      "confidence": 0.9
    }
  ],
  "entities_detected": [
    {
      "text": "robot",
      "category": "robot"
    }
  ],
  "complexity_level": "simple",
  "session_context_turns": 1,
  "related_topics": ["Robotics Technology", "AI Applications"],
  "follow_up_suggestions": [
    "Tell me more about robot",
    "What are examples of robot?",
    "How does this technology work?"
  ]
}
```

### GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "reasoning_agent": "active"
}
```

### GET /api/status
System status and statistics.

**Response:**
```json
{
  "system_name": "Enhanced Radeon AI Knowledge Base",
  "version": "2.0.0",
  "reasoning_agent": {
    "status": "active",
    "capabilities": ["semantic_analysis", "multi_turn_context", "reasoning_chains"],
    "confidence_calculation": "evidence_based"
  },
  "knowledge_stats": {
    "total_articles": 900,
    "total_words": 4200000,
    "enhanced_reasoning": true,
    "ethics_articles": 93,
    "domains_covered": 28
  }
}
```

## Request Parameters

### Chat Request
- **message** (required): User query string
- **format** (optional): Response format ("summary", "detailed", "list")
- **session_id** (optional): Session identifier for context tracking

### Response Fields

#### Core Response
- **id**: Unique response identifier
- **response**: Generated response text
- **timestamp**: Unix timestamp
- **confidence**: Confidence score (0.0-1.0)

#### Reasoning Metadata
- **intent**: Detected intent type (factual, comparative, analytical)
- **complexity_level**: Query complexity (simple, moderate, complex, multi_step)
- **reasoning_steps**: Array of reasoning process steps
- **entities_detected**: Extracted entities with categories

#### Context & Suggestions
- **session_context_turns**: Number of conversation turns
- **related_topics**: Suggested related topics
- **follow_up_suggestions**: Suggested follow-up questions

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request format"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Usage Examples

### Basic Query
```javascript
fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "What is artificial intelligence?",
    format: "detailed"
  })
})
```

### Follow-up Query
```javascript
fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "Tell me more about machine learning",
    format: "detailed",
    session_id: "user-123"
  })
})
```