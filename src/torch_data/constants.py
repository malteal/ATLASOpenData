# TODO: @ANDREAS Move below to concrete datafiles.
KEYS = ['csts', 'csts_columns', 'csts_culens', 'event_info', 'event_info_columns', 'jets', 'jets_columns']
CSTS_COLUMNS = [
    "b'InDetTrackParticlesAuxDyn.phi'",
    "b'InDetTrackParticlesAuxDyn.numberOfPixelHits'",
    "b'InDetTrackParticlesAuxDyn.numberOfPixelHoles'",
    "b'InDetTrackParticlesAuxDyn.numberOfPixelSharedHits'",
    "b'InDetTrackParticlesAuxDyn.numberOfPixelDeadSensors'",
    "b'InDetTrackParticlesAuxDyn.numberOfSCTHits'",
    "b'InDetTrackParticlesAuxDyn.numberOfSCTHoles'",
    "b'InDetTrackParticlesAuxDyn.numberOfSCTSharedHits'",
    "b'InDetTrackParticlesAuxDyn.numberOfSCTDeadSensors'",
    "b'InDetTrackParticlesAuxDyn.qOverP'",
    "b'InDetTrackParticlesAuxDyn.numberOfInnermostPixelLayerHits'",
    "b'InDetTrackParticlesAuxDyn.chiSquared'",
    "b'InDetTrackParticlesAuxDyn.numberDoF'",
    "b'InDetTrackParticlesAuxDyn.d0'",
    "b'InDetTrackParticlesAuxDyn.z0'",
    "b'InDetTrackParticlesAuxDyn.theta'",
    "b'InDetTrackParticlesAuxDyn.vz'",
    "b'InDetTrackParticlesAuxDyn.numberOfTRTHits'",
    "b'InDetTrackParticlesAuxDyn.numberOfTRTOutliers'",
    "b'InDetTrackParticlesAuxDyn.eta'",
    "b'InDetTrackParticlesAuxDyn.pt'"
]
TRACKS_COLUMNS_LOOKUP = {s: idx for idx, s in enumerate(CSTS_COLUMNS)}
JETS_COLUMNS = [
    "b'InDetTrackParticlesAuxDyn.phi'",
    "b'InDetTrackParticlesAuxDyn.numberOfPixelHits'",
    "b'InDetTrackParticlesAuxDyn.numberOfPixelHoles'",
    "b'InDetTrackParticlesAuxDyn.numberOfPixelSharedHits'",
    "b'InDetTrackParticlesAuxDyn.numberOfPixelDeadSensors'",
    "b'InDetTrackParticlesAuxDyn.numberOfSCTHits'",
    "b'InDetTrackParticlesAuxDyn.numberOfSCTHoles'",
    "b'InDetTrackParticlesAuxDyn.numberOfSCTSharedHits'",
    "b'InDetTrackParticlesAuxDyn.numberOfSCTDeadSensors'",
    "b'InDetTrackParticlesAuxDyn.qOverP'",
    "b'InDetTrackParticlesAuxDyn.numberOfInnermostPixelLayerHits'",
    "b'InDetTrackParticlesAuxDyn.chiSquared'",
    "b'InDetTrackParticlesAuxDyn.numberDoF'",
    "b'InDetTrackParticlesAuxDyn.d0'",
    "b'InDetTrackParticlesAuxDyn.z0'",
    "b'InDetTrackParticlesAuxDyn.theta'",
    "b'InDetTrackParticlesAuxDyn.vz'",
    "b'InDetTrackParticlesAuxDyn.numberOfTRTHits'",
    "b'InDetTrackParticlesAuxDyn.numberOfTRTOutliers'",
    #"b'InDetTrackParticlesAuxDyn.eta'",
    #"b'InDetTrackParticlesAuxDyn.pt'"
]
JETS_COLUMNS_LOOKUP = {s: idx for idx, s in enumerate(JETS_COLUMNS)}