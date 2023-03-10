from flask import Blueprint, jsonify
from src.services.search_by_context_service import *
import datetime

health_bp = Blueprint('health_bp', __name__)

@health_bp.route('/health', methods=['GET'])
def index():
    return jsonify({
      'success': 'true',
      'datetime': datetime.datetime.utcnow()
    })