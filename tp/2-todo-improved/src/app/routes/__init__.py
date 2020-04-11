from app.routes.admin import admin, admin_status, admin_lock, admin_delete
from app.routes.admin_todo import admin_task_listing, admin_task_add, admin_task_edit, admin_task_delete, admin_task_status
from app.routes.login import login, register
from app.routes.todo import index, add, edit, status
from app.routes.error import page_not_found