# SGIS: Student Attendance System with Facial Recognition

A web-based student attendance system using facial recognition, designed for deployment on AWS.

## Overview

SGIS is a comprehensive solution for automating student attendance in educational institutions using facial recognition technology. The system allows teachers to:

1. Register students with their facial images
2. Take attendance by uploading classroom photos
3. Generate attendance reports
4. Manage classes and student records

## Features

- **User Authentication**: Secure login and registration for teachers and administrators
- **Student Registration**: Easy registration of students with facial images
- **Facial Recognition**: Automatic identification of students in classroom photos
- **Attendance Tracking**: Recording and management of attendance data
- **Reporting**: Comprehensive attendance reports and analytics
- **AWS Integration**: Serverless deployment using AWS services

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Cloud Services**: AWS (S3, Lambda, RDS)
- **Facial Recognition**: Custom implementation (mock version for development)

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sgis.git
   cd sgis
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export DATABASE_URL="postgresql://username:password@localhost/sgis_db"
   export SESSION_SECRET="your-secure-session-key"
   ```

4. Initialize the database:
   ```bash
   python -c "from app import db; db.create_all()"
   ```

5. Run the application:
   ```bash
   python main.py
   ```

6. Access the application at `http://localhost:5000`

## AWS Deployment

This application is designed to be deployed on AWS. For detailed deployment instructions, refer to the following documents:

- [AWS Deployment Guide](docs/aws_deployment_guide.md)
- [Face Recognition Lambda Guide](docs/face_recognition_lambda_guide.md)
- [S3 Face Recognition Setup](docs/s3_face_recognition_setup.md)
- [AWS Cost Estimation](docs/aws_cost_estimation.md)

## Project Structure

```
├── app.py                   # Flask application instance and database initialization
├── main.py                  # Application entry point
├── models.py                # Database models (User, Class, Student, Attendance)
├── routes.py                # Application routes and view functions
├── aws_service.py           # AWS integration services (S3, Lambda)
├── face_recognition_service.py  # Facial recognition functionality
├── utils.py                 # Utility functions
├── static/                  # Static files (CSS, JS, images)
├── templates/               # HTML templates
└── docs/                    # Documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

Powered by SGIS (Student Guidance and Information System)
© 2025 All Rights Reserved