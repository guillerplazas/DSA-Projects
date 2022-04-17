# DSA-Projects

Class project developed to manage a network of hospitals using the different python classes and data structures.<br/>

### Phase 1:<br/>
The objective of this phase is to obtain information on the status of the Covid-19 
vaccination campaign in the health centers.

The health system stores detailed information about each patient. The following information is stored (see Patient class):<br/>
* name: Surname and Name<br/>
* year: Birth year<br/>
* covid: True to indicate if the covid has been passed and False otherwise<br/>
* Number of vaccine doses: from 0 to 3<br/>

Following functions have been implemented:<br/>
* **addPatient**: receives a patient and adds he/she to the list of  patients in the health center. The list is sorted alphabetically. The patient is only added if he/she is not stored in the patient list. The complexity of the method is linear.<br/>

* **searchPatients**: receives the following parameters: <br/>
    * year (searches for all patients born in that year or previously).
    * covid: By default None: all patients will be searched, whether or not they have suffered the covid. If the value is True, function searches for patients 
who have suffered the covid. If the value is False, it searches for patients who have not suffered the covid.
    * vaccine: By default None: searches for all patients, whether they have received any dose or not. If value is from 0-3, searches patients with that amount of vaccine doses received.<br/>
   * The function returns a new center whose patient list meets the search 
criteria defined by the input arguments of the function. The complexity of the 
method is linear..<br/>

* **statistics**: returns percentage of:.<br/>
    * Patients who have already suffered covid.<br/>
    * Patients older than 70 years (born in 1950 or before) who have already suffered covid.<br/>
    * Patients who have not received any dose..<br/>
    * Patients older than 70 years (born in 1950 or before) who have not received any dose.<br/>
    * Patients who have already received the first dose..<br/>
    * Patients who have already received the second dose..<br/>
    * The complexity of the statistics function is linear.<br/>
    
* **merge**: receives an object of the HealthCenter class, “other”, 
and returns a new health center whose list of patients includes the patients of 
the invoking center, and also the patients of the other center ordered alphabetically and eliminates duplicates. Linear complexity.<br/>

* **minus**: receives an object of the HealthCenter class, “other”, and 
returns a new health center containing the patients of the invoking center
(self), but these patients cannot belong to the “other” center.<br/> 

* **inter**: receives an object of the HealthCenter class, “other”, and 
returns a new health center whose patient list includes only those patients that 
belong to both health centers sorted alphabetically with no duplicates.





A unittest is provided to check the correct functioning.

