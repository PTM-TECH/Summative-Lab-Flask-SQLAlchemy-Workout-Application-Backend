from marshmallow import Schema, fields, validates, ValidationError

#create schema for Exercise
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool()

    @validates('name')
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise ValidationError("Exercise name must be at least 2 characters long")

    @validates('category')
    def validate_category(self, value):
        if not value.strip():
            raise ValidationError("Category is required")


#create schema for WorkoutExercise
class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()

    @validates('reps')
    def validate_reps(self, value):
        if value is not None and value < 0:
            raise ValidationError("Reps cannot be negative")

    @validates('sets')
    def validate_sets(self, value):
        if value is not None and value < 0:
            raise ValidationError("Sets cannot be negative")

    @validates('duration_seconds')
    def validate_duration(self, value):
        if value is not None and value < 0:
            raise ValidationError("Duration cannot be negative")

#create schema for Workout
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str()

    # Nested relationship
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)

    @validates('duration_minutes')
    def validate_duration(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("Duration must be greater than 0")