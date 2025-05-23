from marshmallow import Schema, fields, validate, validates, ValidationError, post_load
from datetime import datetime, date

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    category = fields.Str(required=True, validate=validate.OneOf(['strength', 'cardio', 'flexibility', 'sports']))
    equipment_needed = fields.Bool(load_default=False)
    
    # Schema validations
    @validates('name')
    def validate_name(self, value):
        if not value or not value.strip():
            raise ValidationError("Name cannot be empty or just whitespace")
        if any(char.isdigit() for char in value):
            raise ValidationError("Exercise name should not contain numbers")
    
    @validates('category')
    def validate_category_format(self, value):
        if value and not value.islower():
            raise ValidationError("Category must be lowercase")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True, format='%Y-%m-%d')
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=480))
    notes = fields.Str(load_default="", validate=validate.Length(max=500))
    exercises = fields.Nested('ExerciseSchema', many=True, dump_only=True)
    workout_exercises = fields.Nested('WorkoutExerciseSchema', many=True, dump_only=True)
    
    # Schema validations
    @validates('date')
    def validate_date(self, value):
        if value > date.today():
            raise ValidationError("Workout date cannot be in the future")
        # Don't allow workouts older than 2 years
        if value < date(date.today().year - 2, 1, 1):
            raise ValidationError("Workout date cannot be more than 2 years old")
    
    @validates('notes')
    def validate_notes_content(self, value):
        if value and value.strip() != value:
            raise ValidationError("Notes should not have leading or trailing whitespace")


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1, max=1000))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1, max=50))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1, max=7200))  # Max 2 hours
    
    # Nested relationships for detailed output
    workout = fields.Nested(WorkoutSchema, dump_only=True, exclude=['workout_exercises'])
    exercise = fields.Nested(ExerciseSchema, dump_only=True)
    
    @validates('reps')
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Reps must be a positive number")
    
    @validates('sets')  
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Sets must be a positive number")


# Schema instances for use in routes
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)