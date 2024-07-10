from flask import Blueprint, request, jsonify
from Classi.ClasseFrontEnd.Classe_t_FrontEndVociMenu.Service_t_FrontEndVociMenu import TFrontEndMenuVociService

feMenufigli = Blueprint('fefigli', __name__)
service = TFrontEndMenuVociService()

# Endpoint per ottenere tutti i figli di un menu principale
@feMenufigli.route('/get_all', methods=['GET'])
def get_all_children():
    try:
        menu_id = request.args.get('menu_id')
        if menu_id is None:
            return jsonify({'error': 'Missing menu_id parameter'}), 400
        
        children = service.get_all_children(int(menu_id))
        return jsonify(children), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@feMenufigli.route('/<int:menu_id>', methods=['GET'])
def get_menu_by_id(menu_id):
    try:
        response, status_code = service.get_menu_by_id(menu_id)
        return response, status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
