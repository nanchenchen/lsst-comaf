from django.contrib.auth.models import User
from django.core.files import File


from comaf.apps.base.models import UserKey
from comaf.apps.base.utils import dbController
from comaf.apps.metrics.models import OpsimRun, Metric, Plot

import os
import hashlib
import datetime
import traceback
from time import gmtime, strftime

def create_user(name, email):
    user = User()
    user.username = name
    user.email = email
    user.is_staff = False
    user.save()
    key = UserKey(user=user, value=generate_new_key(name))
    key.save()


def generate_new_key(name):
    time_str = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return hashlib.sha224(name + time_str).hexdigest()

def parse_date(date_str):
    return datetime.datetime.strptime( date_str, "%m/%d/%y" )

def import_from_sqlite(tracking_db_path, username='admin'):
    db_ctrl = dbController.ShowMafDBController(tracking_db_address='sqlite:///' + tracking_db_path)
    import_user = User.objects.get(username=username)

    for run in db_ctrl.run_objs:
        run_db_obj, created = OpsimRun.objects.get_or_create(name=run.metadata['opsimRun'],
                                                             comment=run.metadata['opsimComment'],
                                                             date=parse_date(run.metadata['opsimDate']))


    for metric in db_ctrl.all_metrics:
        metric_db_obj, created = Metric.objects.get_or_create(name=metric.metadata['metricName'],
                                                              owner=import_user,
                                                              opsim_run=OpsimRun.objects.get(name=metric.run.metadata['opsimRun']),
                                                              metadata=metric.metadata['metricMetadata'],
                                                              slicer=metric.metadata['slicerName'],
                                                              display_group=metric.metadata['displayGroup'],
                                                              display_subgroup=metric.metadata['displaySubgroup'],
                                                              display_order=metric.metadata['displayOrder'],
                                                              display_caption=metric.metadata['displayCaption'],
                                                              maf_comment=metric.run.metadata['mafComment'],
                                                              maf_date=parse_date(metric.run.metadata['mafDate']))



        for type, src in metric.plots.iteritems():
            plot, created = Plot.objects.get_or_create(metric=metric_db_obj, type=type)
            #print metric.metadata['metricName'], type, src
            src = src.replace(":", "_")

            try:
                src_path = os.path.join(metric.metadata['mafDir'], src)
                file = open(src_path)
                django_file = File(file)
                filename = "%04d_%s/%s" %(import_user.id, import_user.username, src)
                plot.src.save(filename, django_file)
                file.close()
            except:
                import pdb
                pdb.set_trace()
                traceback.print_exc()

            try:
                thumb = "thumb." + src[:-4] + ".png"
                thumb_path = os.path.join(metric.metadata['mafDir'], thumb)
                file = open(thumb_path)
                django_file = File(file)
                filename = "%04d_%s/%s" %(import_user.id, import_user.username, thumb)
                plot.thumb.save(filename, django_file)
                file.close()
            except:
                import pdb
                pdb.set_trace()
                traceback.print_exc()

            plot.save()



