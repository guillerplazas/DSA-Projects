# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from dlist import DList  # importing the class DList that was provided to us directly
from dlist import DNode  # importing the class DNode that was provided to us directly

# The csv module implements classes to read and write tabular data in CSV (Command Separated Values) format. It implements classes read and write tabular data in CSV format
import csv
import os.path  # contains functions for pathnames


class Patient:
    """Class to represent a Patient"""
    # Patient class constructor:

    def __init__(self, name, year, covid, vaccine):
        self.name = name
        self.year = year
        self.covid = covid
        self.vaccine = vaccine

    # Returns information about a patient:
    def __str__(self):
        return self.name + "\t" + str(self.year) + "\t" + str(self.covid) + "\t" + str(self.vaccine)


class HealthCenter(DList):
    """Class to represent a Health Center"""

    def __init__(self, filetsv=None):
        # Function super() allows us to work with Multiple Inheritance, allowing us to use functionality from already implemented classes:
        super(HealthCenter, self).__init__()

        if filetsv is None or not os.path.isfile(filetsv):
            self.name = ""

        else:
            print("loading the data for the health center from the file ", filetsv)

            # Read information from file:
            self.name = filetsv.replace(".tsv", "")
            tsv_file = open(filetsv)
            read_tsv = csv.reader(tsv_file, delimiter="\t")

            # Import row-wise information from file:
            for row in read_tsv:
                name = row[0]
                year = int(row[1])
                covid = False

                if int(row[2]) == 1:
                    covid = True

                vaccine = int(row[3])
                # Add Patient to HealthCenter linked list:
                self.addLast(Patient(name, year, covid, vaccine))
            tsv_file.close()  # Added in order to avoid warnings, asked teachers permission

    def addPatient(self, patient):
        """Add a new patient in alphabetical order"""
        # If list "self" is empty, set Patient as head of Self:
        if self.isEmpty():
            self.addFirst(patient)
            return True

        control = self._head  # Assign head of List to variable in order to travel list

        # Use lexigrophic comparison with attribute .name to add Patient correctly:
        # Evaluate if Patient belongs to head of List:
        if patient.name < control.elem.name:
            self.addFirst(patient)
            return True

        # Use While loop to travel List and set variable control right after Patient is to be added:
        while patient.name >= control.elem.name and control.next != None:
            # If patient is repeated, i.e. attribute name matches, the function ends:
            if patient.name == control.elem.name:
                return False
            control = control.next

        # Evaluate if list is completly travelled, to set Patient as tail of list:
        if control.next == None:
            self.addLast(patient)
            return True

        # With variable control in right position, add node with Patient prior:
        newnode = DNode(patient)
        auxiliar = control.prev
        auxiliar.next = newnode
        newnode.next = control
        control.prev = newnode
        self._size += 1
        return True

    def searchPatients(self, year, covid=None, vaccine=None):
        """Search for patients on the list """
        result = HealthCenter()
        test = self._head  # Assign head of List to variable in order to travel list
        # Use While loop and variable test to travel List (i.e. alphabetically) and evaluate each list node:
        while test != None:
            # If node atrributes .year , .covid and .vaccine match function parameters, add node to list result:
            if test.elem.year <= year and (test.elem.covid == covid or covid == None) and (test.elem.vaccine == vaccine or vaccine == None):
                result.addLast(test.elem)
            test = test.next
        return result

    def statistics(self):
        """Function that returns different statistics about our list """
        # Evaluate if list is empty, to return error code:
        if self.isEmpty():
            print("Error! List is empty")
            return False

        # Declare variables needed to compute output values:
        elder = 0  # Older than 70 years
        cov_pat = 0  # Passed covid
        elder_cov_pat = 0  # Elder and passed covid
        no_dose_pat = 0  # No dose received
        eld_no_dose_pat = 0  # Elder and no dose received
        first_dose_pat = 0  # First dose received
        second_dose_pat = 0  # Second dose received
        total = len(self)  # Number of total patients

        control = self._head  # Assign head of List to variable in order to travel list
        # Use While loop and variable control to travel list nodes. Evaluate each node to assign the total number of patients matching the specific conditions to their respective variable:
        while control != None:
            if control.elem.year < 1951:
                elder += 1
            if control.elem.covid == True:
                cov_pat += 1
            if control.elem.covid == True and control.elem.year < 1951:
                elder_cov_pat += 1
            if control.elem.vaccine == 0:
                no_dose_pat += 1
            if control.elem.vaccine == 0 and control.elem.year < 1951:
                eld_no_dose_pat += 1
            if control.elem.vaccine == 1:
                first_dose_pat += 1
            if control.elem.vaccine == 2:
                second_dose_pat += 1
            control = control.next

        # If variable elder equals 0, set value to one to avoid arithmetic exception in the computation of percentages:
        if elder == 0:
            print("There are no people older than 70 years. ")
            elder = 1

        # Declare percentage variables and compute respective value. Use function round() to get percentages with 2 digits:
        per_cov_pat = round(cov_pat / total, 2)
        per_elder_cov_pat = round(elder_cov_pat / elder, 2)
        per_no_dose_pat = round(no_dose_pat / total, 2)
        per_eld_no_dose_pat = round(eld_no_dose_pat / elder, 2)
        per_first_dose_pat = round(first_dose_pat / total, 2)
        per_second_dose_pat = round(second_dose_pat / total, 2)

        return per_cov_pat, per_elder_cov_pat, per_no_dose_pat, per_eld_no_dose_pat, per_first_dose_pat, per_second_dose_pat

    def merge(self, other):
        """Returns new list that includes patients of list + other list """
        result = HealthCenter()
        # Assign heads of Lists to variables in order to travel lists:
        test = other._head
        control = self._head

        # Use While loop and variables test and control to travel list (i.e. alphabetically) until the tail of both lists is passed. Use lexicographic comparison between variables to contruct list result alphabetically:
        while test != None or control != None:
            # If tail of other is passed, travel through self. As there is no possible duplicates left, add nodes to result list:
            if test == None:
                result.addLast(control.elem)
                control = control.next
            # If tail of self is passed, travel through other. As there is no possible duplicates left, add nodes to result list:
            elif control == None:
                result.addLast(test.elem)
                test = test.next
            # If there is a duplicate (i.e. atribute .name matches), node control (belonging to self) is added to result and both list are travelled:
            elif control.elem.name == test.elem.name:
                result.addLast(control.elem)
                control = control.next
                test = test.next
            # Node with alphabeticall priority is added to the list and its respective list is travelled:
            elif control.elem.name < test.elem.name:
                result.addLast(control.elem)
                control = control.next
            elif control.elem.name > test.elem.name:
                result.addLast(test.elem)
                test = test.next
        return result

    def minus(self, other):
        """Returns current list without the patients that also belong to other list"""
        result = HealthCenter()
        # Assign heads of Lists to variables in order to travel lists:
        test = other._head
        control = self._head
        # Use While loop and variables test and control to travel list until the tail of list self is passed. Use lexicographic comparison between variables to contruct list result alphabetically:
        while control != None:
            # If tail of other is passed, travel through self adding its nodes to result, as there are no possible matches between lists:
            if test == None:
                result.addLast(control.elem)
                control = control.next
            # If there is a duplicate (i.e. atribute .name matches), both list are travelled without any adittion to result (i.e. node of self is skipped in result):
            elif control.elem.name == test.elem.name:
                control = control.next
                test = test.next
            # If node from self is alphabetically prior and no duplicates have been found, it is added to result and self is travelled:
            elif control.elem.name < test.elem.name:
                result.addLast(control.elem)
                control = control.next
            # If node from other is alphabetically prior and no duplicates have been found, other is travelled:
            elif control.elem.name > test.elem.name:
                test = test.next
        return result

    def inter(self, other):
        """Returns list with only patients that belong to both health center lists"""
        result = HealthCenter()
        # Assign heads of Lists to variables in order to travel lists:
        control = self._head
        test = other._head
        # Use While loop and variables test and control to travel list until the tail of one of the lists is passed. Use lexicographic comparison between variables to contruct list result alphabetically:
        while test != None and control != None:
            # If patient belongs to both lists (i.e. atribute .name matches), then the respective node (from self) is added to result list. Both lists are travelled:
            if control.elem.name == test.elem.name:
                result.addLast(control.elem)
                control = control.next
                test = test.next
            # Node with alphabeticall priority is chosen and its respective list is travelled:
            elif control.elem.name < test.elem.name:
                control = control.next
            elif control.elem.name > test.elem.name:
                test = test.next
        return result


if __name__ == "__main__":
    gst = HealthCenter("data/LosFrailes.tsv")
    print(gst)

    # Puedes añadir más llamadas a funciones para probarlas
