from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from AI_engine.Problem_definition import CropPredictionProblem
from AI_engine.Astar_Greedy import GraphSearch
from AI_engine.Genetic import GeneticAlgorithm
import os

prediction_bp = Blueprint('prediction', __name__)

# Create a constant for the data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

@prediction_bp.route('/prediction')
def prediction_page():
    return render_template('prediction.html')

@prediction_bp.route('/api/predict', methods=['POST'])
def predict_crop():
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

        # Create the problem instance
        problem = CropPredictionProblem(environmental_data, os.path.join(DATA_DIR, 'Crop_Data.csv'))

        results = {
            'astar': {
                'success': False,
                'perfect_match': None,
                'recommendations': [],
                'message': '',
                'error': None
            },
            'genetic': {
                'success': False,
                'best_crop': None,
                'fitness': 0,
                'interventions': {},
                'top_crops': [],
                'message': '',
                'error': None
            }
        }

        # --- A* Search ---
        try:
            graph_search = GraphSearch(problem)
            node, crop_or_list, cost = graph_search.search("A*", max_depth=3)

            if node and isinstance(crop_or_list, str):
                # Perfect match found
                results['astar'] = {
                    'success': True,
                    'perfect_match': {
                        'crop': crop_or_list.title(),
                        'cost': round(cost, 2) if cost else 0
                    },
                    'recommendations': [],
                    'message': f'Perfect match found: {crop_or_list.title()}',
                    'error': None
                }
            elif isinstance(crop_or_list, list):
                # Alternative recommendations
                recommendations = []
                for crop, alt_cost, node_item in crop_or_list[:5]:
                    recommendations.append({
                        'crop': crop.title(),
                        'cost': round(alt_cost, 2) if alt_cost else 0,
                        'state': node_item.state.environment.tolist() if node_item and hasattr(node_item.state, 'environment') else None
                    })
                results['astar'] = {
                    'success': True,
                    'perfect_match': None,
                    'recommendations': recommendations,
                    'message': 'No perfect match found, showing best alternatives',
                    'error': None
                }
            else:
                results['astar'] = {
                    'success': False,
                    'perfect_match': None,
                    'recommendations': [],
                    'message': 'No suitable crops found',
                    'error': None
                }
        except Exception as e:
            print(f"A* Search Error: {str(e)}")  # Debug output
            results['astar'] = {
                'success': False,
                'error': str(e),
                'perfect_match': None,
                'recommendations': [],
                'message': f'Error in A* search: {str(e)}'
            }

        # --- Genetic Algorithm ---
        try:
            ga = GeneticAlgorithm(problem)
            best_solution, best_fitness, best_crop, top_crops = ga.solve("predict")

            formatted_interventions = {}
            for i, (intervention_name, _) in enumerate(problem.interventions):
                formatted_interventions[intervention_name] = round(best_solution[i], 1)

            results['genetic'] = {
                'success': True,
                'best_crop': best_crop.title() if best_crop else 'Unknown',
                'fitness': best_fitness,
                'interventions': formatted_interventions,
                'top_crops': [(crop.title(), round(score, 1)) for crop, score in top_crops],
                'message': f'Best crop with interventions: {best_crop.title() if best_crop else "Unknown"}',
                'error': None
            }
        except Exception as e:
            print(f"Genetic Algorithm Error: {str(e)}")  # Debug output
            results['genetic'] = {
                'success': False, 
                'error': str(e),
                'best_crop': None,
                'fitness': 0,
                'interventions': {},
                'top_crops': [],
                'message': f'Error in genetic algorithm: {str(e)}'
            }

        # Store the prediction data in session with correct structure
        session['prediction_data'] = {
            'input': environmental_data,  # Store as list for easy indexing
            'results': results
        }

        return jsonify({'success': True, 'redirect': '/prediction-results'}), 200

    except Exception as e:
        print(f"General Error: {str(e)}")  # Debug output
        return jsonify({'success': False, 'message': f'Error processing prediction: {str(e)}'}), 500


@prediction_bp.route('/prediction-results')
def prediction_results():
    if 'prediction_data' not in session:
        flash('Please submit prediction data first')
        return redirect(url_for('prediction.prediction_page'))

    return render_template('prediction_result.html', prediction_data=session['prediction_data'])