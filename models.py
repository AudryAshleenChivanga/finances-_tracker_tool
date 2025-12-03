"""
Database Models for Finance Tracker
User authentication, profile management, and Chengeta Academy
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()


# Association table for course instructors (many-to-many)
course_instructors = db.Table('course_instructors',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    """User model for authentication and profile."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile information
    full_name = db.Column(db.String(120))
    profile_picture = db.Column(db.String(255))  # Store file path
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Customization settings
    theme = db.Column(db.String(20), default='light')
    currency = db.Column(db.String(10), default='USD')
    timezone = db.Column(db.String(50), default='UTC')
    
    # Preferences
    default_income_category = db.Column(db.String(50), default='Salary')
    default_expense_category = db.Column(db.String(50), default='Other')
    budget_alert_threshold = db.Column(db.Integer, default=80)  # Percentage
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Update the last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def get_data_file(self):
        """Get user-specific transactions file path."""
        return f'data/users/{self.id}/transactions.json'
    
    def get_budget_file(self):
        """Get user-specific budgets file path."""
        return f'data/users/{self.id}/budgets.json'
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    # Relationships for Academy
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic')
    taught_courses = db.relationship('Course', secondary=course_instructors, backref='instructors')


class Course(db.Model):
    """Course model for Chengeta Academy."""
    
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(300))
    
    # Pricing
    price = db.Column(db.Float, default=0.0)  # 0 = free
    original_price = db.Column(db.Float)  # For showing discounts
    currency = db.Column(db.String(10), default='USD')
    
    # Content
    thumbnail = db.Column(db.String(255))  # Image path
    preview_video = db.Column(db.String(255))  # Preview video URL
    
    # Metadata
    category = db.Column(db.String(50), default='general')  # budgeting, investing, debt, savings, mindset
    level = db.Column(db.String(20), default='beginner')  # beginner, intermediate, advanced
    duration_hours = db.Column(db.Float, default=0)  # Total course duration
    
    # Topics covered (stored as JSON)
    topics = db.Column(db.Text)  # JSON array of topics
    
    # What you'll learn (stored as JSON)
    learning_outcomes = db.Column(db.Text)  # JSON array
    
    # Requirements (stored as JSON)
    requirements = db.Column(db.Text)  # JSON array
    
    # Status
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # Statistics
    total_students = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    
    # Relationships
    lessons = db.relationship('Lesson', backref='course', lazy='dynamic', order_by='Lesson.order')
    enrollments = db.relationship('Enrollment', backref='course', lazy='dynamic')
    
    def get_topics(self):
        """Get topics as a list."""
        if self.topics:
            return json.loads(self.topics)
        return []
    
    def set_topics(self, topics_list):
        """Set topics from a list."""
        self.topics = json.dumps(topics_list)
    
    def get_learning_outcomes(self):
        """Get learning outcomes as a list."""
        if self.learning_outcomes:
            return json.loads(self.learning_outcomes)
        return []
    
    def set_learning_outcomes(self, outcomes_list):
        """Set learning outcomes from a list."""
        self.learning_outcomes = json.dumps(outcomes_list)
    
    def get_requirements(self):
        """Get requirements as a list."""
        if self.requirements:
            return json.loads(self.requirements)
        return []
    
    def set_requirements(self, req_list):
        """Set requirements from a list."""
        self.requirements = json.dumps(req_list)
    
    def get_total_lessons(self):
        """Get total number of lessons."""
        return self.lessons.count()
    
    def get_published_lessons(self):
        """Get published lessons."""
        return self.lessons.filter_by(is_published=True).all()
    
    def calculate_duration(self):
        """Calculate total duration from lessons."""
        total_minutes = sum(lesson.duration_minutes or 0 for lesson in self.lessons)
        self.duration_hours = round(total_minutes / 60, 1)
        return self.duration_hours
    
    def __repr__(self):
        return f'<Course {self.title}>'


class Lesson(db.Model):
    """Lesson model for course content."""
    
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Content type
    content_type = db.Column(db.String(20), default='video')  # video, text, quiz, assignment
    
    # Video content
    video_url = db.Column(db.String(500))  # YouTube, Vimeo, or hosted URL
    video_provider = db.Column(db.String(20))  # youtube, vimeo, hosted
    
    # Text content
    text_content = db.Column(db.Text)  # Markdown or HTML
    
    # Resources/attachments (JSON array of file paths)
    resources = db.Column(db.Text)
    
    # Metadata
    order = db.Column(db.Integer, default=0)  # Lesson order in course
    duration_minutes = db.Column(db.Integer, default=0)
    is_free_preview = db.Column(db.Boolean, default=False)  # Can be viewed without enrollment
    is_published = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    progress = db.relationship('LessonProgress', backref='lesson', lazy='dynamic')
    
    def get_resources(self):
        """Get resources as a list."""
        if self.resources:
            return json.loads(self.resources)
        return []
    
    def set_resources(self, resources_list):
        """Set resources from a list."""
        self.resources = json.dumps(resources_list)
    
    def get_video_embed_url(self):
        """Get embeddable video URL."""
        if not self.video_url:
            return None
        
        if self.video_provider == 'youtube':
            # Extract video ID and return embed URL
            if 'youtube.com/watch?v=' in self.video_url:
                video_id = self.video_url.split('watch?v=')[1].split('&')[0]
            elif 'youtu.be/' in self.video_url:
                video_id = self.video_url.split('youtu.be/')[1].split('?')[0]
            else:
                video_id = self.video_url
            return f'https://www.youtube.com/embed/{video_id}'
        
        elif self.video_provider == 'vimeo':
            if 'vimeo.com/' in self.video_url:
                video_id = self.video_url.split('vimeo.com/')[1].split('?')[0]
            else:
                video_id = self.video_url
            return f'https://player.vimeo.com/video/{video_id}'
        
        return self.video_url
    
    def __repr__(self):
        return f'<Lesson {self.title}>'


class Enrollment(db.Model):
    """Enrollment model for tracking student course access."""
    
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    # Payment info
    amount_paid = db.Column(db.Float, default=0.0)
    payment_method = db.Column(db.String(50))  # stripe, paypal, paynow, free
    payment_status = db.Column(db.String(20), default='completed')  # pending, completed, refunded
    transaction_id = db.Column(db.String(100))
    
    # Progress
    progress_percent = db.Column(db.Float, default=0.0)
    lessons_completed = db.Column(db.Integer, default=0)
    last_lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    
    # Status
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    certificate_issued = db.Column(db.Boolean, default=False)
    certificate_id = db.Column(db.String(50))
    
    # Timestamps
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    last_lesson = db.relationship('Lesson', foreign_keys=[last_lesson_id])
    lesson_progress = db.relationship('LessonProgress', backref='enrollment', lazy='dynamic')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='unique_enrollment'),)
    
    def update_progress(self):
        """Update progress based on completed lessons."""
        total_lessons = self.course.get_total_lessons()
        if total_lessons > 0:
            completed = self.lesson_progress.filter_by(is_completed=True).count()
            self.lessons_completed = completed
            self.progress_percent = round((completed / total_lessons) * 100, 1)
            
            if self.progress_percent >= 100:
                self.is_completed = True
                self.completed_at = datetime.utcnow()
        
        self.last_accessed = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<Enrollment User:{self.user_id} Course:{self.course_id}>'


class LessonProgress(db.Model):
    """Track individual lesson completion for students."""
    
    __tablename__ = 'lesson_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    
    # Progress
    is_completed = db.Column(db.Boolean, default=False)
    watch_time_seconds = db.Column(db.Integer, default=0)  # For video lessons
    
    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('enrollment_id', 'lesson_id', name='unique_lesson_progress'),)
    
    def mark_complete(self):
        """Mark lesson as completed."""
        self.is_completed = True
        self.completed_at = datetime.utcnow()
        db.session.commit()
        
        # Update enrollment progress
        self.enrollment.update_progress()
    
    def __repr__(self):
        return f'<LessonProgress Enrollment:{self.enrollment_id} Lesson:{self.lesson_id}>'


class Quiz(db.Model):
    """Quiz model for lesson assessments."""
    
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Settings
    passing_score = db.Column(db.Integer, default=70)  # Percentage needed to pass
    time_limit_minutes = db.Column(db.Integer)  # None = no limit
    max_attempts = db.Column(db.Integer, default=3)  # 0 = unlimited
    shuffle_questions = db.Column(db.Boolean, default=True)
    show_correct_answers = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('QuizQuestion', backref='quiz', lazy='dynamic', order_by='QuizQuestion.order')
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy='dynamic')
    lesson = db.relationship('Lesson', backref='quizzes')
    
    def get_total_questions(self):
        return self.questions.count()
    
    def __repr__(self):
        return f'<Quiz {self.title}>'


class QuizQuestion(db.Model):
    """Quiz question model."""
    
    __tablename__ = 'quiz_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default='multiple_choice')  # multiple_choice, true_false, short_answer
    
    # Options stored as JSON: [{"text": "Option A", "is_correct": true}, ...]
    options = db.Column(db.Text)
    
    # For short answer questions
    correct_answer = db.Column(db.Text)
    
    # Explanation shown after answering
    explanation = db.Column(db.Text)
    
    # Points for this question
    points = db.Column(db.Integer, default=1)
    
    order = db.Column(db.Integer, default=0)
    
    def get_options(self):
        if self.options:
            return json.loads(self.options)
        return []
    
    def set_options(self, options_list):
        self.options = json.dumps(options_list)
    
    def check_answer(self, answer):
        """Check if the given answer is correct."""
        if self.question_type == 'multiple_choice':
            options = self.get_options()
            for i, opt in enumerate(options):
                if opt.get('is_correct') and str(i) == str(answer):
                    return True
            return False
        elif self.question_type == 'true_false':
            options = self.get_options()
            for i, opt in enumerate(options):
                if opt.get('is_correct') and str(i) == str(answer):
                    return True
            return False
        elif self.question_type == 'short_answer':
            # Case-insensitive comparison
            return self.correct_answer.lower().strip() == str(answer).lower().strip()
        return False
    
    def __repr__(self):
        return f'<QuizQuestion {self.id}>'


class QuizAttempt(db.Model):
    """Track student quiz attempts."""
    
    __tablename__ = 'quiz_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)
    
    # Results
    score = db.Column(db.Float, default=0)  # Percentage
    points_earned = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)
    passed = db.Column(db.Boolean, default=False)
    
    # Answers stored as JSON: {"question_id": "answer", ...}
    answers = db.Column(db.Text)
    
    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    time_taken_seconds = db.Column(db.Integer)
    
    # Relationships
    user = db.relationship('User', backref='quiz_attempts')
    enrollment = db.relationship('Enrollment', backref='quiz_attempts')
    
    def get_answers(self):
        if self.answers:
            return json.loads(self.answers)
        return {}
    
    def set_answers(self, answers_dict):
        self.answers = json.dumps(answers_dict)
    
    def calculate_score(self):
        """Calculate and save the score."""
        answers = self.get_answers()
        total_points = 0
        earned_points = 0
        
        for question in self.quiz.questions:
            total_points += question.points
            answer = answers.get(str(question.id))
            if answer is not None and question.check_answer(answer):
                earned_points += question.points
        
        self.total_points = total_points
        self.points_earned = earned_points
        self.score = round((earned_points / total_points * 100) if total_points > 0 else 0, 1)
        self.passed = self.score >= self.quiz.passing_score
        self.completed_at = datetime.utcnow()
        
        if self.started_at:
            self.time_taken_seconds = int((self.completed_at - self.started_at).total_seconds())
        
        db.session.commit()
        return self.score
    
    def __repr__(self):
        return f'<QuizAttempt User:{self.user_id} Quiz:{self.quiz_id}>'

