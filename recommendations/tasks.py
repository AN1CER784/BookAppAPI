from celery import shared_task


@shared_task
def get_user_recommendations():
    from management.commands.get_recommendations import Command
    Command().handle()
