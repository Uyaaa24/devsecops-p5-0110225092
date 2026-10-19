import time

from flask import Flask, jsonify

from app.routes.tasks import tasks_bp

_START_TIME = time.time()


def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024  # batasi body 10 KB
    app.register_blueprint(tasks_bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "uptime": round(time.time() - _START_TIME, 2)})

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Endpoint tidak ditemukan"}), 404

    @app.get("/")
    def index():
        html = """
        <!DOCTYPE html>
        <html lang="id">
        <head><meta charset="utf-8"><title>Task Manager</title></head>
        <body style="font-family:sans-serif;max-width:480px;margin:40px auto">
          <h1>Task Manager API</h1>
          <p>Status: <b>berjalan</b></p>
          <ul>
            <li><a href="/health">/health</a></li>
            <li><a href="/api/tasks">/api/tasks</a></li>
          </ul>
        </body>
        </html>
        """
        return html

    return app