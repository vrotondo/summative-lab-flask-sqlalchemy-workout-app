from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
from datetime import datetime

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    # Table constraints
    __table_args__ = (
        CheckConstraint('length(name) >= 2', name='check_name_length'),
        CheckConstraint("category IN ('strength', 'cardio', 'flexibility', 'sports')", name='check_valid_category'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises', overlaps="workout_exercises")
    
    # Model validations
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters long")
        return name.strip().title()
    
    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['strength', 'cardio', 'flexibility', 'sports']
        if category.lower() not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return category.lower()
    
    def __repr__(self):
        return f'<Exercise {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'
    
    # Table constraints
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_positive_duration'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan', overlaps="workouts")
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', overlaps="workout_exercises")
    
    # Model validations
    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration is None or duration <= 0:
            raise ValueError("Duration must be a positive number")
        if duration > 480:  # 8 hours max
            raise ValueError("Duration cannot exceed 480 minutes (8 hours)")
        return duration
    
    @validates('notes')
    def validate_notes(self, key, notes):
        if notes and len(notes) > 500:
            raise ValueError("Notes cannot exceed 500 characters")
        return notes
    
    def __repr__(self):
        return f'<Workout {self.id} on {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    
    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises', overlaps="exercises,workouts")
    exercise = db.relationship('Exercise', back_populates='workout_exercises', overlaps="exercises,workouts")
    
    # Ensure unique workout-exercise combinations
    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='unique_workout_exercise'),
    )
    
    def __repr__(self):
        return f'<WorkoutExercise workout:{self.workout_id} exercise:{self.exercise_id}>'