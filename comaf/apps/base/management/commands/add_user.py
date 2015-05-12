from django.core.management.base import BaseCommand, make_option, CommandError

class Command(BaseCommand):
    help = "Add a new user."
    args = "<username> <email>"

    def handle(self, username, email, *args, **options):

        from comaf.apps.base.tasks import create_user

        create_user(username, email)
