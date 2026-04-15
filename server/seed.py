from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Seeding database...")

    #clear any previous records in the db tables
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    #create exercises data
    bench_press = Exercise(name="Bench press", category="Strength", equipment_needed=True)
    squats = Exercise(name="Squats", category="Strength", equipment_needed=False)
    running = Exercise(name="Running", category="Cardio", equipment_needed=False)
    pushups = Exercise(name="Push-ups", category="Push-ups", equipment_needed=False)

    #add and save all the entries in the db
    db.session.add_all([bench_press, squats, running, pushups])
    db.session.commit()

    #create workouts data
    firstworkout = Workout(date=date(2026, 4, 13), duration_minutes=50, notes="Full body intense workout")
    secondworkout = Workout(date=date(2026, 4, 15), duration_minutes=35, notes="Quick cardio session")

    #add and save all data to the db
    db.session.add_all([firstworkout, secondworkout])
    db.session.commit()