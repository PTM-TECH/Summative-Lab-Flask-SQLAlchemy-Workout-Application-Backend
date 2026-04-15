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

    #link workouts table and exercises table
    we1 = WorkoutExercise(workout_id = firstworkout.id, exercise_id = bench_press.id, reps=15, sets=3)
    we2 = WorkoutExercise(workout_id = firstworkout.id, exercise_id=squats.id, reps=20, sets=3)
    we3 = WorkoutExercise(workout_id=secondworkout.id, exercise_id=running.id, duration_seconds=1200)
    we4 = WorkoutExercise(workout_id=firstworkout.id, exercise_id=pushups.id, reps=10, sets=5)

    #add and save the data in db
    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()

    print("Seeding completed successfully.")