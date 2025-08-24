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

        # Input validation
        if environmental_data[0] < 0 or environmental_data[1] < 0 or environmental_data[2] < 0:
            return jsonify({'success': False, 'message': 'Nutrients (Nitrogen, Phosphorus, Potassium) must be non-negative'}), 400
        if environmental_data[5] < 0 or environmental_data[5] > 14:
            return jsonify({'success': False, 'message': 'pH value must be between 0 and 14'}), 400
        if environmental_data[4] < 0 or environmental_data[4] > 100:
            return jsonify({'success': False, 'message': 'Humidity must be between 0 and 100%'}), 400
        if environmental_data[6] < 20:
            return jsonify({'success': False, 'message': 'Rainfall must be greater than 20mm'}), 400

        print(f"Processing environmental data: {environmental_data}")

        # Create the problem instance
        try:
            from AI_engine.Problem_definition import CropState
            initial_state = CropState(environmental_data)
            problem = CropPredictionProblem(initial_state, os.path.join(DATA_DIR, 'Crop_Data.csv'))
            print(f"Problem created successfully. Initial state: {problem.initial_state}")
        except Exception as e:
            print(f"Error creating problem: {str(e)}")
            return jsonify({'success': False, 'message': f'Error initializing problem: {str(e)}'}), 500

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
        print("Starting A* Search...")
        try:
            graph_search = GraphSearch(problem)
            node, crop_or_list, cost = graph_search.search("A*", max_depth=4)
            print(f"A* Search completed. Node: {node}, Result: {crop_or_list}, Cost: {cost}")

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
                print(f"A* Perfect match: {crop_or_list}")
            elif isinstance(crop_or_list, list) and len(crop_or_list) > 0:
                # Alternative recommendations
                recommendations = []
                for item in crop_or_list[:5]:
                    if isinstance(item, tuple) and len(item) >= 3:
                        crop, alt_cost, node_item = item
                        recommendations.append({
                            'crop': crop.title() if isinstance(crop, str) else str(crop),
                            'cost': round(alt_cost, 2) if alt_cost else 0
                        })
                results['astar'] = {
                    'success': True,
                    'perfect_match': None,
                    'recommendations': recommendations,
                    'message': 'No perfect match found, showing best alternatives',
                    'error': None
                }
                print(f"A* Alternatives: {len(recommendations)} found")
            else:
                results['astar'] = {
                    'success': False,
                    'perfect_match': None,
                    'recommendations': [],
                    'message': 'No suitable crops found with A* search',
                    'error': None
                }
                print("A* No results found")
        except Exception as e:
            error_msg = str(e)
            print(f"A* Search Error: {error_msg}")
            results['astar'] = {
                'success': False,
                'error': error_msg,
                'perfect_match': None,
                'recommendations': [],
                'message': f'Error in A* search: {error_msg}'
            }

        # --- Genetic Algorithm ---
        print("Starting Genetic Algorithm...")
        try:
            ga = GeneticAlgorithm(problem)
            best_solution, best_fitness, best_crop, top_crops = ga.solve("predict")
            print(f"GA completed. Best crop: {best_crop}, Fitness: {best_fitness}")

            if best_solution and best_crop:
                formatted_interventions = {}
                if hasattr(problem, 'interventions') and problem.interventions:
                    for i, (intervention_name, _) in enumerate(problem.interventions):
                        if i < len(best_solution):
                            formatted_interventions[intervention_name] = round(best_solution[i], 1)

                # Ensure top_crops is properly formatted
                formatted_top_crops = []
                if top_crops:
                    for item in top_crops[:5]:
                        if isinstance(item, tuple) and len(item) >= 2:
                            crop, score = item
                            formatted_top_crops.append((
                                crop.title() if isinstance(crop, str) else str(crop), 
                                round(float(score), 1)
                            ))

                results['genetic'] = {
                    'success': True,
                    'best_crop': best_crop.title() if isinstance(best_crop, str) else str(best_crop),
                    'fitness': round(float(best_fitness), 4),
                    'interventions': formatted_interventions,
                    'top_crops': formatted_top_crops,
                    'message': f'Best crop with interventions: {best_crop.title() if isinstance(best_crop, str) else str(best_crop)}',
                    'error': None
                }
                print(f"GA Success: {results['genetic']['best_crop']}")
            else:
                results['genetic'] = {
                    'success': False,
                    'best_crop': None,
                    'fitness': 0,
                    'interventions': {},
                    'top_crops': [],
                    'message': 'Genetic algorithm did not find optimal solution',
                    'error': None
                }
        except Exception as e:
            error_msg = str(e)
            print(f"Genetic Algorithm Error: {error_msg}")
            results['genetic'] = {
                'success': False, 
                'error': error_msg,
                'best_crop': None,
                'fitness': 0,
                'interventions': {},
                'top_crops': [],
                'message': f'Error in genetic algorithm: {error_msg}'
            }

        # Store the prediction data in session with correct structure
        session['prediction_data'] = {
            'input': environmental_data,  # Store as list for easy indexing
            'results': results
        }

        print(f"Final results: A* success={results['astar']['success']}, GA success={results['genetic']['success']}")
        return jsonify({'success': True, 'redirect': '/prediction-results'}), 200

    except Exception as e:
        error_msg = str(e)
        print(f"General Error: {error_msg}")
        return jsonify({'success': False, 'message': f'Error processing prediction: {error_msg}'}), 500


@prediction_bp.route('/prediction-results')
def prediction_results():
    if 'prediction_data' not in session:
        flash('Please submit prediction data first')
        return redirect(url_for('prediction.prediction_page'))

    return render_template('prediction_result.html', prediction_data=session['prediction_data'])