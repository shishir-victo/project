from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='teacher')  # teacher or admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with classes
    classes = db.relationship('Class', backref='teacher', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    students = db.relationship('Student', backref='class_obj', lazy=True)
    attendance_sessions = db.relationship('AttendanceSession', backref='class_obj', lazy=True)
    
    def __repr__(self):
        return f'<Class {self.name}>'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    face_encoding = db.Column(db.Text)  # JSON string of face encoding
    face_image_path = db.Column(db.String(255))  # Path/URL to student's face image in S3
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    attendance_records = db.relationship('AttendanceRecord', backref='student', lazy=True)
    
    def __repr__(self):
        return f'<Student {self.name} ({self.student_id})>'


class AttendanceSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    session_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    start_time = db.Column(db.Time, nullable=False, default=datetime.utcnow().time)
    end_time = db.Column(db.Time)
    image_path = db.Column(db.String(255))  # Path/URL to classroom image in S3
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    attendance_records = db.relationship('AttendanceRecord', backref='session', lazy=True)
    
    def __repr__(self):
        return f'<AttendanceSession {self.id} for {self.class_obj.name} on {self.session_date}>'


class AttendanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('attendance_session.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    status = db.Column(db.String(20), default='present')  # present, absent, late
    confidence = db.Column(db.Float)  # Face recognition confidence score
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AttendanceRecord {self.student.name} - {self.status}>'
