from flask import Blueprint, request, jsonify
from Classi.ClasseAlimenti.Classe_t_alimenti.Service_t_alimenti import ServiceAlimenti

t_alimenti_controller = Blueprint('alimenti', __name__)
service_alimenti = ServiceAlimenti()

@t_alimenti_controller.route('/get_all', methods=['GET'])
def get_all():
    alimenti = service_alimenti.get_all()
    return jsonify(alimenti)

@t_alimenti_controller.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    alimento = service_alimenti.get_by_id(id)
    return jsonify(alimento)

@t_alimenti_controller.route('/create', methods=['POST'])
def create():
    dati = request.json
    required_fields = ['Alimento', 'Energia_Kcal', 'Energia_KJ', 'Prot_Tot_Gr', 'Glucidi_Tot', 'Lipidi_Tot', 'Saturi_Tot', 'fkAllergene', 'fkTipologiaAlimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        Alimento = dati['Alimento'].strip()
        Energia_Kcal = float(dati['Energia_Kcal'])
        Energia_KJ = float(dati['Energia_KJ'])
        Prot_Tot_Gr = float(dati['Prot_Tot_Gr'])
        Glucidi_Tot = float(dati['Glucidi_Tot'])
        Lipidi_Tot = float(dati['Lipidi_Tot'])
        Saturi_Tot = float(dati['Saturi_Tot'])
        fkAllergene = dati['fkAllergene'].strip()
        fkTipologiaAlimento = int(dati['fkTipologiaAlimento'])

        return jsonify(service_alimenti.create(Alimento, Energia_Kcal, Energia_KJ, Prot_Tot_Gr, Glucidi_Tot, Lipidi_Tot, Saturi_Tot, fkAllergene, fkTipologiaAlimento))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_alimenti_controller.route('/update/<int:id>', methods=['PUT'])
def update(id):
    dati = request.json
    required_fields = ['Alimento', 'Energia_Kcal', 'Energia_KJ', 'Prot_Tot_Gr', 'Glucidi_Tot', 'Lipidi_Tot', 'Saturi_Tot', 'fkAllergene', 'fkTipologiaAlimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        Alimento = dati['Alimento'].strip()
        Energia_Kcal = float(dati['Energia_Kcal'])
        Energia_KJ = float(dati['Energia_KJ'])
        Prot_Tot_Gr = float(dati['Prot_Tot_Gr'])
        Glucidi_Tot = float(dati['Glucidi_Tot'])
        Lipidi_Tot = float(dati['Lipidi_Tot'])
        Saturi_Tot = float(dati['Saturi_Tot'])
        fkAllergene = dati['fkAllergene'].strip()
        fkTipologiaAlimento = int(dati['fkTipologiaAlimento'])

        return jsonify(service_alimenti.update(id, Alimento, Energia_Kcal, Energia_KJ, Prot_Tot_Gr, Glucidi_Tot, Lipidi_Tot, Saturi_Tot, fkAllergene, fkTipologiaAlimento))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_alimenti_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    return jsonify(service_alimenti.delete(id))
