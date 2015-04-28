#! /usr/bin/env python
from tornado import ioloop
from tornado import web
from jinja2 import Environment, FileSystemLoader
import os, argparse


from lsst.sims.maf.viz import MafTracking, controller
import lsst.sims.maf.db as db

import json

class RunSelectHandler(web.RequestHandler):
    def get(self):
        selectTempl = env.get_template("runselect.html")
        if 'runId' in self.request.arguments:
            runId = int(self.request.arguments['runId'][0])
        else:
            # Set runID to a negative number, to default to first run.
            runId = startRunId
        self.write(selectTempl.render(runlist=runlist, runId=runId, jsPath=jsPath))

class MetricSelectHandler(web.RequestHandler):
    def get(self):
        selectTempl = env.get_template("metricselect.html")
        runId = int(self.request.arguments['runId'][0])
        self.write(selectTempl.render(runlist=runlist, runId=runId))

class MetricResultsPageHandler(web.RequestHandler):
    def get(self):
        resultsTempl = env.get_template("results.html")
        runId = int(self.request.arguments['runId'][0])
        if 'metricId' in self.request.arguments:
            metricIdList = self.request.arguments['metricId']
        else:
            metricIdList = []
        if 'Group_subgroup' in self.request.arguments:
            groupList = self.request.arguments['Group_subgroup']
        else:
            groupList = []
        self.write(resultsTempl.render(metricIdList=metricIdList, groupList=groupList,
                                    runId=runId, runlist=runlist))

class DataHandler(web.RequestHandler):
    def get(self):
        runId = int(self.request.arguments['runId'][0])
        metricId = int(self.request.arguments['metricId'][0])
        if 'datatype' in self.request.arguments:
            datatype = self.request.arguments['datatype'][0].lower()
        else:
            datatype = 'npz'
        run = runlist.getRun(runId)
        metric = run.metricIdsToMetrics([metricId])
        if datatype == 'npz':
            npz = run.getNpz(metric)
            if npz is None:
                self.write('No npz file available.')
            else:
                self.redirect(npz)
        elif datatype == 'json':
            jsn = run.getJson(metric)
            if jsn is None:
                self.write('No JSON file available.')
            else:
                self.write(jsn)
        else:
            self.write('Data type "%s" not understood.' %(datatype))

class ConfigPageHandler(web.RequestHandler):
    def get(self):
        configTempl = env.get_template("configs.html")
        runId = int(self.request.arguments['runId'][0])
        self.write(configTempl.render(runlist=runlist, runId=runId))

class StatPageHandler(web.RequestHandler):
    def get(self):
        statTempl = env.get_template("stats.html")
        runId = int(self.request.arguments['runId'][0])
        self.write(statTempl.render(runlist=runlist, runId=runId))

class AllMetricResultsPageHandler(web.RequestHandler):
    def get(self):
        """Load up the files and display """
        allresultsTempl = env.get_template("allmetricresults.html")
        runId = int(self.request.arguments['runId'][0])
        self.write(allresultsTempl.render(runlist=runlist, runId=runId))

class MultiColorPageHandler(web.RequestHandler):
    def get(self):
        """Display sky maps. """
        multiColorTempl = env.get_template("multicolor.html")
        runId = int(self.request.arguments['runId'][0])
        self.write(multiColorTempl.render(runlist=runlist, runId=runId))

class showMaf(web.RequestHandler):
    def get(self):
        template = env.get_template("showMaf.html")
        self.write(template.render())        

class showRun(web.RequestHandler):
    def get(self, id):
        template = env.get_template("showRun.html")
        self.write(template.render(runId=int(id)))

class searchMetric(web.RequestHandler):
    def get(self):
        template = env.get_template("search.html")
        self.write(template.render())
        
#REST api
class SearchHandler(web.RequestHandler):
    """return all the runs in json format"""
    def initialize(self, trackingDbAddress):
        self.controller = controller.ShowMafDBController(trackingDbAddress)

    def get(self):
        list_type = self.get_argument('list_type')
        if list_type == 'metrics':
            results = self.controller.get_all_metrics()
        if list_type == 'sim_data':
            results = self.controller.get_all_sim_data()
        if list_type == 'slicer':
            results = self.controller.get_all_slicer()
        self.write(json.dumps(results))

    def post(self):
        keywords = self.get_argument('keywords')
        results = self.controller.search_metrics(json.loads(keywords))
        self.write(json.dumps(results))

class RunListHandler(web.RequestHandler):
    """return all the runs in json format"""
    def initialize(self, trackingDbAddress):
        self.runlist = MafTracking(trackingDbAddress)
    def get(self):
        runs = [dict(zip(self.runlist.runs.dtype.names,x)) for x  in self.runlist.runs ]
        for run in runs:
            run['mafRunId'] = int(run['mafRunId'])
        self.write(json.dumps(runs))

class RunHandler(web.RequestHandler):
    """return metrics of a run in a tree-structured way in json format"""
    def initialize(self, trackingDbAddress):
        self.runlist = MafTracking(trackingDbAddress)
    def get(self, id):
        mafRun = self.runlist.getRun(int(id))
        mafRunInfo = self.runlist.getRunInfo(int(id))

        run = dict()
        runInfo = [dict(zip(mafRunInfo.dtype.names,x)) for x  in mafRunInfo ][0]
        metrics = []
        # TODO: make this recursive so that the groups go to more/less than two levels
        groups = mafRun.groups.keys()
        for g in groups:
            members = []
            for sg in mafRun.groups[g]:
                subsetMembers = []
                subsetMetrics = mafRun.metricsInSubgroup(g, sg)
                for metric in subsetMetrics:
                    metricInfo = mafRun.metricInfo(metric)
                    caption = mafRun.captionForMetric(metric)
                    metricInfo['metricId'] = int(metric[0])
                    plotInfo = mafRun.plotsForMetric(metric)
                    plotdict = mafRun.plotDict(plotInfo)
                    plots = []
                    for plottype in plotdict:
                        plots.append({
                            'plotType': plottype,
                            'plotFile': plotdict[plottype]['plotFile'][0],
                            'thumbFile': plotdict[plottype]['thumbFile'][0]
                        })

                    metricInfo['plots'] = plots
                    metricInfo['caption'] = caption
                    subsetMembers.append(json.loads(json.dumps(metricInfo)))
                members.append({"groupName": sg, "members": subsetMembers})    
            metrics.append({"groupName": g, "members": members})
        run['runInfo'] = runInfo
        run['metrics'] = metrics
        self.write(json.dumps(run, indent=3))
        
        
        
def make_app(trackingDbAddress):
    """The tornado global configuration """
    application = web.Application([
        ("/", RunSelectHandler),
        web.url(r"/runList", RunListHandler, dict(trackingDbAddress=trackingDbAddress), name="runList"),
        web.url(r"/run/([0-9]*)", RunHandler, dict(trackingDbAddress=trackingDbAddress), name="run"),
        web.url(r"/search", SearchHandler, dict(trackingDbAddress=trackingDbAddress), name="search"),
        ("/showMaf", showMaf),
        ("/searchMetric", searchMetric),
        web.url(r"/showRun/([0-9]*)", showRun),
        (r"/maf_cadence/(.*)", web.StaticFileHandler, {'path': mafDbDir}),
        ("/metricSelect", MetricSelectHandler),
        ("/metricResults", MetricResultsPageHandler),
        ("/getData", DataHandler),
        ("/configParams", ConfigPageHandler),
        ("/summaryStats", StatPageHandler),
        ("/allMetricResults", AllMetricResultsPageHandler),
        ("/multiColor", MultiColorPageHandler),

        (r"/(favicon.ico)", web.StaticFileHandler, {'path':faviconPath}),
       # (r"/(sorttable.js)", web.StaticFileHandler, {'path':jsPath}),
        (r"/fonts/(.*)", web.StaticFileHandler, {'path':os.path.join(mafDir, 'lsst/sims/maf/viz/statics/css/fonts')}),
        (r"/*/(.*)", web.StaticFileHandler, {'path':staticpath}),
        
        ], debug=True)
    return application

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Python script to display MAF output in a web browser."+
                                     "  After launching, point your browser to 'http://localhost:8989/'")
    defaultdb = os.path.join(os.getcwd(), 'trackingDb_sqlite.db')
    defaultdb = 'sqlite:///' + defaultdb
    parser.add_argument("-t", "--trackingDb", type=str, default=defaultdb, help="Tracking database dbAddress.")
    parser.add_argument("-d", "--mafDir", type=str, default=None, help="Add this directory to the trackingDb and open immediately.")
    parser.add_argument("-c", "--mafComment", type=str, default=None, help="Add a comment to the trackingDB describing the MAF analysis of this directory (paired with mafDir argument).")
    parser.add_argument("-p", "--port", type=int, default=8989, help="Port for connecting to showMaf.")
    args = parser.parse_args()

    # Check tracking DB is sqlite (and add as convenience if forgotten).
    trackingDbAddress = args.trackingDb
    if not trackingDbAddress.startswith('sqlite:///'):
        trackingDbAddress = 'sqlite:///' + trackingDbAddress
    print 'Using tracking database at %s' %(trackingDbAddress)

    global startRunId
    startRunId = -666
    # If given a directory argument:
    if args.mafDir is not None:
        mafDir = os.path.realpath(args.mafDir)
        if not os.path.isdir(mafDir):
            print 'There is no directory containing MAF outputs at %s.' %(mafDir)
            print 'Just opening using tracking db at %s.' %(trackingDbAddress)
        # Open tracking database to add a run.
        trackingDb = db.TrackingDb(trackingDbAddress=trackingDbAddress)
        # Set opsim comment and name from the config files from the run.
        opsimComment = ''
        opsimRun = ''
        opsimDate = ''
        mafDate = ''
        if os.path.isfile(os.path.join(mafDir, 'configSummary.txt')):
            file = open(os.path.join(mafDir, 'configSummary.txt'))
            for line in file:
                tmp = line.split()
                if tmp[0].startswith('RunName'):
                    opsimRun = ' '.join(tmp[1:])
                if tmp[0].startswith('RunComment'):
                    opsimComment = ' '.join(tmp[1:])
                if tmp[0].startswith('MAFVersion'):
                    mafDate =  tmp[-1]
                if tmp[0].startswith('OpsimVersion'):
                    opsimDate = tmp[-2]
                    # Let's go ahead and make the formats match
                    opsimDate = opsimDate.split('-')
                    opsimDate = opsimDate[1]+'/'+opsimDate[2]+'/'+opsimDate[0][2:]
        # Give some feedback to the user about what we're doing.
        print 'Adding to tracking database at %s:' %(trackingDbAddress)
        print ' MafDir = %s' %(mafDir)
        print ' MafComment = %s' %(args.mafComment)
        print ' OpsimRun = %s' %(opsimRun)
        print ' OpsimComment = %s' %(opsimComment)
        print ' OpsimDate = %s' %(opsimDate)
        print ' MafDate = %s' %(mafDate)
        # Add the run.
        startRunId = trackingDb.addRun(opsimRun, opsimComment, args.mafComment, mafDir, opsimDate, mafDate)
        print ' Used runID %d' %(startRunId)
        trackingDb.close()

    # Open tracking database and start visualization.
    global runlist
    runlist = MafTracking(trackingDbAddress)
    if startRunId < 0:
        startRunId = runlist.runs[0]['mafRunId']
    # Set up path to template and favicon paths, and load templates.
    mafDir = ""#os.getenv('SIMS_MAF_DIR')
    templateDir = os.path.join(mafDir, 'lsst/sims/maf/viz/templates/' )
    global faviconPath
    faviconPath = os.path.join(mafDir, 'lsst/sims/maf/viz/')
    global jsPath
    jsPath = os.path.join(mafDir, 'lsst/sims/maf/viz/statics/js')
    
    env = Environment(loader=FileSystemLoader(templateDir))
    # Add 'zip' to jinja templates.
    env.globals.update(zip=zip)

    global staticpath
    staticpath = os.path.join(mafDir, 'lsst/sims/maf/viz/statics/')

    global mafDbDir
    mafDbDir = os.path.join(mafDir, 'maf_cadence/')

    # Start up tornado app.
    application = make_app(trackingDbAddress)
    application.listen(args.port)
    print 'Tornado Starting: \nPoint your web browser to http://localhost:%d/ \nCtrl-C to stop' %(args.port)

    ioloop.IOLoop.instance().start()

