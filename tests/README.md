# Testing Documentation

This directory contains all testing files and documentation for the Radeon SML AI project.

## 📁 Test Files Structure

### API Testing
- `test_api.py` - Core API endpoint testing
- `test_api_results.json` - API test results and benchmarks
- `test_api_validation_results.json` - API validation outcomes

### System Testing  
- `test_deployment.py` - Production deployment verification
- `test_local.py` - Local development environment testing
- `test_browser.html` - Browser-based testing interface

### Performance Testing
- `test_phi2_performance.py` - AI model performance benchmarks
- `production_comparison_results.json` - Production vs local comparisons

### Reasoning & AI Testing
- `test_reasoning.py` - AI reasoning quality validation
- `backend_reasoning_test_results.json` - Reasoning test outcomes

### Query Testing
- `test_query.json` - Sample queries for testing
- `test_query2.json` - Additional test queries

## 🧪 Test Categories

### 1. Unit Tests
- Individual function testing
- Component isolation testing
- Mock data validation

### 2. Integration Tests  
- API endpoint integration
- Database connectivity
- External service integration

### 3. Performance Tests
- Response time benchmarks
- Load testing scenarios
- Memory usage analysis

### 4. End-to-End Tests
- Complete user workflow testing
- Production environment validation
- Cross-browser compatibility

## 🚀 Running Tests

### All Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=.
```

### Specific Test Categories
```bash
# API tests only
python tests/test_api.py

# Performance tests
python tests/test_phi2_performance.py

# Reasoning validation
python tests/test_reasoning.py

# Deployment verification
python tests/test_deployment.py
```

### Browser Tests
Open `test_browser.html` in a web browser for interactive testing.

## 📊 Test Metrics & Benchmarks

### Current Performance Targets
- **API Response Time**: < 2.5 seconds average
- **Memory Usage**: < 2GB peak
- **Uptime**: > 99.5%
- **User Satisfaction**: > 4.0/5

### Test Coverage Goals
- **Unit Tests**: > 80% code coverage
- **API Tests**: 100% endpoint coverage
- **Integration Tests**: All critical paths
- **Performance Tests**: All user scenarios

## 🔧 Test Configuration

### Environment Variables
```bash
# Test environment
TEST_MODE=true
API_BASE_URL=http://localhost:8000
TEST_TIMEOUT=30

# Performance testing
PERFORMANCE_TEST_ITERATIONS=100
LOAD_TEST_CONCURRENT_USERS=50
```

### Test Data
- Mock data is generated programmatically
- Test queries are stored in JSON files
- Performance baselines are tracked over time

## 📈 Continuous Testing

### Automated Testing
- GitHub Actions run tests on every push
- Performance benchmarks are tracked
- Regression testing prevents degradation

### Manual Testing Checklist
- [ ] API endpoints respond correctly
- [ ] Frontend loads and functions
- [ ] AI responses are relevant and accurate
- [ ] Performance meets benchmarks
- [ ] Error handling works properly

## 🐛 Debugging Failed Tests

### Common Issues
1. **API Connection Errors**: Check server status and network
2. **Performance Degradation**: Review memory usage and optimization
3. **AI Response Quality**: Validate knowledge base and models
4. **Frontend Issues**: Check build process and dependencies

### Debug Commands
```bash
# Verbose test output
python tests/test_api.py -v

# Debug mode
DEBUG=true python tests/test_reasoning.py

# Performance profiling
python -m cProfile tests/test_phi2_performance.py
```

## 📝 Adding New Tests

### Test File Template
```python
import unittest
import requests
import json

class TestNewFeature(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8000"
    
    def test_feature_functionality(self):
        # Test implementation
        pass
    
    def test_feature_edge_cases(self):
        # Edge case testing
        pass
    
    def test_feature_performance(self):
        # Performance validation
        pass

if __name__ == "__main__":
    unittest.main()
```

### Test Documentation Guidelines
- Document test purpose and scope
- Include setup and teardown instructions
- Explain expected outcomes
- Provide troubleshooting guidance

## 🎯 Quality Assurance

### Code Quality Checks
- PEP 8 compliance
- Type hint validation
- Security vulnerability scanning
- Dependency health checks

### Review Process
1. All tests must pass before merge
2. Performance benchmarks must be met
3. New features require new tests
4. Documentation must be updated

---

For questions about testing, see the main project documentation or create an issue.