from flask import request, Blueprint, jsonify
from bson import ObjectId

from src.decorators.authentication_decorator import auth_required
from src.repositories.api_key_repository import ApiKeyRepository

api_key_bp = Blueprint('api_key_bp', __name__)

@api_key_bp.route('/api_key', methods=['POST'])
@auth_required
def store_api_key():
    request_data = request.json
    repository = ApiKeyRepository()
    result = repository.encrypt_and_store_key(request_data)
    return jsonify(result)


@api_key_bp.route('/api_key/<organization_id>', methods=['DELETE'])
@auth_required
def delete_api_key(organization_id):
    repository = ApiKeyRepository()
    deleted_count = repository.delete_by_organization_id(organization_id)
    return jsonify({'status': 'API key deleted successfully', 'deleted_count': deleted_count})