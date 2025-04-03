# AWS Deployment Documentation

This folder contains comprehensive guides for deploying the Student Attendance System to AWS services, making use of the AWS free tier offerings while ensuring optimal performance and security.

## Documentation Overview

### [AWS Deployment Guide](aws_deployment_guide.md)
The primary guide for deploying the complete application to AWS, covering:
- Setting up AWS account and IAM users
- Creating and configuring S3 buckets
- Setting up RDS PostgreSQL database
- Deploying the application to Elastic Beanstalk
- Configuring environment variables
- Setting up custom domains and HTTPS
- Monitoring and maintenance

### [Face Recognition Lambda Guide](face_recognition_lambda_guide.md)
A specialized guide for offloading face recognition tasks to AWS Lambda:
- Building Lambda functions for face recognition
- Creating and configuring Lambda layers
- Setting up API Gateway
- Integrating Lambda functions with the main application
- Monitoring and optimizing Lambda performance
- Managing costs for serverless components

### [S3 and Face Recognition Setup](s3_face_recognition_setup.md)
Detailed technical guide focused on:
- Configuring S3 buckets optimally for image storage
- Setting up folder structures and lifecycle policies
- Implementing and tuning face recognition
- Security best practices for facial data
- Testing and validating the integration

## Getting Started

Start with the [AWS Deployment Guide](aws_deployment_guide.md) for a complete overview. If your application requires high-performance face recognition capabilities, also review the [Face Recognition Lambda Guide](face_recognition_lambda_guide.md).

## Cost Considerations

The guides emphasize AWS free tier usage, but be aware of these cost factors:
- S3 storage beyond free tier limits
- RDS database instance uptime and storage
- Lambda invocations beyond free tier
- Data transfer between AWS services

Set up AWS Budgets and Billing Alarms to monitor usage and prevent unexpected charges.

## Security Notes

When deploying to AWS:
- Use IAM roles with principle of least privilege
- Keep your AWS credentials secure
- Encrypt sensitive data at rest and in transit
- Regularly rotate access keys
- Enable CloudTrail for auditing
- Follow all recommendations for securing facial recognition data

## Support and Maintenance

After deployment:
- Monitor CloudWatch logs regularly
- Set up alarms for critical metrics
- Keep dependencies updated
- Perform regular backups
- Test disaster recovery procedures

## Compliance Considerations

Facial recognition data may be subject to various regulations. Consider:
- GDPR (EU)
- CCPA (California)
- BIPA (Illinois)
- Industry-specific regulations
- School district or institutional policies

Consult legal expertise to ensure compliance with applicable regulations.