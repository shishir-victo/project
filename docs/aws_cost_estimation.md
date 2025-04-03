# AWS Cost Estimation Guide

This document provides an estimation of AWS service costs for the Student Attendance System, focusing on free tier usage and cost optimization strategies.

## AWS Free Tier Resources

The following AWS resources are available in the free tier (as of April 2025):

| Service | Free Tier Allocation | Duration |
|---------|----------------------|----------|
| EC2 (t2.micro) | 750 hours per month | 12 months |
| RDS (db.t2.micro) | 750 hours per month | 12 months |
| S3 | 5GB storage, 20,000 GET, 2,000 PUT | 12 months |
| Lambda | 1M free requests, 400,000 GB-seconds | Unlimited |
| API Gateway | 1M API calls | 12 months |
| CloudFront | 50GB data transfer, 2M HTTP/HTTPS requests | 12 months |
| Elastic Beanstalk | No additional charge (pay for resources) | - |

## Estimated Monthly Costs

### Base Deployment (Free Tier)

| Service | Usage Pattern | Estimated Monthly Cost |
|---------|---------------|------------------------|
| Elastic Beanstalk (t2.micro) | 24/7 operation | $0 (free tier) |
| RDS PostgreSQL (db.t2.micro) | 20GB storage | $0 (free tier) |
| S3 | 2GB storage, 10,000 GET, 1,000 PUT | $0 (free tier) |
| Route 53 | 1 hosted zone | $0.50 |
| **Total** | | **$0.50** |

### Base Deployment (Post-Free Tier)

| Service | Usage Pattern | Estimated Monthly Cost |
|---------|---------------|------------------------|
| Elastic Beanstalk (t2.micro) | 24/7 operation | $8.50 |
| RDS PostgreSQL (db.t2.micro) | 20GB storage | $13.00 |
| S3 | 2GB storage, 10,000 GET, 1,000 PUT | $0.05 |
| Route 53 | 1 hosted zone | $0.50 |
| **Total** | | **$22.05** |

### Enhanced Deployment with Lambda

| Service | Usage Pattern | Estimated Monthly Cost |
|---------|---------------|------------------------|
| Elastic Beanstalk (t2.micro) | 24/7 operation | $0/$8.50 (free tier/paid) |
| RDS PostgreSQL (db.t2.micro) | 20GB storage | $0/$13.00 (free tier/paid) |
| S3 | 5GB storage, 15,000 GET, 1,500 PUT | $0/$0.12 (free tier/paid) |
| Lambda | 100,000 invocations/month, 1GB memory, 500ms avg execution | $0 (free tier) |
| API Gateway | 100,000 API calls | $0 (free tier)/$0.35 (paid) |
| Route 53 | 1 hosted zone | $0.50 |
| **Total (free tier)** | | **$0.50** |
| **Total (post-free tier)** | | **$22.47** |

## Cost Optimization Strategies

### General Strategies

1. **Right-sizing resources**:
   - Start with t2.micro instances during development
   - Scale only when necessary based on actual usage

2. **Use spot instances for development**:
   - Up to 90% cost savings for non-production environments
   - Example: t2.micro spot instance ~$3/month vs $8.50 for on-demand

3. **Schedule non-production environments**:
   - Run development/staging only during business hours (8 hours/day, 5 days/week)
   - Potential savings: ~70% on EC2 and RDS costs

### S3 Optimization

1. **Lifecycle policies**:
   - Transition infrequently accessed data to lower-cost storage classes
   - Example configuration:
     ```
     Classroom photos older than 30 days → S3 Standard-IA
     Classroom photos older than 90 days → S3 Glacier
     ```

2. **Image optimization**:
   - Resize images before uploading
   - Use appropriate compression
   - Potential storage reduction: 40-60%

### RDS Optimization

1. **Storage optimization**:
   - Use efficient data types
   - Implement data archiving for old records
   - Set up automated backups with appropriate retention periods

2. **Performance tuning**:
   - Optimize queries to reduce CPU usage
   - Use connection pooling to reduce overhead

### Lambda Optimization

1. **Execution optimization**:
   - Tune memory allocation for cost/performance balance
   - Optimize code to reduce execution time
   - Reuse connections and resources between invocations

2. **Throttling and quotas**:
   - Implement rate limiting for Lambda functions
   - Set up CloudWatch alarms for unusual invocation patterns

## School-Specific Deployment Scenarios

### Small School (200 students, 10 classes)

| Metric | Value |
|--------|-------|
| Student photos | 200 × 100KB = 20MB |
| Classroom photos | 10 classes × 2 sessions/day × 20 days/month × 500KB = 200MB |
| Database size | ~50MB initial, growing at ~10MB/month |
| Face recognition operations | 200 students + 400 attendance sessions = ~600/month |

**Estimated monthly cost**: $0.50 (free tier) / $22.05 (post-free tier)

### Medium School (1,000 students, 40 classes)

| Metric | Value |
|--------|-------|
| Student photos | 1,000 × 100KB = 100MB |
| Classroom photos | 40 classes × 2 sessions/day × 20 days/month × 500KB = 800MB |
| Database size | ~200MB initial, growing at ~50MB/month |
| Face recognition operations | 1,000 students + 1,600 attendance sessions = ~2,600/month |

**Estimated monthly cost**: $0.50 (free tier) / $22.05 (post-free tier)

### Large School (5,000 students, 200 classes)

| Metric | Value |
|--------|-------|
| Student photos | 5,000 × 100KB = 500MB |
| Classroom photos | 200 classes × 2 sessions/day × 20 days/month × 500KB = 4GB |
| Database size | ~1GB initial, growing at ~200MB/month |
| Face recognition operations | 5,000 students + 8,000 attendance sessions = ~13,000/month |

**Recommended configuration**:
- t3.small instance ($17/month) instead of t2.micro
- RDS with 50GB storage ($20/month)
- Lambda for face recognition processing

**Estimated monthly cost**: $40-50/month

## Long-Term Cost Planning

### Year 1 (Free Tier Period)

| Quarter | Estimated Cost | Notes |
|---------|----------------|-------|
| Q1 | $1.50 | Route 53 only, all else in free tier |
| Q2 | $1.50 | Route 53 only, all else in free tier |
| Q3 | $1.50 | Route 53 only, all else in free tier |
| Q4 | $1.50 | Route 53 only, all else in free tier |
| **Total Year 1** | **$6.00** | |

### Year 2+ (Post-Free Tier)

| Service | Annual Cost |
|---------|-------------|
| EC2/Elastic Beanstalk | $102.00 |
| RDS PostgreSQL | $156.00 |
| S3 (basic usage) | $0.60 |
| Route 53 | $6.00 |
| **Total Annual Cost** | **$264.60** |

## AWS Budgeting and Alerting

1. **Set up AWS Budget**:
   ```
   AWS Console → Billing → Budgets → Create budget
   Type: Cost budget
   Period: Monthly
   Start month: Current month
   Budget amount: $30
   ```

2. **Configure alerts**:
   ```
   Threshold: 80%
   Alert recipients: your-email@example.com
   ```

3. **Set up CloudWatch alarms**:
   - EC2 CPU utilization > 80% for 1 hour
   - RDS database connections > 80% of maximum
   - Lambda errors > 5% of invocations
   - S3 storage growing > 20% month-over-month

## Conclusion

The Student Attendance System can be deployed cost-effectively using AWS free tier services in the first year, with reasonable ongoing costs thereafter. For schools with larger deployments, optimizations can be made to keep costs manageable while maintaining performance and reliability.

**Recommendation**: Start with the base deployment on free tier services, monitor actual usage patterns for 2-3 months, then optimize based on real-world data before committing to a long-term infrastructure plan.