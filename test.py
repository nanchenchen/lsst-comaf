import lsst.sims.maf.db as db
from lsst.sims.maf.viz import MafTracking

trackingDbAddress = "sqlite:///maf_cadence/trackingDb_sqlite.db"
trackingDb = db.TrackingDb(trackingDbAddress=trackingDbAddress)
runlist = MafTracking(trackingDbAddress)