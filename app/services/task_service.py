from datetime import datetime, timezone

_tasks = []
_next_id = 1


def get_all(status=None):
    if status:
        return [t for t in _tasks if t["status"] == status]
    return list(_tasks)


def get_by_id(task_id):
    for task in _tasks:
        if task["id"] == task_id:
            return task
    return None


def create(title, status="todo"):
    global _next_id
    task = {
        "id": _next_id,
        "title": title.strip(),
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _next_id += 1
    _tasks.append(task)
    return task


def update(task_id, title=None, status=None):
    task = get_by_id(task_id)
    if task is None:
        return None
    if title is not None:
        task["title"] = title.strip()
    if status is not None:
        task["status"] = status
    return task


def remove(task_id):
    task = get_by_id(task_id)
    if task is None:
        return False
    _tasks.remove(task)
    return True


def reset():
    global _next_id
    _tasks.clear()
    _next_id = 1