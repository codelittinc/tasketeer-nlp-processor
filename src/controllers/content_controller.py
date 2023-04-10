from flask import request, Blueprint, jsonify
from src.decorators.authentication_decorator import auth_required
from src.services.upsert_file_index_service import *
from src.repositories.file_indexer_status_repository import *

content_bp = Blueprint('content_bp', __name__)

@content_bp.route('/contents', methods=['POST'])
@auth_required
def index():
    request_data = request.json
    service = UpsertFileIndexService()
    response = service.apply(request_data)
    return jsonify(response)


@content_bp.route('/contents/<process_uuid>', methods=['GET'])
@auth_required
def status(process_uuid):
    repository = FileIndexerStatusRepository()
    item = repository.get_by_process_uuid(process_uuid)
    return jsonify({
      'organization': item['organization'] if item else None,
      'process_uuid': item['process_uuid'] if item else None,
      'created_at': item['created_at'] if item else None,
    })