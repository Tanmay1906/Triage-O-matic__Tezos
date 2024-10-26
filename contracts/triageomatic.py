import smartpy as sp

class TriageOMatic(sp.Contract):
    def __init__(self):
        self.init(
            incidents=sp.big_map(tkey=sp.TNat, tvalue=sp.TRecord(
                id=sp.TNat, 
                description=sp.TString, 
                timeline=sp.TList(sp.TString), 
                affectedSystems=sp.TList(sp.TString), 
                anomalyAlerts=sp.TList(sp.TString), 
                evidenceChain=sp.TList(sp.TString)
            )), 
            evidences=sp.big_map(tkey=sp.TNat, tvalue=sp.TRecord(
                id=sp.TNat, 
                description=sp.TString, 
                hash=sp.TBytes
            )), 
            incidentCounter=0, 
            evidenceCounter=0
        )

    @sp.entry_point
    def addIncident(self, params):
        new_id = self.data.incidentCounter + 1
        new_incident = sp.record(
            id=new_id, 
            description=params.description, 
            timeline=params.timeline, 
            affectedSystems=params.affectedSystems, 
            anomalyAlerts=params.anomalyAlerts, 
            evidenceChain=params.evidenceChain
        )
        self.data.incidents[new_id] = new_incident
        self.data.incidentCounter += 1
        sp.emit(sp.record(incidentId=new_id, description=params.description), tag="IncidentLogged")

    @sp.entry_point
    def getIncidentDetails(self, params):
        sp.result(self.data.incidents[params.incidentId])

    @sp.entry_point
    def logEvidence(self, params):
        new_id = self.data.evidenceCounter + 1
        new_evidence = sp.record(
            id=new_id, 
            description=params.description, 
            hash=params.hash
        )
        self.data.evidences[new_id] = new_evidence
        self.data.evidenceCounter += 1
        sp.emit(sp.record(evidenceId=new_id, description=params.description, hash=params.hash), tag="EvidenceLogged")

    @sp.entry_point
    def verifyEvidenceImmutability(self, params):
        evidence = self.data.evidences[params.evidenceId]
        sp.result(evidence.hash == params.hash)

@sp.add_test(name="TriageOMatic Test")
def test():
    scenario = sp.test_scenario()
    scenario.h1("TriageOMatic")

    contract = TriageOMatic()
    scenario += contract

    scenario += contract.addIncident(
        description="Incident1", 
        timeline=["Step1", "Step2"], 
        affectedSystems=["System1"], 
        anomalyAlerts=["Alert1"], 
        evidenceChain=["Evidence1"]
    ).run()
    scenario.verify(contract.data.incidentCounter == 1)

    scenario += contract.getIncidentDetails(incidentId=1)

    scenario += contract.logEvidence(
        description="Evidence1", 
        hash=sp.bytes("0x1234")
    ).run()
    scenario.verify(contract.data.evidenceCounter == 1)

    scenario += contract.verifyEvidenceImmutability(
        evidenceId=1, 
        hash=sp.bytes("0x1234")
    ).run(result=True)
    scenario += contract.verifyEvidenceImmutability(
        evidenceId=1, 
        hash=sp.bytes("0x5678")
    ).run(result=False)
