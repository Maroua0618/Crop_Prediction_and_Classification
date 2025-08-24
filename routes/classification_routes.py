from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from AI_engine.Problem_definition import CropPredictionProblem
from AI_engine.Utility_functions import get_crop_requirements
from app import db
from models import PredictionResult
import json
import os

classification_bp = Blueprint('classification', __name__)

# Create a constant for the data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

@classification_bp.route('/classification')
def classification_page():
    return render_template('classification.html')

@classification_bp.route('/api/classify', methods=['POST'])
def classify_crop():
    try:
        data = request.form
        try:
            environmental_data = [
                float(data.get('Nitrogen', 0)),
                float(data.get('Phosphorus', 0)),
                float(data.get('Potassium', 0)),
                float(data.get('Temperature', 0)),
                float(data.get('Humidity', 0)),
                float(data.get('Ph', 0)),
                float(data.get('Rainfall', 0))
            ]
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': 'Invalid input data. Please enter valid numbers.'}), 400

        if environmental_data[5] < 0 or environmental_data[5] > 14:
            return jsonify({'success': False, 'message': 'pH value must be between 0 and 14'}), 400
        if environmental_data[4] < 0 or environmental_data[4] > 100:
            return jsonify({'success': False, 'message': 'Humidity must be between 0 and 100%'}), 400
        if environmental_data[6] < 0:
            return jsonify({'success': False, 'message': 'Rainfall cannot be negative'}), 400

        crop_requirements = get_crop_requirements(os.path.join(DATA_DIR, 'Crop_recommendationV2.csv'))
        problem = CropPredictionProblem(environmental_data, os.path.join(DATA_DIR, 'Crop_Data.csv'))

        direct_matches = []
        partial_matches = {}

        for crop, ranges in crop_requirements.items():
            match_count = 0
            total_features = len(problem.feature_names)

            for i, feature in enumerate(problem.feature_names):
                min_val, max_val = ranges[feature]
                if min_val <= environmental_data[i] <= max_val:
                    match_count += 1

            match_percentage = (match_count / total_features) * 100

            if match_percentage == 100:
                direct_matches.append(crop.title())
            elif match_percentage >= 60:
                partial_matches[crop.title()] = round(match_percentage, 1)

        sorted_partial = sorted(partial_matches.items(), key=lambda x: x[1], reverse=True)

        environmental_dict = {}
        for i, feature in enumerate(problem.feature_names):
            environmental_dict[feature] = environmental_data[i]

        results = {
            'direct_matches': direct_matches,
            'partial_matches': sorted_partial[:5],
            'environmental_data': environmental_dict
        }

        session['classification_data'] = {
            'input': environmental_data,
            'results': results
        }

        if 'user_id' in session:
            try:
                classification = PredictionResult(
                    user_id=session['user_id'],
                    algorithm='classification',
                    input_data=json.dumps(environmental_data),
                    result_data=json.dumps(results, default=str)
                )
                db.session.add(classification)
                db.session.commit()
            except Exception as e:
                print(f"Database save error: {str(e)}")

        return jsonify({'success': True, 'redirect': '/classification-results'}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error processing classification: {str(e)}'}), 500

@classification_bp.route('/classification-results')
def classification_results():
    if 'classification_data' not in session:
        flash('Please submit classification data first')
        return redirect(url_for('classification.classification_page'))

    return render_template('classification_result.html', classification_data=session['classification_data'])