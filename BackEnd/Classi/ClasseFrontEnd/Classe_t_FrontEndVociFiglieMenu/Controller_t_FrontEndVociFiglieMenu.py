from flask import Blueprint, request, jsonify
from Classi.ClasseFrontEnd.Classe_t_FrontEndVociFiglieMenu.Service_t_FrontEndVociFiglieMenu import TFrontEndMenuVociFiglieService

feMenunipoti = Blueprint('fenipoti', __name__)
service = TFrontEndMenuVociFiglieService()

@feMenunipoti.route('/get_all', methods=['GET'])
def get_all_menus():
    try:
        response, status_code = service.get_all_menus()
        return response, status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@feMenunipoti.route('/<int:menu_id>', methods=['GET'])
def get_menu_by_id(menu_id):
    try:
        response, status_code = service.get_menu_by_id(menu_id)
        return response, status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
