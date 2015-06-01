from django.core.management.base import BaseCommand, make_option, CommandError

class Command(BaseCommand):
    help = "Import from a tracking db."
    args = "<tracking db>"
    option_list = BaseCommand.option_list + (
        make_option('-u', '--username',
                    action='store',
                    dest='username',
                    help='Set the owner of the files'
        ),
    )
    def handle(self, db_path, *args, **options):

        from comaf.apps.base.tasks import import_from_sqlite

        username = options.get('username', None)
        if username:
            import_from_sqlite(tracking_db_path=db_path, username=username)
        else:
            import_from_sqlite(tracking_db_path=db_path)