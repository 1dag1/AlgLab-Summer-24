import math

import networkx as nx
from data_schema import Donation, Solution , Donor, Recipient
from database import TransplantDatabase
from ortools.sat.python.cp_model import FEASIBLE, OPTIMAL, CpModel, CpSolver


class CrossoverTransplantSolver:
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
        compatible_donors = {j: self.database.get_compatible_donors(Recipient(id=j)) for j in allRecipients}

        #Variables
        self.x = {}
        for i in allDonors:
            for j in allRecipients:
                if Recipient(id=j) in compatible_recipients[i]:
                    self.x[i, j] = self.model.NewBoolVar(f"x_{i}_{j}")


        #Objective
        self.model.Maximize(sum(self.x[i, j.id] for i in allDonors for j in compatible_recipients[i]))

        #Constrains

        #Only one transplantation per donor
        for i in allDonors:
            self.model.Add(sum(self.x[i, j.id] for j in compatible_recipients[i]) <= 1)

        #Only one transplantation per recipient
        for j in allRecipients:
            self.model.Add(sum(self.x[i.id, j] for i in compatible_donors[j]) <= 1)

        #Only donations when friend gets transplantation as well

        for i in allDonors:
            recipientID = self.database.get_partner_recipient(Donor(id=i)).id
            self.model.Add(sum(self.x[i, j.id] for j in compatible_recipients[i]) <= sum(self.x[k.id, recipientID]for k in compatible_donors[recipientID]))

        #Max one Donation for one representative
        for j in allRecipients:
            JDPartnerIDS = []
            jDonorPartners = self.database.get_partner_donors(Recipient(id=j))
            for donorPartner in jDonorPartners:
                JDPartnerIDS.append(donorPartner.id)
            self.model.Add((sum(self.x[dPartnerID, k.id] for dPartnerID in JDPartnerIDS for k in compatible_recipients[dPartnerID]) == sum(self.x[i.id ,j] for i in compatible_donors[j])))

        self.solver = CpSolver()
        self.solver.parameters.log_search_progress = True


    def optimize(self, timelimit: float = math.inf) -> Solution:
        """
        Solves the constraint programming model and returns the optimal solution (if found within time limit).
        :param timelimit: The maximum time limit for the solver.
        :return: A list of Donation objects representing the best solution, or None if no solution was found.
        """
        if timelimit <= 0.0:
            return Solution(donations=[])
        if timelimit < math.inf:
            self.solver.parameters.max_time_in_seconds = timelimit
        # TODO: Implement me!
        status = self.solver.Solve(self.model)
        allDonors = range(1, len(self.database.get_all_donors()) + 1 )


        donations = []
        for i in allDonors:
            for j in self.database.get_compatible_recipients(Donor(id=i)):
                if ((self.solver.Value(self.x[i, j.id])) == 1):
                    donations.append(Donation(donor= Donor(id= i), recipient= Recipient(id=j.id)))

        return Solution(donations=donations)
