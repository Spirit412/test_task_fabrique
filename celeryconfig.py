from api.config import settings

broker_url = settings.CELERY_BROKER_URL
result_backend = settings.CELERY_RESULT_BACKEND

accept_content = ['json', 'msgpack', 'yaml']
task_serializer = 'json'
result_serializer = 'json'
timezone = 'Europe/Moscow'
enable_utc = True

task_routes = {
    'api.celery_worker.Tasks.resize_asset_task': 'low-priority',
    'api.celery_worker.CRONTasks.cron_my_test_task': 'low-priority'
}
