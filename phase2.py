# -*- coding: utf-8 -*-


from binarysearchtree import BSTNode, BinarySearchTree


import csv  # read files csv, tsv
import os.path  # to work with files and directory https://docs.python.org/3/library/os.path.html
import queue  # package implementes a queueu, https://docs.python.org/3/library/queue.html
import re  # working with regular expressions


def checkFormatHour(time):
    """checks if the time follows the format hh:dd"""
    pattern = re.compile(r'\d{2}:\d{2}')  # busca la palabra foo

    if pattern.match(time):
        data = time.split(':')
        hour = int(data[0])
        minute = int(data[1])
        if hour in range(8, 20) and minute in range(0, 60, 5):
            return True

    return False


# number of all possible appointments for one day
NUM_APPOINTMENTS = 144


class Patient:
    """Class to represent a Patient"""

    def __init__(self, name, year, covid, vaccine, appointment=None):

        self.name = name
        self.year = year
        self.covid = covid
        self.vaccine = vaccine
        self.appointment = appointment  # string with format hour:minute

    def setAppointment(self, time):
        """gets a string with format hour:minute"""
        self.appointment = time

    def __str__(self):
        return self.name+'\t'+str(self.year)+'\t'+str(self.covid)+'\t'+str(self.vaccine)+'\t appointment:'+str(self.appointment)

    def __eq__(self, other):
        return other != None and self.name == other.name


class HealthCenter2(BinarySearchTree):
    """Class to represent a Health Center. This class is a subclass of a binary search tree to
    achive a better temporal complexity of its algorithms for
    searching, inserting o removing a patient (or an appointment)"""

    def __init__(self, filetsv=None, orderByName=True):
        """
        This constructor allows to create an object instance of HealthCenter2.
        It takes two parameters:
        - filetsv: a file csv with the information about the patients whe belong to this health center
        - orderByName: if it is True, it means that the patients should be sorted by their name in the binary search tree,
        however, if is is False, it means that the patients should be sorted according their appointments
        """

        # Call to the constructor of the super class, BinarySearchTree.
        # This constructor only define the root to None
        super(HealthCenter2, self).__init__()
        # Now we
        if filetsv is None or not os.path.isfile(filetsv):
            # If the file does not exist, we create an empty tree (health center without patients)
            self.name = ''
            # print('File does not exist ',filetsv)
        else:
            order = 'by appointment'
            if orderByName:
                order = 'by name'

            # print('\n\nloading patients from {}. The order is {}\n\n'.format(filetsv,order))

            self.name = filetsv[filetsv.rindex('/')+1:].replace('.tsv', '')
            # print('The name of the health center is {}\n\n'.format(self.name))
            # self.name='LosFrailes'

            fichero = open(filetsv)
            lines = csv.reader(fichero, delimiter="\t")

            for row in lines:
                # print(row)
                name = row[0]  # nombre
                year = int(row[1])  # año nacimiento
                covid = False
                if int(row[2]) == 1:  # covid:0 o 1
                    covid = True
                vaccine = int(row[3])  # número de dosis
                try:
                    appointment = row[4]
                    if checkFormatHour(appointment) == False:
                        # print(appointment, ' is not a right time (hh:minute)')
                        appointment = None

                except:
                    appointment = None

                objPatient = Patient(name, year, covid, vaccine, appointment)
                # name is the key, and objPatient the eleme
                if orderByName:
                    self.insert(name, objPatient)
                else:
                    if appointment:
                        self.insert(appointment, objPatient)
                    else:
                        print(
                            objPatient, " was not added because appointment was not valid!!!")

            fichero.close()

    # We use an auxiliary function for recursion. In this case, this auxiliary funtion follows a O(n) complexity.
    def searchPatients(self, year=2021, covid=None, vaccine=None):
        if self._root is None:  # Handles error cases
            print("No patients have been found. List is empty.")
            return False
        result = HealthCenter2()
        for level in range(1, self.height()+2):  # Level order traversal
            self._searchPatients(self._root, level, result,
                                 year, covid, vaccine)
        return result

    # We define the recursive method. The function follows an O(n^2)
    def _searchPatients(self, node, level, result, year, covid, vaccine):
        if node is None:    # Base case
            return

        # We study the level.
        if level == 1:
            # For efficency: year is evaluarted first (only mandatory input).
            if node.elem.year <= year:
                # Evaluates if data corresponds and adds node to result if correct.
                if (covid == None or node.elem.covid == covid) and (vaccine == None or node.elem.vaccine == vaccine):
                    result.insert(node.key, node.elem)
        # We search all the nodes, as it is asked in the problem. If not, we could find a more efficent traversal.
        elif level > 1:
            self._searchPatients(node.left, level-1,
                                 result, year, covid, vaccine)
            self._searchPatients(node.right, level-1,
                                 result, year, covid, vaccine)
    """ The function search patient follows a time complexity of O(n^2), where n is the number of nodes.
    This is because we evaluate O(n) + O(n-1) + ... + O(1), which leads to O(n^2)"""

    # We use an auxiliary function for recursion:
    def vaccine(self, name, vaccinated):
        """This functions simulates the vaccination of a patient whose
        name is name. It returns True is the patient is vaccinated and False eoc"""
        if self._root is None:  # Handles error cases
            print("Tree is empty.")
            return None
        return self._vaccine(self._root, name, vaccinated)

    # We define the recursive method:
    def _vaccine(self, node, name, vaccinated):

        updated = False  # Boolean variable for code efficency.
        # Evaluates the node containing the input name:
        if node.elem.name == name:
            # For efficency purposes, it first cheks and updates vaccine number on patients allegded to receive it:
            if node.elem.vaccine in range(2):
                node.elem.vaccine += 1
                print("Vaccine status updated.")
                updated = True
            # Then if the patient has received 2 vaccines, it eliminates it and adds it to result:
            if node.elem.vaccine == 2:
                vaccinated.insert(name, node.elem)
                self.remove(node.key)
                if updated is False:
                    print("Patient already received 2 vaccines.")
                return updated  # Variable updated helps to know wether the patient already had 2 vacinnes previosuly or not
            return True

        # Evaluates how the function should travel the tree efficently:
        if node.right and name < node.right.elem.name:
            return self._vaccine(node.left, name, vaccinated)
        elif node.right and name > node.left.elem.name:
            return self._vaccine(node.right, name, vaccinated)
        else:
            print("Patient doesn´t exist.")
            return False
    """ The funtion vaccine follows a time complexity of O(log(n)), as it is similar
    to the structure of a search in a BST."""

    # Auxiliary function is defined, including all exceptions for efficency.
    def makeAppointment(self, name, time, schedule):
        """This functions makes an appointment
        for the patient whose name is name. It functions returns True is the appointment
        is created and False eoc """
        # Returns node with Complexity O(log(n))
        patient = self.find(name)
        # Studies exception cases:
        if patient is None:
            print("Patient not found in current list")
            return False
        if patient.elem.vaccine == 2:
            print("Patient", patient.elem.name, " has already vaccinated.")
            return False
        if checkFormatHour(time) == False:
            print("Time not correct. Must be a string with format “hh:mm” ")
            return False
        if schedule._root is None:
            print("Error! Original list is empty.")
            return False
        if schedule.size() == 0:
            patient.elem.appointment = time
            schedule._root = BSTNode(time, patient.elem.copy())
            return True
        if schedule.size() >= NUM_APPOINTMENTS:
            print("No more appointments free for today.")
            return False
        return self._makeAppointment(schedule._root, patient, time, schedule)

    # Recursive method is applied. Two variables will be used (rightcap, leftcap) in order to travel efficently:
    # Complexity is O(log(n)+8)
    def _makeAppointment(self, node, patient, time, schedule, rightcap="21:00", leftcap="08:00"):
        # 3 Base cases for travelling the tree. Fisrt one is  key is smaller than node:
        if time < node.key:
            # If left child exists we travel through it:
            if node.left is not None:
                rightcap = min(node.key, rightcap)  # Adjust value of rightcap.
                return self._makeAppointment(node.left, patient, time, schedule, rightcap, leftcap)
            # If it doesn´t, we add
            else:
                patient.elem.appointment = time
                # Copy elements of node and declare new node
                node.left = BSTNode(time, patient.elem)
                node.left.parent = node
                return True

        # 2nd Base Case (same principle as previous):
        if time > node.key:
            if node.right is not None:
                leftcap = max(node.key, leftcap)
                return self._makeAppointment(node.right, patient, time, schedule, rightcap, leftcap)
            else:
                patient.elem.appointment = time
                node.right = BSTNode(time, patient.elem)
                node.right.parent = node
                return True

        # 3rd Base Case: The key and node are equal. Then we first prioritize looking for previous time slot:
        if time == node.key:
            # First evaluate case error: That is if time is 08:00:
            if prevTime(time) is None:  # prevTime() developed in order to find turns correctly
                return self._makeAppointment(node.right, patient, postTime(time), schedule, rightcap, leftcap)

            # If previous time is smaller than leftcap, it means that no previous value has previous time slot:
            elif prevTime(time) > leftcap:
                if node.left is not None:
                    rightcap = min(node.key, rightcap)
                    return self._makeAppointment(node.left, patient, prevTime(time), schedule, rightcap, leftcap)
                else:
                    patient.elem.appointment = prevTime(time)
                    node.left = BSTNode(prevTime(time), patient.elem)
                    node.left.parent = node
                    return True

            # If conditions don´t apply, study case for posterior time slot (with same principle):
            if postTime(time) is None:
                return self._makeAppointment(node.right, patient, prevTime(time), schedule, rightcap, leftcap)
            elif postTime(time) < rightcap:
                if node.right is not None:
                    leftcap = max(node.key, leftcap)
                    return self._makeAppointment(node.right, patient, postTime(time), schedule, rightcap, leftcap)
                else:
                    patient.elem.appointment = postTime(time)
                    node.right = BSTNode(postTime(time), patient.elem)
                    node.right.parent = node
                    return True
    """ The function make appointment has a complexity of O(log(n)). As it has in the auxiliary formula a search
    with complexity O(log(n)) and in the recursive case other O(log(n)). We know O(log(n))+O(log(n))=O(log(n)) """


# Time funtions made to handle the appointments:
def prevTime(time):
    pattern = re.compile(r'\d{2}:\d{2}')

    if pattern.match(time):
        data = time.split(':')
        hour = int(data[0])
        minute = int(data[1])

        if minute == 0:
            if hour == 8:
                return None
            hour = hour-1
            minute = 55
        else:
            minute = minute-5

        time = [hour, minute]
        time = ["%02d" % x for x in time]

        data = ':'.join(time)
        return data


def postTime(time):
    pattern = re.compile(r'\d{2}:\d{2}')

    if pattern.match(time):
        data = time.split(':')
        hour = int(data[0])
        minute = int(data[1])
        if minute == 0:
            if hour == 21:
                return None
        if minute == 55:
            hour = hour+1
            minute = 0
        else:
            minute = minute+5

        time = [hour, minute]
        time = ["%02d" % x for x in time]

        data = ':'.join(time)
        return data


if __name__ == '__main__':

    """
    # Testing the constructor. Creating a health center where patients are sorted by name
    o = HealthCenter2('data/LosFrailes2.tsv')
    o.draw()
    print()
    pat = Patient()
    newpat = pat.copy()


    print('Patients who were born in or before than 2021, had covid and did not get any vaccine')
    result = o.searchPatients(1990, True, 0)
    result.draw()
    print()

    print('Patients who were born in or before than 1990, did not have covid and did not get any vaccine')
    result = o.searchPatients(1990, False, 0)
    result.draw()
    print()

    print('Patients who were born in or before than 1990 and got one dosage')
    result = o.searchPatients(1990, None, 1)
    result.draw()
    print()

    print('Patients who were born in or before than 1950 and had covid')
    result = o.searchPatients(1990, True, None)
    result.draw()
    print()

    # Testing the constructor. Creating a health center where patients are sorted by name

    # when False is used -> list organised by time
    print("DRAW SCHECH")
    schedule = HealthCenter2('data/LosFrailesCitas.tsv', False)
    schedule.draw(False)
    print()
    print("Expected")
    schedule_exp = HealthCenter2(
        'data/LosFracilesCitasLosada13.tsv', False)
    schedule_exp.draw(False)

    print("DRAW II")
    o.makeAppointment("Perez", "09:00", schedule)
    schedule.draw(False)
    print()

    print(prevTime("08.00"))

    o.makeAppointment("Losada", "19:55", schedule)
    o.makeAppointment("Jaen", "16:00", schedule)
    o.makeAppointment("Perez", "16:00", schedule)
    o.makeAppointment("Jaen", "16:00", schedule)

    o.makeAppointment("Losada", "15:45", schedule)
    o.makeAppointment("Jaen", "08:00", schedule)

    o.makeAppointment("Abad", "08:00", schedule)
    o.makeAppointment("Omar", "15:45", schedule)
    o.makeAppointment("Jaen", "08:05", schedule)

    schedule.draw(False)
    time = "00:00"
    print("\n", time)
    print(postTime(time))

    vaccinated=HealthCenter2('data/vaccinated.tsv')
    vaccinated.draw(False)

    name='Ainoza'  #doest no exist
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)

    name='Abad'   #0 dosages
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)



    name='Font' #with one dosage
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)

    name='Omar' #with two dosage
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)"""
