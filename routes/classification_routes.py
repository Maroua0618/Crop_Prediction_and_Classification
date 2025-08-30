import numpy as np
from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from AI_engine.Problem_definition import CropPredictionProblem
from AI_engine.Astar_Greedy import GraphSearch
from AI_engine.Genetic import GeneticAlgorithm
from AI_engine.CSP import run_csp
import os

classification_bp = Blueprint('classification', __name__)

# Create a constant for the data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

def convert_numpy_types(obj):
    """Recursively convert NumPy types to native Python types for JSON serialization."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_numpy_types(item) for item in obj)
    else:
        return obj

@classification_bp.route('/classification')
def classification_page():
    return render_template('classification.html')

@classification_bp.route('/api/classify', methods=['POST'])
def classify_crops():
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
            print(f"Problem created successfully.")
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
            'greedy': {  
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
                'top_crops': None,
                'interventions': {},
                'message': '',
                'error': None
            },
            'csp': {  
                'success': False,
                'message': '',
                'data': None,
                'error': None
            }
        }

        # --- A* Search ---
        print("Starting A* Search...")
        try:
            graph_search = GraphSearch(problem)
            node, crop_or_list, cost = graph_search.search("A*", max_depth=4)
            print(f"A* Search completed. Result: {crop_or_list}, Cost: {cost}")

            if node and isinstance(crop_or_list, str):
                # Perfect match found
                results['astar'] = {
                    'success': True,
                    'perfect_match': {
                        'crop': crop_or_list.title(),
                        'cost': round(float(cost), 2) if cost else 0
                    },
                    'recommendations': [],
                    'message': f'Perfect match found: {crop_or_list.title()}',
                    'error': None
                }
                print(f"A* Perfect match: {crop_or_list}")
            elif isinstance(crop_or_list, list) and len(crop_or_list) > 0:
                # Alternative recommendations
                recommendations = []
                if crop_or_list:
                    for item in crop_or_list[:5]:   # just take the first 5 items
                        if isinstance(item, tuple) and len(item) >= 3:
                            crop, alt_cost, node_item = item
                            recommendations.append({
                                'crop': crop.title() if isinstance(crop, str) else str(crop),
                                'cost': round(float(alt_cost), 2) if alt_cost else 0
                        })

                results['astar'] = {
                    'success': True,
                    'perfect_match': None,
                    'recommendations': recommendations,
                    'message': 'No perfect match found, showing best alternative',
                    'error': None
                }
                
            else:
                results['astar'] = {
                    'success': False,
                    'perfect_match': None,
                    'recommendations': [],
                    'message': 'No suitable crop found with A* search',
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
            
        # --- Greedy Search ---
        print("Starting Greedy Search...")
        try:
            graph_search = GraphSearch(problem)
            node, crop_or_list, cost = graph_search.search("Greedy_search", max_depth=4)
            print(f"Greedy Search completed. Result: {crop_or_list}, Cost: {cost}")

            if node and isinstance(crop_or_list, str):
                # Perfect match found
                results['greedy'] = {
                    'success': True,
                    'perfect_match': {
                        'crop': crop_or_list.title(),
                        'cost': round(float(cost), 2) if cost else 0
                    },
                    'recommendations': [],
                    'message': f'Perfect match found: {crop_or_list.title()}',
                    'error': None
                }
                print(f"Greedy Perfect match: {crop_or_list}")
            elif isinstance(crop_or_list, list) and len(crop_or_list) > 0:
                # Alternative recommendations
                recommendations = []
                if crop_or_list:
                    for item in crop_or_list[:5]:   # just take the first 5 items
                        if isinstance(item, tuple) and len(item) >= 3:
                            crop, alt_cost, node_item = item
                            recommendations.append({
                                'crop': crop.title() if isinstance(crop, str) else str(crop),
                                'cost': round(float(alt_cost), 2) if alt_cost else 0
                        })

                results['greedy'] = {
                    'success': True,
                    'perfect_match': None,
                    'recommendations': recommendations,
                    'message': 'No perfect match found, showing best alternative',
                    'error': None
                }
                print(f"Greedy Alternatives: {len(recommendations)} found")
            else:
                results['greedy'] = {
                    'success': False,
                    'perfect_match': None,
                    'recommendations': [],
                    'message': 'No suitable crop found with Greedy search',
                    'error': None
                }
                print("Greedy No results found")
        except Exception as e:
            error_msg = str(e)
            print(f"Greedy Search Error: {error_msg}")
            results['greedy'] = {
                'success': False,
                'error': error_msg,
                'perfect_match': None,
                'recommendations': [],
                'message': f'Error in Greedy search: {error_msg}'
            }
            
        # --- Genetic Algorithm ---
        print("Starting Genetic Algorithm...")
        try:
            ga = GeneticAlgorithm(problem)
            best_solution, best_fitness, best_crop, top_crops = ga.solve("classify")
            print(f"GA completed. Best crop: {best_crop}, Fitness: {best_fitness}")
            print(f"Top crops: {top_crops}")

            if best_solution and best_crop:
                formatted_interventions = {}
                if hasattr(problem, 'interventions') and problem.interventions:
                    for i, (intervention_name, _) in enumerate(problem.interventions):
                        if i < len(best_solution):
                            formatted_interventions[intervention_name] = round(float(best_solution[i]), 1)
                formatted_top_crops=[] 
                if top_crops:
                    for crop_item in top_crops: 
                        crop_solution = crop_item[2] if len(crop_item) > 2 else None
                        
                        
                        formatted_top_crops.append({
                            'crop': crop_item[0].title() if isinstance(crop_item[0], str) else str(crop_item[0]),
                            'cost': round(float(crop_item[1]), 2) if crop_item[1] else 0,
                            
                        })

                results['genetic'] = {
                    'success': True,
                    'best_crop': best_crop.title() if isinstance(best_crop, str) else str(best_crop),
                    'fitness': round(float(best_fitness), 4),
                    'top_crops': formatted_top_crops,
                    'interventions': formatted_interventions,
                    'message': f'Best crop with interventions: {best_crop.title() if isinstance(best_crop, str) else str(best_crop)}',
                    'error': None
                }
                
            else:
                results['genetic'] = {
                    'success': False,
                    'best_crop': None,
                    'fitness': 0,
                    'top_crops': [],
                    'interventions': {},
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
                'top_crops': [],
                'interventions': {},
                'message': f'Error in genetic algorithm: {error_msg}'
            }
            
        # --- CSP ---
 
        print("Starting CSP...")
        try:
            csp_result = run_csp(environmental_data)
            print("CSP completed.")
 
            if csp_result:
                # Get the top crop from alternative_crops
                alternative_crops = csp_result.get('alternative_crops', {})
                if alternative_crops:
                    
                    sorted_crops = sorted(alternative_crops.items(), 
                                        key=lambda x: x[1]['percentage'], 
                                        reverse=True)
                    top_crops = sorted_crops[:5]

                    # Create a simplified CSP result with just the top recommendations
                    simplified_csp_result = {
                        'crops': top_crops,
                        'suitability_percentage': round(top_crops[0][1]['percentage'], 1),
                          'matching_conditions': [],
                        'non_matching_conditions': [],
                        'solution': csp_result.get('solution', {}),
                        'resources': csp_result.get('resources', {}),
                        'environment': csp_result.get('environment', {}),
                        
                    }
                    
                    # Parse the details to separate matching vs non-matching conditions
                    for crop_name, crop_data in top_crops:
                        for detail in crop_data.get('details', []):
                            if '✓' in detail:
                                simplified_csp_result['matching_conditions'].append(detail)
                            else:
                                simplified_csp_result['non_matching_conditions'].append(detail)
                    
                    # Convert to ensure JSON serialization
                    serializable_csp_result = convert_numpy_types(simplified_csp_result)
                    
                    results['csp'] = { 
                        'success': True,
                        'message': f'Best crop recommendation: {top_crops}',
                        'data': serializable_csp_result
                    } 
                else:
                    results['csp'] = {
                        'success': False,
                        'message': 'No suitable crops found',
                        'data': None
                    }
            else:
                results['csp'] = {
                    'success': False,
                    'message': 'CSP did not find a solution',
                    'data': None
                }
        except Exception as e:
            error_msg = str(e)
            print(f"CSP Error: {error_msg}")
            results['csp'] = {
                'success': False,
                'error': error_msg,
                'message': f'Error in CSP: {error_msg}'
            }
        # Convert all results to ensure JSON serialization
        results = convert_numpy_types(results)

        # Store the classification data in session with correct structure
        session['classification_data'] = {
            'input': environmental_data,  # Store as list for easy indexing
            'results': results
        }

        print(f"Final results: A* success={bool(results['astar']['success'])}, Greedy success={bool(results['greedy']['success'])}, GA success={bool(results['genetic']['success'])}, CSP success={bool(results['csp']['success'])}")
        return jsonify({'success': True, 'redirect': '/classification-results'}), 200

    except Exception as e:
        error_msg = str(e)
        print(f"General Error: {error_msg}")
        return jsonify({'success': False, 'message': f'Error processing classification: {error_msg}'}), 500


@classification_bp.route('/classification-results')
def classification_results():
    if 'classification_data' not in session:
        flash('Please submit classification data first')
        return redirect(url_for('classification.classification_page'))

    return render_template('classification_result.html', classification_data=session['classification_data'])