from flask import request, Blueprint, jsonify

from src.repositories.open_ai_process_repository import OpenAiProcessRepository
from src.services.search_by_context_service import *
from src.decorators.authentication_decorator import auth_required

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['GET'])
@auth_required
def index():
    service = SearchByContextService()
    response = service.apply(request.args)
    return jsonify({
      'response': response,
    })
    
@search_bp.route('/search/<process_uuid>', methods=['GET'])
@auth_required
def get(process_uuid):
    repository = OpenAiProcessRepository()
    item = repository.get_by_process_uuid(process_uuid)
    return jsonify({
      'organization': item['organization'] if item else None,
      'question': item['question'] if item else None,
      'response': item['response'] if item else None,
    })