from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

#create Exercise Model

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    #create relationship
    workout_exercises = db.relationship("WorkoutExercise",
                        back_populates="exercise",
                        cascade="all, delete-orphan"
                        )
    workouts =  db.relationship("Workout",
                secondary="workout_exercises",
                back_populates="exercises"
                )
    def __repr__(self):
        return f"Exercise(id='{self.id}', name='{self.name}', category='{self.category}')"

#create Workout Model
class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    #create relationship
    workout_exercises = db.relationship('WorkoutExercise',
                        back_populates='workout',
                        cascade='all, delete-orphan'
                        )

    exercises = db.relationship('Exercise',
                secondary='workout_exercises',
                back_populates='workouts'
                )

    def __repr__(self):
        return f"Workout(id='{self.id}', date='{self.date}' duration='{self.duration_minutes}'min)"

#create WorkoutExercise Model -> Join table

class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id =    db.Column(
                    db.Integer,
                    db.ForeignKey('workouts.id'),
                    nullable=False
    )
    exercise_id =   db.Column(
                    db.Integer,
                    db.ForeignKey('exercises.id'),
                    nullable=False
    )
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    #create relationship
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    def __repr__(self):
        return (
            f"<WorkoutExercise id={self.id} "
            f"workout_id={self.workout_id} "
            f"exercise_id={self.exercise_id} "
            f"reps={self.reps} sets={self.sets} duration={self.duration_seconds}>"
        )