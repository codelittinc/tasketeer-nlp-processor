from flask import request, Blueprint, jsonify
from src.decorators.authentication_decorator import auth_required
from src.services.upsert_file_index_service import *

file_index_bp = Blueprint('file_index_bp', __name__)

@file_index_bp.route('/file_index', methods=['POST'])
@auth_required
def index():
    request_data = request.json
    service = UpsertFileIndexService()
    response = service.apply(request_data)
    return jsonify(response)