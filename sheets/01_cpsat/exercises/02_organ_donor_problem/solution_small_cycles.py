import math
from collections import defaultdict

import networkx as nx
from data_schema import Donation, Solution, Donor, Recipient
from database import TransplantDatabase
from ortools.sat.python.cp_model import FEASIBLE, OPTIMAL, CpModel, CpSolver


class CycleLimitingCrossoverTransplantSolver:
    def __init__(self, database: TransplantDatabase) -> None:
        """
        Constructs a new solver instance, using the instance data from the given database instance.
        :param Database database: The organ donor/recipients database.
        """

        self.database = database
        # TODO: Implement me!
        self.model = CpModel()

        allDonors = range(1, len(self.database.get_all_donors()) + 1)
        allRecipients = range(1, len(self.database.get_all_recipients()) + 1)


        compatible_recipients = {i: self.database.get_compatible_recipients(Donor(id=i)) for i in allDonors}

        partner_recipient = []
        for donor in allDonors:
            partner_recipient.append(self.database.get_partner_recipient(Donor(id=donor)))

        partner_donors = {j: self.database.get_partner_donors(Recipient(id=j)) for j in allDonors}

        #Variables
        self.x = {}
        for i in allDonors:
            for j in allRecipients:
                self.x[i, j] = self.model.NewBoolVar(f"x_{i}_{j}")

        #Objective
        self.model.Maximize(sum(self.x[i, j] for i in allDonors for j in allRecipients))

        #Constrains
        #only compatible transplantations

        for i in allDonors:
            for j in allRecipients:
                self.model.Add(self.x[i, j] <= int(Recipient(id=j) in compatible_recipients[i]))

        #Only one transplantation per donor
        for i in allDonors:
            self.model.Add(sum(self.x[i, j] for j in allRecipients) <= 1)

        #Only one transplantation per recipient
        for j in allRecipients:
            self.model.Add(sum(self.x[i, j] for i in allDonors) <= 1)

        #Only donations when friend gets transplantation as well

        for i in allDonors:
            recipientID = partner_recipient[i-1].id
            self.model.Add(sum(self.x[i, j] for j in allRecipients) <= sum(self.x[k, recipientID]for k in allDonors))

        #Max one Donation for one representative
        for j in allRecipients:
            JDPartnerIDS = []
            jDonorPartners = partner_donors[j]
            for donorPartner in jDonorPartners:
                JDPartnerIDS.append(donorPartner.id)
            self.model.Add((sum(self.x[dPartnerID, k] for dPartnerID in JDPartnerIDS for k in allRecipients) == sum(
                self.x[i, j] for i in allDonors)))
        self.solver = CpSolver()
        self.solver.parameters.log_search_progress = True




        for i in allDonors:
            otherPartnerDonorsIDs = []
            irecipient = partner_recipient[i -1]
            otherPartnerDonors = partner_donors[irecipient.id]
            for otherPartnerDonor in otherPartnerDonors:
                otherPartnerDonorsIDs.append(otherPartnerDonor.id)
            for j in allRecipients:
                jpartnerDonorsIDs = []
                jpartnerDonors = partner_donors[j]
                for jpartnerDonor in jpartnerDonors:
                    jpartnerDonorsIDs.append(jpartnerDonor.id)
                for k in allRecipients:
                    kpartnerDonorsIDs = []
                    kpartnerDonors = partner_donors[k]
                    for kpartnerDonor in kpartnerDonors:
                        kpartnerDonorsIDs.append(kpartnerDonor.id)
                    self.model.Add(4*(sum(self.x[otherPartnerDonorID, j] for otherPartnerDonorID in otherPartnerDonorsIDs)) +(2*(sum(self.x[partnerDonorID,k] for partnerDonorID in jpartnerDonorsIDs)))+ 3*(sum(self.x[partnerDonorID2, irecipient.id] for partnerDonorID2 in jpartnerDonorsIDs)) + sum(self.x[kpartnerDonorID, irecipient.id] for kpartnerDonorID in kpartnerDonorsIDs)  <= 9)
                    self.model.Add(4*(sum(self.x[otherPartnerDonorID, j] for otherPartnerDonorID in otherPartnerDonorsIDs)) +(2*(sum(self.x[partnerDonorID,k] for partnerDonorID in jpartnerDonorsIDs)))+ 3*(sum(self.x[partnerDonorID2, irecipient.id] for partnerDonorID2 in jpartnerDonorsIDs)) + sum(self.x[kpartnerDonorID, irecipient.id] for kpartnerDonorID in kpartnerDonorsIDs)  != 6)

    def optimize(self, timelimit: float = math.inf) -> Solution:
        if timelimit <= 0.0:
            return Solution(donations=[])
        if timelimit < math.inf:
            self.solver.parameters.max_time_in_seconds = timelimit
        # TODO: Implement me!
        status = self.solver.Solve(self.model)
        allDonors = range(1, len(self.database.get_all_donors()) + 1 )
        allRecipients = range(1, len(self.database.get_all_recipients()) + 1 )

        donations = []
        for i in allDonors:
            for j in allRecipients:
                if ((self.solver.Value(self.x[i, j])) == 1):
                    donations.append(Donation(donor= Donor(id= i), recipient= Recipient(id=j)))

        return Solution(donations=donations)
