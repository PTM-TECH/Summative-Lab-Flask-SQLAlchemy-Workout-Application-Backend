from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

#initialize schemas
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()

#home route
@app.route('/')
def home():
    return make_response(jsonify({"message": "Workout Tracker API running"}))

#Workout routes
#workouts route -> GET/ get all workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)

#Get single workout
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}, 404)
    return make_response(jsonify(workout_schema.dump(workout)), 200)

#Create workout -> POST
@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = request.get_json()
        validated_data = workout_schema.load(data)
        workout = Workout(**validated_data)
        #add and save to db
        db.session.add(workout)
        db.session.commit()
        return make_response(jsonify(workout_schema.dump(workout)), 201)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

#Delete a workout -> DELETE
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    #delete the workout from the db
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted successfully"}), 200

#Exercise routes
#Get all exercises -> GET
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)

#Get a single exercise -> GET
@app.route('/exercises/<int:id>')
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return make_response(jsonify(exercise_schema.dump(exercise)), 200)

#create exercise -> POST
@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = request.get_json()
        validated_data = exercise_schema.load(data)
        exercise = Exercise(**validated_data)
        # add and save exercise to database
        db.session.add(exercise)
        db.session.commit()
        return make_response(jsonify(exercise_schema.dump(exercise)), 201)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
#delete exercise -> DELETE
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    #delete the exercise from the db
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise deleted successfully"}), 200

#add exercise to workout -> Join table
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    try:
        workout = Workout.query.get(workout_id)
        exercise = Exercise.query.get(exercise_id)

        if not workout or not exercise:
            return jsonify({"error": "Workout or exercise not found"}), 404
        
        data = request.get_json()
        workout_exercise = WorkoutExercise(
            workout_id = workout_id,
            exercise_id = exercise_id,
            reps = data.get('reps'),
            sets = data.get('sets'),
            duration_seconds = data.get('duration_seconds')
        )
        #add and save workout_exercise to the db
        db.session.add(workout_exercise)
        db.session.commit()
        return make_response(jsonify(workout_exercise_schema.dump(workout_exercise)), 201)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)