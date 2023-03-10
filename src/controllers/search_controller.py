from flask import request, Blueprint, jsonify
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