# GCP Security Checklist for Radeon AI

## Current Security Gaps
- ❌ No authentication required (`--allow-unauthenticated`)
- ❌ No WAF (Web Application Firewall) protection
- ❌ No rate limiting
- ❌ No DDoS protection
- ❌ No geo-blocking
- ❌ No resource limits

## Recommended Security Measures

### 1. Authentication & Authorization
```bash
# Remove public access
--no-allow-unauthenticated

# Add specific user access
gcloud run services add-iam-policy-binding radeon-ai \
    --member="user:your-email@domain.com" \
    --role="roles/run.invoker"
```

### 2. Cloud Armor WAF
```bash
# Create security policy
gcloud compute security-policies create radeon-ai-waf

# Add rate limiting (100 req/min per IP)
gcloud compute security-policies rules create 1000 \
    --security-policy=radeon-ai-waf \
    --action=rate-based-ban \
    --rate-limit-threshold-count=100
```

### 3. Resource Limits
```bash
# Set CPU and memory limits
--cpu=2 --memory=4Gi --max-instances=10
```

### 4. Network Security
```bash
# Create VPC with private subnets
gcloud compute networks create radeon-ai-vpc --subnet-mode=custom

# Create firewall rules
gcloud compute firewall-rules create allow-radeon-ai \
    --network=radeon-ai-vpc \
    --allow=tcp:8000 \
    --source-ranges=10.0.0.0/8
```

### 5. Monitoring & Logging
```bash
# Enable audit logs
gcloud logging sinks create radeon-ai-audit \
    bigquery.googleapis.com/projects/PROJECT_ID/datasets/security_logs
```

## Implementation Priority

### High Priority (Immediate)
1. **Remove `--allow-unauthenticated`** - Prevents unauthorized access
2. **Add rate limiting** - Prevents abuse and DoS
3. **Set resource limits** - Prevents resource exhaustion

### Medium Priority (This Week)
1. **Implement Cloud Armor WAF** - Advanced threat protection
2. **Add monitoring** - Security event detection
3. **Configure proper IAM** - Principle of least privilege

### Low Priority (Future)
1. **VPC with private networking** - Network isolation
2. **Custom domain with SSL** - Professional deployment
3. **Multi-region deployment** - High availability

## Quick Fix Commands

```bash
# Immediate security improvement
gcloud run deploy radeon-ai \
    --source . \
    --no-allow-unauthenticated \
    --cpu=1 --memory=2Gi --max-instances=5

# Add your access
gcloud run services add-iam-policy-binding radeon-ai \
    --member="user:YOUR_EMAIL" \
    --role="roles/run.invoker"
```

## Cost Impact
- **Cloud Armor**: ~$1/month for basic policy
- **Resource limits**: Reduces potential overcharges
- **Authentication**: No additional cost
- **Monitoring**: ~$0.50/GB of logs

## Testing Security
```bash
# Test rate limiting
for i in {1..150}; do curl -s YOUR_SERVICE_URL; done

# Test authentication
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" YOUR_SERVICE_URL
```