from flask import request, Blueprint, jsonify
from src.services.upsert_file_index_service import *

file_index_bp = Blueprint('file_index_bp', __name__)

@file_index_bp.route('/file_index', methods=['POST'])
def index():
    request_data = request.json
    service = UpsertFileIndexService()
    entity_id = service.apply(request_data)
    return jsonify({'id': entity_id})