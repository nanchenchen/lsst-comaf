from lsst.sims.maf.db import trackingDb, resultsDb
import marisa_trie
import json

class MetricObj(object):
    """
    Save a metric as an object
    """
    def __init__(self, metadata):
        self.metadata = metadata
        self.plots = {}
        self.stats = []

    def __repr__(self):
        return json.dumps(self.metadata)

class RunObj(object):
    """
    Save a run as an object
    """
    def __init__(self, metadata):
        self.metadata = metadata
        self.metrics = None
        self.run_db = resultsDb.ResultsDb(resultsDbAddress='sqlite:///' + self.metadata['mafDir'] + '/resultsDb_sqlite.db')
        # initialize dictionary
        self.metric_objs = {}
        self.load_metric_objs()

    def load_metric_objs(self):

        metadata_list = ['metricId', 'metricName', 'slicerName', 'metricMetadata', 'simDataName', 'metricDataFile',
                        'displayGroup', 'displaySubgroup', 'displayOrder', 'displayCaption']

        # join metrics and displays
        sql = 'SELECT A.metricId, ' + ', '.join(metadata_list[1:]) + ' FROM displays AS A, metrics AS B WHERE A.metricId = B.metricId'
        metrics = self.run_db.session.execute(sql).fetchall()

        for metric in metrics:
            metadata = {}
            for m in metadata_list:
                metadata[m] = getattr(metric, m)
            metric_obj = MetricObj(metadata)
            self.metric_objs[metadata['metricId']] = metric_obj
            metric_obj.run = self

        # get all plots
        plots = self.run_db.session.query(resultsDb.PlotRow).all()
        for plot in plots:
            self.metric_objs[plot.metricId].plots[plot.plotType] = plot.plotFile

        # get all stats
        stats = self.run_db.session.query(resultsDb.SummaryStatRow).all()
        for stat in stats:
            self.metric_objs[stat.metricId].stats.append({'summaryName': stat.summaryName,
                                                      'summaryValue': stat.summaryValue})
    def __repr__(self):
        return json.dumps(self.metadata)


class ShowMafDBController(object):

    def load_run_objs(self):
        self.run_objs = []
        runs = self.tracking_db.session.query(trackingDb.RunRow).all()
        metadata_list = ['mafRunId', 'opsimRun', 'opsimComment', 'mafComment', 'mafDir', 'opsimDate', 'mafDate']
        for run in runs:
            metadata = {}
            for m in metadata_list:
                metadata[m] = getattr(run, m)
            run_obj = RunObj(metadata)
            self.run_objs.append(run_obj)

    def __init__(self, tracking_db_address):
        self.tracking_db = trackingDb.TrackingDb(trackingDbAddress=tracking_db_address)
        self.run_objs = []
        self.load_run_objs()

    def build_metric_index(self):
        """
        Using trie (a data structure) to build index tree for metrics,
        so that searching across runs is easier
        """

        self.all_metrics_obj = []
        self.all_metrics_idx = {}

        all_metrics_name = []
        all_metrics_slicer = []
        #all_metrics_metadata = []
        all_metrics_sim_data = []
        all_metrics_tuple = []

        for run_obj in self.run_objs:
            for idx in run_obj.metric_objs:
                metric_obj = run_obj.metric_objs[idx]
                all_metrics_name.append(metric_obj.metadata['metricName'])
                all_metrics_slicer.append(metric_obj.metadata['slicerName'])
                #all_metrics_metadata.append(metric_obj.metadata['metricMetadata'])
                all_metrics_sim_data.append(metric_obj.metadata['simDataName'])
                self.all_metrics_obj.append(metric_obj)

        all_metrics_tuple = map(lambda x: tuple([x]), range(len(self.all_metrics_obj)))
        self.all_metrics_idx['name'] = marisa_trie.RecordTrie('I', zip(all_metrics_name, all_metrics_tuple))
        self.all_metrics_idx['slicer'] = marisa_trie.RecordTrie('I', zip(all_metrics_slicer, all_metrics_tuple))
        self.all_metrics_idx['sim_data'] = marisa_trie.RecordTrie('I', zip(all_metrics_sim_data, all_metrics_tuple))

