# AWS Deployment Guide

This guide provides step-by-step instructions for deploying the Student Attendance System to AWS services, optimized for the free tier while maintaining performance and security.

## Prerequisites

- AWS account with administrative access
- AWS CLI installed and configured
- Git repository of the Student Attendance System
- Python 3.8+
- PostgreSQL client (for database migrations)

## Deployment Architecture

The deployment architecture consists of:

- **AWS Elastic Beanstalk**: Hosts the Flask web application
- **Amazon RDS**: PostgreSQL database for application data
- **Amazon S3**: Storage for student and classroom photos
- **AWS Lambda** (optional): For face recognition processing
- **Amazon CloudWatch**: For monitoring and logging
- **Amazon Route 53** (optional): For DNS management

## Step 1: Prepare the Application for Deployment

1. **Configure the environment variables**:

   Create a `.env.production` file (do not commit to Git):
   ```
   DATABASE_URL=postgresql://username:password@your-rds-instance.region.rds.amazonaws.com:5432/dbname
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   AWS_REGION=us-east-1
   S3_BUCKET=your-bucket-name
   FLASK_ENV=production
   SECRET_KEY=your-secure-random-string
   ```

2. **Update application configuration**:

   In `config.py` or equivalent:
   ```python
   # Production configuration
   class ProductionConfig(Config):
       DEBUG = False
       TESTING = False
       SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
       # Add other production-specific settings
   ```

3. **Create Elastic Beanstalk configuration**:

   Create a folder `.ebextensions` with file `01_flask.config`:
   ```yaml
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: main:app
     aws:elasticbeanstalk:application:environment:
       FLASK_ENV: production
   ```

4. **Create Procfile**:

   ```
   web: gunicorn --bind 0.0.0.0:5000 --workers 3 main:app
   ```

5. **Create requirements.txt**:

   Ensure all dependencies are listed with specific versions.

## Step 2: Set Up Amazon RDS Database

1. **Create PostgreSQL database**:

   - Navigate to RDS Console
   - Click "Create database"
   - Choose "Standard create"
   - Engine type: PostgreSQL
   - Templates: Free tier
   - DB instance identifier: `student-attendance-db`
   - Master username: Choose a secure username
   - Master password: Generate a strong password
   - DB instance class: `db.t2.micro` (Free tier eligible)
   - Storage: 20 GB (minimum)
   - VPC: Default VPC
   - Public access: No (for security)
   - Create new security group: `rds-postgres-sg`
   - Initial database name: `attendance_system`
   - Click "Create database"

2. **Configure security group**:

   - Go to EC2 > Security Groups
   - Select the newly created RDS security group
   - Add inbound rule:
     - Type: PostgreSQL
     - Source: `[Your Elastic Beanstalk Security Group ID]` (add this later)
     - Description: "Allow connections from Elastic Beanstalk"

3. **Note database connection details**:

   - Endpoint URL
   - Port (default: 5432)
   - Initial database name
   - Master username and password

## Step 3: Create S3 Bucket for Image Storage

1. **Create bucket**:

   - Go to S3 Console
   - Click "Create bucket"
   - Name: `student-attendance-images-[unique-suffix]`
   - Region: Same as your application
   - Block all public access: Enabled
   - Bucket versioning: Disabled (to minimize costs)
   - Default encryption: Enabled (SSE-S3)
   - Click "Create bucket"

2. **Create folder structure**:

   - `student_photos/`
   - `classroom_photos/`
   - `temp/`

3. **Configure CORS** (if needed for direct uploads):

   - Select your bucket
   - Go to "Permissions" tab
   - Edit CORS configuration:
   ```json
   [
     {
       "AllowedHeaders": ["*"],
       "AllowedMethods": ["PUT", "POST", "GET"],
       "AllowedOrigins": ["https://your-eb-domain.elasticbeanstalk.com"],
       "ExposeHeaders": []
     }
   ]
   ```

## Step 4: Create IAM User for Application

1. **Create policy**:

   - Go to IAM Console
   - Click "Policies" > "Create policy"
   - Use JSON editor:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "s3:PutObject",
           "s3:GetObject",
           "s3:DeleteObject",
           "s3:ListBucket"
         ],
         "Resource": [
           "arn:aws:s3:::student-attendance-images-[unique-suffix]",
           "arn:aws:s3:::student-attendance-images-[unique-suffix]/*"
         ]
       }
     ]
   }
   ```
   - Name: `student-attendance-s3-access`
   - Click "Create policy"

2. **Create user**:

   - Go to IAM Console > Users
   - Click "Add users"
   - Username: `student-attendance-app`
   - Access type: Programmatic access
   - Attach policy: `student-attendance-s3-access`
   - Tags: Add name and environment tags
   - Create user and save credentials securely

## Step 5: Deploy to Elastic Beanstalk

1. **Initialize Elastic Beanstalk**:

   ```bash
   pip install awsebcli
   cd /path/to/student-attendance-system
   eb init
   
   # Select region
   # Create new application
   # Select Python platform
   # Select Python 3.8
   # Set up SSH (optional)
   ```

2. **Create environment**:

   ```bash
   eb create student-attendance-prod
   
   # Choose load balancer type: application
   # Choose default instance profile
   ```

3. **Configure environment variables**:

   - Go to Elastic Beanstalk Console
   - Select your environment
   - Go to Configuration > Software
   - Add environment properties:
     - DATABASE_URL=postgresql://username:password@your-rds-instance.region.rds.amazonaws.com:5432/dbname
     - AWS_ACCESS_KEY_ID=your-access-key
     - AWS_SECRET_ACCESS_KEY=your-secret-key
     - AWS_REGION=us-east-1
     - S3_BUCKET=student-attendance-images-[unique-suffix]
     - SECRET_KEY=your-secure-random-string
   - Apply changes

4. **Update security group for RDS**:

   - Find the security group ID of your Elastic Beanstalk environment
   - Update the RDS security group to allow access from the EB security group

5. **Deploy the application**:

   ```bash
   eb deploy
   ```

6. **Run database migrations**:

   - Connect to the Elastic Beanstalk instance:
   ```bash
   eb ssh
   ```
   
   - Run the migration commands:
   ```bash
   cd /var/app/current
   source /var/app/venv/staging-LQM1lest/bin/activate
   python -c "from app import db; db.create_all()"
   ```

7. **Verify deployment**:

   ```bash
   eb open
   ```

## Step 6: Set Up Monitoring and Logging

1. **Configure CloudWatch Alarms**:

   - Go to CloudWatch Console
   - Click "Alarms" > "Create alarm"
   - Select metric:
     - EC2 > By Auto Scaling Group
     - Select your EB environment's Auto Scaling Group
     - Select "CPUUtilization"
   - Set threshold:
     - Greater than 80% for 5 minutes
   - Add notification:
     - Create new SNS topic
     - Add your email
   - Name: "HighCPUUtilization-StudentAttendance"
   - Create alarm

2. **Configure Log Monitoring**:

   - Go to Elastic Beanstalk Console
   - Select your environment
   - Go to Monitoring
   - Set up additional monitoring metrics as needed

## Step 7: Set Up HTTPS (Optional)

1. **Request SSL Certificate**:

   - Go to AWS Certificate Manager
   - Click "Request certificate"
   - Choose "Request a public certificate"
   - Add domain names:
     - yourdomain.com
     - www.yourdomain.com
   - Choose DNS validation
   - Complete validation by adding DNS records

2. **Configure HTTPS listener**:

   - Go to EC2 Console > Load Balancers
   - Select your EB load balancer
   - Add listener:
     - Protocol: HTTPS
     - Port: 443
     - Certificate: Select your ACM certificate
     - Security policy: ELBSecurityPolicy-TLS-1-2-2017-01
   - Click "Add"

3. **Configure redirection**:

   - Edit HTTP:80 listener
   - Add rule to redirect to HTTPS:443

## Step 8: Set Up Custom Domain (Optional)

1. **Create DNS record**:

   If using Route 53:
   - Go to Route 53 Console
   - Select your hosted zone
   - Click "Create record"
   - Name: www
   - Type: A - IPv4 address
   - Alias: Yes
   - Target: Your Elastic Beanstalk environment
   - Routing policy: Simple
   - Click "Create records"

   If using another DNS provider:
   - Create a CNAME record pointing to your EB domain

2. **Update application configuration**:

   - Update CORS settings in S3 to include your custom domain
   - Update any hardcoded URLs in your application

## Step 9: Set Up Backup and Disaster Recovery

1. **Configure RDS backups**:

   - Go to RDS Console
   - Select your database
   - Click "Modify"
   - Backup section:
     - Backup retention period: 7 days
     - Backup window: Select a time with low traffic
   - Click "Continue" and "Apply immediately"

2. **Configure S3 versioning** (if needed):

   - Go to S3 Console
   - Select your bucket
   - Go to "Properties" tab
   - Enable versioning

## Step 10: Final Checklist and Verification

1. **Security checks**:

   - Verify all security groups have minimal necessary access
   - Ensure no public access to RDS
   - Check IAM permissions follow least privilege principle
   - Verify SSL/TLS configuration

2. **Functionality tests**:

   - Test user registration and login
   - Test student registration with photo upload
   - Test attendance taking with classroom photos
   - Test report generation

3. **Performance checks**:

   - Monitor application response times
   - Check database query performance
   - Verify face recognition processing speed

4. **Documentation**:

   - Update deployment documentation with actual values
   - Create operations runbook for maintenance tasks
   - Document backup and restore procedures

## Maintenance Procedures

### Deploying Updates

```bash
# Make changes to your code
git add .
git commit -m "Description of changes"

# Deploy to Elastic Beanstalk
eb deploy
```

### Database Migrations

For schema changes:

```bash
# Connect to the instance
eb ssh

# Navigate to application directory
cd /var/app/current
source /var/app/venv/*/bin/activate

# Run migration commands (example with Flask-Migrate)
python -c "from app import db; db.create_all()"
```

### Scaling

To scale the application:

1. Go to Elastic Beanstalk Console
2. Select your environment
3. Go to Configuration > Capacity
4. Modify auto scaling settings:
   - Min instances: 1
   - Max instances: 2 (or as needed)
   - Scale up trigger: CPUUtilization > 70% for 5 minutes
   - Scale down trigger: CPUUtilization < 30% for 5 minutes

### Monitoring

Regular monitoring tasks:

1. Check CloudWatch metrics daily
2. Review application logs weekly
3. Test backup restoration quarterly
4. Review security configurations monthly

## Troubleshooting

### Common Issues

1. **Database connection failures**:
   - Verify security group rules
   - Check database credentials in environment variables
   - Test connection from EB instance using psql

2. **S3 access issues**:
   - Verify IAM permissions
   - Check environment variables for AWS credentials
   - Test S3 access from EB instance using AWS CLI

3. **Application errors**:
   - Check EB logs: `eb logs`
   - SSH into instance for detailed investigation: `eb ssh`
   - Review CloudWatch logs for application errors

4. **Performance issues**:
   - Check instance CPU and memory utilization
   - Review database performance metrics
   - Check for slow API calls to AWS services

## Cost Optimization

1. **Right-size instances**:
   - Start with t2.micro (free tier)
   - Monitor CPU and memory utilization
   - Adjust only if consistently high utilization

2. **Database optimization**:
   - Use appropriate storage type
   - Implement data lifecycle policies
   - Consider read replicas only if needed

3. **S3 cost reduction**:
   - Implement lifecycle policies for older objects
   - Consider compression for larger images
   - Use appropriate storage classes

Refer to the [AWS Cost Estimation Guide](aws_cost_estimation.md) for detailed cost analysis.