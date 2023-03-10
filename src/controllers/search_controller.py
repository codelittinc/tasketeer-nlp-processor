from flask import request, Blueprint, jsonify
from src.services.search_by_context_service import *

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['GET'])
def index():
    service = SearchByContextService()
    response = service.apply(request.args)
    return jsonify({
      'response': response,
    })