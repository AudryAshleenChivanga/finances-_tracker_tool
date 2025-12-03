"""
Chengeta Academy - Course Management System
Routes for course browsing, enrollment, and learning
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Course, Lesson, Enrollment, LessonProgress, Quiz, QuizQuestion, QuizAttempt
from datetime import datetime
import uuid

academy_bp = Blueprint('academy', __name__, url_prefix='/academy')


# ==================== PUBLIC ROUTES ====================

@academy_bp.route('/')
def courses():
    """Academy home - browse all courses."""
    # Get filter parameters
    category = request.args.get('category', 'all')
    level = request.args.get('level', 'all')
    sort = request.args.get('sort', 'popular')
    
    # Base query - only published courses
    query = Course.query.filter_by(is_published=True)
    
    # Apply filters
    if category != 'all':
        query = query.filter_by(category=category)
    if level != 'all':
        query = query.filter_by(level=level)
    
    # Apply sorting
    if sort == 'popular':
        query = query.order_by(Course.total_students.desc())
    elif sort == 'newest':
        query = query.order_by(Course.published_at.desc())
    elif sort == 'rating':
        query = query.order_by(Course.average_rating.desc())
    elif sort == 'price_low':
        query = query.order_by(Course.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Course.price.desc())
    
    courses = query.all()
    featured_courses = Course.query.filter_by(is_published=True, is_featured=True).limit(3).all()
    
    return render_template('academy/courses.html',
                         courses=courses,
                         featured_courses=featured_courses,
                         current_category=category,
                         current_level=level,
                         current_sort=sort)


@academy_bp.route('/course/<slug>')
def course_detail(slug):
    """View course details and curriculum."""
    course = Course.query.filter_by(slug=slug, is_published=True).first_or_404()
    
    # Check if user is enrolled
    enrollment = None
    if current_user.is_authenticated:
        enrollment = Enrollment.query.filter_by(
            user_id=current_user.id,
            course_id=course.id
        ).first()
    
    # Get lessons grouped by sections (for now, just ordered)
    lessons = course.get_published_lessons()
    
    return render_template('academy/course_detail.html',
                         course=course,
                         lessons=lessons,
                         enrollment=enrollment)


# ==================== ENROLLMENT ====================

@academy_bp.route('/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll(course_id):
    """Enroll in a course."""
    course = Course.query.get_or_404(course_id)
    
    # Check if already enrolled
    existing = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()
    
    if existing:
        flash('You are already enrolled in this course.', 'info')
        return redirect(url_for('academy.course_detail', slug=course.slug))
    
    # For free courses, enroll directly
    if course.price == 0:
        enrollment = Enrollment(
            user_id=current_user.id,
            course_id=course_id,
            amount_paid=0,
            payment_method='free',
            payment_status='completed'
        )
        db.session.add(enrollment)
        
        # Update course stats
        course.total_students += 1
        
        db.session.commit()
        
        flash(f'Successfully enrolled in "{course.title}"!', 'success')
        return redirect(url_for('academy.learn', slug=course.slug))
    
    # For paid courses, redirect to payment
    return redirect(url_for('academy.checkout', course_id=course_id))


@academy_bp.route('/checkout/<int:course_id>')
@login_required
def checkout(course_id):
    """Checkout page for paid courses."""
    course = Course.query.get_or_404(course_id)
    
    # Check if already enrolled
    existing = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()
    
    if existing:
        return redirect(url_for('academy.learn', slug=course.slug))
    
    return render_template('academy/checkout.html', course=course)


# ==================== LEARNING ====================

@academy_bp.route('/learn/<slug>')
@login_required
def learn(slug):
    """Course learning page - watch lessons."""
    course = Course.query.filter_by(slug=slug).first_or_404()
    
    # Check enrollment
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course.id
    ).first()
    
    if not enrollment:
        flash('Please enroll in this course first.', 'warning')
        return redirect(url_for('academy.course_detail', slug=slug))
    
    # Get current lesson (last accessed or first)
    lesson_id = request.args.get('lesson')
    if lesson_id:
        current_lesson = Lesson.query.get_or_404(lesson_id)
    elif enrollment.last_lesson_id:
        current_lesson = Lesson.query.get(enrollment.last_lesson_id)
    else:
        current_lesson = course.lessons.filter_by(is_published=True).first()
    
    # Get all lessons
    lessons = course.get_published_lessons()
    
    # Get progress for each lesson
    progress_map = {}
    for lp in enrollment.lesson_progress:
        progress_map[lp.lesson_id] = lp
    
    # Update last accessed
    enrollment.last_accessed = datetime.utcnow()
    if current_lesson:
        enrollment.last_lesson_id = current_lesson.id
    db.session.commit()
    
    return render_template('academy/learn.html',
                         course=course,
                         lessons=lessons,
                         current_lesson=current_lesson,
                         enrollment=enrollment,
                         progress_map=progress_map)


@academy_bp.route('/lesson/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    """Mark a lesson as completed."""
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # Get enrollment
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=lesson.course_id
    ).first()
    
    if not enrollment:
        return jsonify({'success': False, 'message': 'Not enrolled'}), 403
    
    # Get or create progress
    progress = LessonProgress.query.filter_by(
        enrollment_id=enrollment.id,
        lesson_id=lesson_id
    ).first()
    
    if not progress:
        progress = LessonProgress(
            enrollment_id=enrollment.id,
            lesson_id=lesson_id
        )
        db.session.add(progress)
    
    progress.mark_complete()
    
    return jsonify({
        'success': True,
        'progress_percent': enrollment.progress_percent,
        'is_course_completed': enrollment.is_completed
    })


@academy_bp.route('/lesson/<int:lesson_id>/progress', methods=['POST'])
@login_required
def update_progress(lesson_id):
    """Update lesson watch progress."""
    lesson = Lesson.query.get_or_404(lesson_id)
    data = request.get_json()
    
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=lesson.course_id
    ).first()
    
    if not enrollment:
        return jsonify({'success': False}), 403
    
    progress = LessonProgress.query.filter_by(
        enrollment_id=enrollment.id,
        lesson_id=lesson_id
    ).first()
    
    if not progress:
        progress = LessonProgress(
            enrollment_id=enrollment.id,
            lesson_id=lesson_id
        )
        db.session.add(progress)
    
    progress.watch_time_seconds = data.get('watch_time', 0)
    db.session.commit()
    
    return jsonify({'success': True})


# ==================== MY COURSES ====================

@academy_bp.route('/my-courses')
@login_required
def my_courses():
    """View enrolled courses."""
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    
    in_progress = [e for e in enrollments if not e.is_completed]
    completed = [e for e in enrollments if e.is_completed]
    
    return render_template('academy/my_courses.html',
                         in_progress=in_progress,
                         completed=completed)


@academy_bp.route('/certificate/<enrollment_id>')
@login_required
def certificate(enrollment_id):
    """View/download course completion certificate."""
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    
    if enrollment.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('academy.my_courses'))
    
    if not enrollment.is_completed:
        flash('Complete the course first to get your certificate.', 'warning')
        return redirect(url_for('academy.learn', slug=enrollment.course.slug))
    
    # Generate certificate ID if not exists
    if not enrollment.certificate_id:
        enrollment.certificate_id = f"CHG-{enrollment.course_id}-{enrollment.user_id}-{uuid.uuid4().hex[:8].upper()}"
        enrollment.certificate_issued = True
        db.session.commit()
    
    return render_template('academy/certificate.html',
                         enrollment=enrollment)


# ==================== ADMIN ROUTES ====================

@academy_bp.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard for course management."""
    # Check if user is admin (you can add an is_admin field to User model)
    courses = Course.query.all()
    total_students = db.session.query(db.func.count(Enrollment.id)).scalar()
    total_revenue = db.session.query(db.func.sum(Enrollment.amount_paid)).scalar() or 0
    
    return render_template('academy/admin/dashboard.html',
                         courses=courses,
                         total_students=total_students,
                         total_revenue=total_revenue)


@academy_bp.route('/admin/course/new', methods=['GET', 'POST'])
@login_required
def create_course():
    """Create a new course."""
    if request.method == 'POST':
        data = request.form
        
        # Generate slug from title
        slug = data['title'].lower().replace(' ', '-').replace("'", '')
        
        course = Course(
            title=data['title'],
            slug=slug,
            description=data['description'],
            short_description=data.get('short_description', ''),
            price=float(data.get('price', 0)),
            original_price=float(data.get('original_price', 0)) if data.get('original_price') else None,
            category=data.get('category', 'general'),
            level=data.get('level', 'beginner'),
            thumbnail=data.get('thumbnail', ''),
            preview_video=data.get('preview_video', '')
        )
        
        # Set JSON fields
        if data.get('topics'):
            course.set_topics([t.strip() for t in data['topics'].split(',')])
        if data.get('learning_outcomes'):
            course.set_learning_outcomes([o.strip() for o in data['learning_outcomes'].split('\n') if o.strip()])
        if data.get('requirements'):
            course.set_requirements([r.strip() for r in data['requirements'].split('\n') if r.strip()])
        
        db.session.add(course)
        db.session.commit()
        
        flash('Course created successfully!', 'success')
        return redirect(url_for('academy.edit_course', course_id=course.id))
    
    return render_template('academy/admin/course_form.html', course=None)


@academy_bp.route('/admin/course/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    """Edit an existing course."""
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'POST':
        data = request.form
        
        course.title = data['title']
        course.description = data['description']
        course.short_description = data.get('short_description', '')
        course.price = float(data.get('price', 0))
        course.original_price = float(data.get('original_price', 0)) if data.get('original_price') else None
        course.category = data.get('category', 'general')
        course.level = data.get('level', 'beginner')
        course.thumbnail = data.get('thumbnail', '')
        course.preview_video = data.get('preview_video', '')
        
        if data.get('topics'):
            course.set_topics([t.strip() for t in data['topics'].split(',')])
        if data.get('learning_outcomes'):
            course.set_learning_outcomes([o.strip() for o in data['learning_outcomes'].split('\n') if o.strip()])
        if data.get('requirements'):
            course.set_requirements([r.strip() for r in data['requirements'].split('\n') if r.strip()])
        
        db.session.commit()
        flash('Course updated successfully!', 'success')
    
    return render_template('academy/admin/course_form.html', course=course)


@academy_bp.route('/admin/course/<int:course_id>/publish', methods=['POST'])
@login_required
def publish_course(course_id):
    """Publish or unpublish a course."""
    course = Course.query.get_or_404(course_id)
    course.is_published = not course.is_published
    
    if course.is_published and not course.published_at:
        course.published_at = datetime.utcnow()
    
    db.session.commit()
    
    status = 'published' if course.is_published else 'unpublished'
    flash(f'Course {status} successfully!', 'success')
    
    return redirect(url_for('academy.edit_course', course_id=course_id))


@academy_bp.route('/admin/course/<int:course_id>/lessons', methods=['GET', 'POST'])
@login_required
def manage_lessons(course_id):
    """Manage course lessons."""
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'POST':
        data = request.form
        
        # Generate slug
        slug = data['title'].lower().replace(' ', '-').replace("'", '')
        
        lesson = Lesson(
            course_id=course_id,
            title=data['title'],
            slug=slug,
            description=data.get('description', ''),
            content_type=data.get('content_type', 'video'),
            video_url=data.get('video_url', ''),
            video_provider=data.get('video_provider', 'youtube'),
            text_content=data.get('text_content', ''),
            duration_minutes=int(data.get('duration_minutes', 0)),
            is_free_preview=data.get('is_free_preview') == 'on',
            order=course.lessons.count()
        )
        
        db.session.add(lesson)
        course.calculate_duration()
        db.session.commit()
        
        flash('Lesson added successfully!', 'success')
    
    lessons = course.lessons.order_by(Lesson.order).all()
    return render_template('academy/admin/lessons.html', course=course, lessons=lessons)


@academy_bp.route('/admin/lesson/<int:lesson_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_lesson(lesson_id):
    """Edit a lesson."""
    lesson = Lesson.query.get_or_404(lesson_id)
    
    if request.method == 'POST':
        data = request.form
        
        lesson.title = data['title']
        lesson.description = data.get('description', '')
        lesson.content_type = data.get('content_type', 'video')
        lesson.video_url = data.get('video_url', '')
        lesson.video_provider = data.get('video_provider', 'youtube')
        lesson.text_content = data.get('text_content', '')
        lesson.duration_minutes = int(data.get('duration_minutes', 0))
        lesson.is_free_preview = data.get('is_free_preview') == 'on'
        lesson.is_published = data.get('is_published') == 'on'
        
        lesson.course.calculate_duration()
        db.session.commit()
        
        flash('Lesson updated successfully!', 'success')
        return redirect(url_for('academy.manage_lessons', course_id=lesson.course_id))
    
    return render_template('academy/admin/lesson_form.html', lesson=lesson)


@academy_bp.route('/admin/lesson/<int:lesson_id>/delete', methods=['POST'])
@login_required
def delete_lesson(lesson_id):
    """Delete a lesson."""
    lesson = Lesson.query.get_or_404(lesson_id)
    course_id = lesson.course_id
    
    db.session.delete(lesson)
    db.session.commit()
    
    # Recalculate course duration
    course = Course.query.get(course_id)
    course.calculate_duration()
    db.session.commit()
    
    flash('Lesson deleted successfully!', 'success')
    return redirect(url_for('academy.manage_lessons', course_id=course_id))


# ==================== QUIZ ROUTES ====================

@academy_bp.route('/quiz/<int:quiz_id>')
@login_required
def take_quiz(quiz_id):
    """Take a quiz."""
    quiz = Quiz.query.get_or_404(quiz_id)
    lesson = quiz.lesson
    
    # Check enrollment
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=lesson.course_id
    ).first()
    
    if not enrollment:
        flash('Please enroll in the course first.', 'warning')
        return redirect(url_for('academy.course_detail', slug=lesson.course.slug))
    
    # Check attempt limit
    attempts = QuizAttempt.query.filter_by(
        quiz_id=quiz_id,
        user_id=current_user.id
    ).count()
    
    if quiz.max_attempts > 0 and attempts >= quiz.max_attempts:
        flash('You have reached the maximum number of attempts for this quiz.', 'warning')
        return redirect(url_for('academy.learn', slug=lesson.course.slug, lesson=lesson.id))
    
    # Get questions (shuffle if enabled)
    questions = list(quiz.questions.all())
    if quiz.shuffle_questions:
        import random
        random.shuffle(questions)
    
    return render_template('academy/quiz.html',
                         quiz=quiz,
                         questions=questions,
                         lesson=lesson,
                         enrollment=enrollment,
                         attempts_remaining=quiz.max_attempts - attempts if quiz.max_attempts > 0 else 'Unlimited')


@academy_bp.route('/quiz/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    """Submit quiz answers."""
    quiz = Quiz.query.get_or_404(quiz_id)
    lesson = quiz.lesson
    
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=lesson.course_id
    ).first()
    
    if not enrollment:
        return jsonify({'success': False, 'message': 'Not enrolled'}), 403
    
    # Create attempt
    attempt = QuizAttempt(
        quiz_id=quiz_id,
        user_id=current_user.id,
        enrollment_id=enrollment.id
    )
    
    # Collect answers from form
    answers = {}
    for question in quiz.questions:
        answer = request.form.get(f'question_{question.id}')
        if answer is not None:
            answers[str(question.id)] = answer
    
    attempt.set_answers(answers)
    db.session.add(attempt)
    db.session.commit()
    
    # Calculate score
    score = attempt.calculate_score()
    
    # If passed, mark lesson as completed
    if attempt.passed:
        progress = LessonProgress.query.filter_by(
            enrollment_id=enrollment.id,
            lesson_id=lesson.id
        ).first()
        
        if not progress:
            progress = LessonProgress(
                enrollment_id=enrollment.id,
                lesson_id=lesson.id
            )
            db.session.add(progress)
        
        if not progress.is_completed:
            progress.mark_complete()
    
    return redirect(url_for('academy.quiz_results', attempt_id=attempt.id))


@academy_bp.route('/quiz/results/<int:attempt_id>')
@login_required
def quiz_results(attempt_id):
    """View quiz results."""
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    
    if attempt.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('academy.my_courses'))
    
    quiz = attempt.quiz
    lesson = quiz.lesson
    answers = attempt.get_answers()
    
    # Build results with question details
    results = []
    for question in quiz.questions:
        user_answer = answers.get(str(question.id))
        is_correct = question.check_answer(user_answer) if user_answer is not None else False
        
        results.append({
            'question': question,
            'user_answer': user_answer,
            'is_correct': is_correct,
            'options': question.get_options()
        })
    
    return render_template('academy/quiz_results.html',
                         attempt=attempt,
                         quiz=quiz,
                         lesson=lesson,
                         results=results)


# ==================== ADMIN QUIZ ROUTES ====================

@academy_bp.route('/admin/lesson/<int:lesson_id>/quiz', methods=['GET', 'POST'])
@login_required
def manage_quiz(lesson_id):
    """Manage quiz for a lesson."""
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # Get existing quiz or create new
    quiz = Quiz.query.filter_by(lesson_id=lesson_id).first()
    
    if request.method == 'POST':
        if not quiz:
            quiz = Quiz(
                lesson_id=lesson_id,
                title=request.form.get('title', f'Quiz: {lesson.title}')
            )
            db.session.add(quiz)
        
        quiz.title = request.form.get('title', quiz.title)
        quiz.description = request.form.get('description', '')
        quiz.passing_score = int(request.form.get('passing_score', 70))
        quiz.max_attempts = int(request.form.get('max_attempts', 3))
        quiz.shuffle_questions = request.form.get('shuffle_questions') == 'on'
        quiz.show_correct_answers = request.form.get('show_correct_answers') == 'on'
        
        db.session.commit()
        flash('Quiz settings saved!', 'success')
    
    questions = quiz.questions.order_by(QuizQuestion.order).all() if quiz else []
    
    return render_template('academy/admin/quiz_manage.html',
                         lesson=lesson,
                         quiz=quiz,
                         questions=questions)


@academy_bp.route('/admin/quiz/<int:quiz_id>/question', methods=['POST'])
@login_required
def add_question(quiz_id):
    """Add a question to a quiz."""
    quiz = Quiz.query.get_or_404(quiz_id)
    
    question_type = request.form.get('question_type', 'multiple_choice')
    question_text = request.form.get('question_text')
    explanation = request.form.get('explanation', '')
    
    question = QuizQuestion(
        quiz_id=quiz_id,
        question_text=question_text,
        question_type=question_type,
        explanation=explanation,
        order=quiz.questions.count()
    )
    
    if question_type in ['multiple_choice', 'true_false']:
        options = []
        if question_type == 'true_false':
            correct = request.form.get('correct_answer')
            options = [
                {'text': 'True', 'is_correct': correct == '0'},
                {'text': 'False', 'is_correct': correct == '1'}
            ]
        else:
            # Get options from form
            for i in range(4):
                opt_text = request.form.get(f'option_{i}')
                if opt_text:
                    options.append({
                        'text': opt_text,
                        'is_correct': request.form.get('correct_answer') == str(i)
                    })
        question.set_options(options)
    else:
        question.correct_answer = request.form.get('correct_answer', '')
    
    db.session.add(question)
    db.session.commit()
    
    flash('Question added!', 'success')
    return redirect(url_for('academy.manage_quiz', lesson_id=quiz.lesson_id))


@academy_bp.route('/admin/question/<int:question_id>/delete', methods=['POST'])
@login_required
def delete_question(question_id):
    """Delete a quiz question."""
    question = QuizQuestion.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    lesson_id = question.quiz.lesson_id
    
    db.session.delete(question)
    db.session.commit()
    
    flash('Question deleted!', 'success')
    return redirect(url_for('academy.manage_quiz', lesson_id=lesson_id))


# ==================== API ROUTES ====================

@academy_bp.route('/api/courses')
def api_courses():
    """API endpoint for courses."""
    courses = Course.query.filter_by(is_published=True).all()
    
    return jsonify({
        'success': True,
        'courses': [{
            'id': c.id,
            'title': c.title,
            'slug': c.slug,
            'short_description': c.short_description,
            'price': c.price,
            'original_price': c.original_price,
            'thumbnail': c.thumbnail,
            'category': c.category,
            'level': c.level,
            'duration_hours': c.duration_hours,
            'total_students': c.total_students,
            'average_rating': c.average_rating,
            'total_lessons': c.get_total_lessons()
        } for c in courses]
    })

