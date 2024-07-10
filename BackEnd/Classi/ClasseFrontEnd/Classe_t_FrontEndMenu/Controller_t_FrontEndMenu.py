from flask import Blueprint, request, jsonify
from Classi.ClasseFrontEnd.Classe_t_FrontEndMenu.Service_t_FrontEndMenu import TFrontEndMenuService

feMenuPadre = Blueprint('fepadre', __name__)
service = TFrontEndMenuService()

@feMenuPadre.route('/get_all', methods=['GET'])
def get_all_menus():
    try:
        response = service.get_all_menus()
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@feMenuPadre.route('/<int:menu_id>', methods=['GET'])
def get_menu_by_id(menu_id):
    try:
        menu = service.get_menu_by_id(menu_id)
        return jsonify(menu)
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400  # Esempio di gestione di un errore specifico (ValueError)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Gestione generica degli errori


@feMenuPadre.route('/get_by_ids', methods=['GET'])
def get_menus_by_ids():
    try:
        ids = request.args.getlist('id')  # Questo prende tutti i valori della query parameter 'id'
        if not ids:
            return jsonify({'error': 'Parameter "id" is required'}), 400

        menus = []
        for menu_id in ids:
            menu = service.get_menu_by_id(int(menu_id))
            menus.append(menu)

        return jsonify(menus)
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500