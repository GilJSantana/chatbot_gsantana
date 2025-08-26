'''
O módulo de rotas cria os acessos as funcionaliades da API.

'''

from flask import Blueprint, request, jsonify
from backend.services.faq_service import FAQServices
from backend.repositories.faq_repository import FAQRepository
from .database import db
from .models import FAQ

faq_bp = Blueprint('faq_bp', __name__, url_prefix='/api/faq')

faq_repository = FAQRepository()
faq_service = FAQServices(faq_repository)


# Rota para acessar a funcionalidade de busca de FAQs
@faq_bp.route('/search', methods=['GET'])
def search_faqs():
    query = request.args.get('q', '')
    faqs = faq_service.search_faqs(query)
    best_match = faqs[0]
    return jsonify({
        'answer': best_match.answer,
        'confidence': 1.0  # Implementar lógica de confiança, se necessário.
    })


# Rota para acessar a funcionalidade que adiciona novas FAQs (Admin)
@faq_bp.route('/add', methods=['POST'])
def add_faq():
    data = request.json
    try:
        new_faq = faq_service.add_faq(data)
        return jsonify({
            'message': 'FAQ adicionada com sucesso.',
            'faq': new_faq.to_dict()
        }), 201
    except ValueError as error:
        return jsonify({'error': str(error)}), 400


# Rota para acessar a funcionalidade de edição de FAQs (Admin)
@faq_bp.route('/edit/<int:faq_id>', methods=['PUT'])
def edit_faq(faq_id):
    data = request.json
    try:
        updated_faq = faq_service.update_faq(faq_id, data)
        if updated_faq:
            return jsonify({
                'message': 'FAQ atualizada com sucesso.',
                'faq': updated_faq.to_dict()
            }), 200
        return jsonify({'error': 'FAQ não encontrada.'}), 404
    except ValueError as error:
        return jsonify({'error': str(error)}), 400


# Rota para acessar a funcionalidade que deleta uma FAQs (Admin)
@faq_bp.route('/delete/<int:faq_id>', methods=['DELETE'])
def delete_faq(faq_id):
    if faq_service.delete_faq(faq_id):
        return jsonify({'message': 'FAQ deletada com sucesso.'}), 200
    return jsonify({'error': 'FAQ não encontrada.'}), 404


# Rota para acessar a funcionalidade que lista todas as FAQs (Admin)
@faq_bp.route('/all', methods=['GET'])
def get_all_faqs():
    faqs = faq_service.get_all_faqs()
    return jsonify([faq.to_dict() for faq in faqs])
