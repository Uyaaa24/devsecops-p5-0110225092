from flask import Blueprint, jsonify, request

from app.services import task_service
from app.utils.validator import validate_task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


@tasks_bp.get("")
def list_tasks():
    return jsonify(task_service.get_all(request.args.get("status")))


@tasks_bp.get("/<int:task_id>")
def get_task(task_id):
    task = task_service.get_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task tidak ditemukan"}), 404
    return jsonify(task)


@tasks_bp.post("")
def create_task():
    data = request.get_json(silent=True)
    valid, errors = validate_task(data)
    if not valid:
        return jsonify({"errors": errors}), 400
    task = task_service.create(data["title"], data.get("status", "todo"))
    return jsonify(task), 201


@tasks_bp.put("/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True)
    valid, errors = validate_task(data)
    if not valid:
        return jsonify({"errors": errors}), 400
    task = task_service.update(task_id, data.get("title"), data.get("status"))
    if task is None:
        return jsonify({"error": "Task tidak ditemukan"}), 404
    return jsonify(task)


@tasks_bp.delete("/<int:task_id>")
def delete_task(task_id):
    if not task_service.remove(task_id):
        return jsonify({"error": "Task tidak ditemukan"}), 404
    return "", 204