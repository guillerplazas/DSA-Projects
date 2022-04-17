# DSA-Projects

Class project developed to manage a network of hospitals using the different python classes and data structures.<br/>

### Phase 1:<br/>
The objective of this phase is to obtain information on the status of the Covid-19 
vaccination campaign in the health centers.

The health system stores detailed information about each patient. The following information is stored (see Patient class):<br/>
* name: Surname and Name<br/>
* year: Birth year<br/>
* covid: True to indicate if the covid has been passed and False otherwise<br/>
* vaccine: Whether or not you have been vaccinated (0 to indicate that you 
have not been vaccinated, 1 to indicate that you have received the first dose 
and 2 to indicate that you have received the second dose)<br/>

Following functions have been implemented:<br/>
* **addPatient**: receives a patient and adds he/she to the list of  patients in the health center. The list is sorted alphabetically. The patient is only added if he/she is not stored in the patient list. The complexity of the method is linear.<br/>

* **searchPatients**: receives the following parameters: <br/>
    * year (searches for all patients born in that year or previously).
    * covid: By default None: all patients will be searched, whether or not they have suffered the covid. If the value is True, function searches for patients 
who have suffered the covid. If the value is False, it searches for patients who have not suffered the covid.
    * vaccine: By default None: searches for all patients, whether they have received any dose or not. If the 
value is 0, the function searches for patients who 
have not received any dose. If the value is 1, the function searches 
for patients who have received only one dose. If the value is 2, the 
function searches for patients who have received two doses.<br/>
   * The function returns a new center whose patient list meets the search 
criteria defined by the input arguments of the function. The complexity of the 
method is linear. 



A unittest is provided to check the correct functioning.

