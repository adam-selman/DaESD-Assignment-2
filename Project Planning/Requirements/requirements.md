# 1. SmartCare System Requirements

- [1. SmartCare System Requirements](#1-smartcare-system-requirements)
- [2. Requirements from Specification](#2-requirements-from-specification)
  - [2.1. User Roles and Access Control](#21-user-roles-and-access-control)
    - [2.1.1. Functional Requirements](#211-functional-requirements)
    - [2.1.2. Non-functional Requirements](#212-non-functional-requirements)
  - [2.2. Scheduling, Work Scheme and Prescriptions](#22-scheduling-work-scheme-and-prescriptions)
    - [2.2.1. Functional Requirements](#221-functional-requirements)
    - [2.2.2. Non-functional Requirements](#222-non-functional-requirements)
  - [2.3. Billing and Invoicing](#23-billing-and-invoicing)
    - [2.3.1. Functional Requirements](#231-functional-requirements)
    - [2.3.2. Non-functional Requirements](#232-non-functional-requirements)
  - [2.4. System Collaboration](#24-system-collaboration)
      - [2.4.0.1. Functional Requirements](#2401-functional-requirements)
      - [2.4.0.2. Non-functional Requirements](#2402-non-functional-requirements)
  - [2.5. Pages](#25-pages)
    - [2.5.1. Functional Requirements](#251-functional-requirements)
    - [2.5.2. Non-functional Requirements](#252-non-functional-requirements)
  - [2.6. Full Requirements List](#26-full-requirements-list)
    - [2.6.1. Functional Requirements](#261-functional-requirements)
    - [2.6.2. Non-functional Requirements](#262-non-functional-requirements)
- [3. References](#3-references)


# 2. Requirements from Specification

The requirements below are separated into functional and non-functional requirements. Each shall be given a unique identifier. Functional requirements in the form FR.XXX.Y where FR indicates a functional requirement, XXX is replaced with a number and Y is replaced by a letter from the MoSCoW acronym. Non-functional requirements shall take the same form, using NFR to signify a nonfunctional requirement. The easy approach to requirements syntax (EARS) (Mavin et al., 2009) shall be followed for requirement descriptions to ensure they are clear and concise.

## 2.1. User Roles and Access Control

### 2.1.1. Functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| FR.001.M   | The data storage system shall track if a user is a Doctor  | M  |
| FR.005.M   | If a user is a Doctor, then the data storage system shall track if they work full time or part time.  | M |
| FR.010.M   | The data storage system shall track if a user is a Nurse  | M |
| FR.015.M   | The data storage system shall track if a user is a Patient  | M |
| FR.020.M   | The data storage system shall track if a user is an Admin  | M |
| FR.025.M   | When a user is successfully authenticated the system shall re-direct them to their designated dhasboard. |M |
| FR.030.M   | If a user has not been authenticated, then the system shall prevent them from accessing the application. |M  |
| FR.035.M   | If a user has not been authenticated and they attempt to access the site, then the system shall re-direct them to the login/registration page. | M |
| FR.040.M   | The system shall allow new users to register their details to create an account. | M |
| FR.045.M   | When creating a new user account address information shall be retrieved using an external web service. | M |
| FR.050.M   | The system shall allow users to request their account be deleted. |M  |
| FR.055.M   | The system shall allow the user to logout. | M |
| FR.060.M   | When a user has been inactive for 5 minutes the system shall log them out.  | M |
| FR.065.M   | When a user attempts to access a dashboard their right to access it shall be authenticated.   | M |
| FR.070.M   | If the user is an admin, then the system shall allow them to register new doctor users  | M |
| FR.075.M   | If the user is an admin, then the system shall allow them to register new nurse users  | M|
| FR.080.M   | If the user is an admin, then the system shall allow them to perform create operations on stored records.  | M|
| FR.085.M   | If the user is an admin, then the system shall allow them to perform read operations on stored records.  | M|
| FR.090.M   | If the user is an admin, then the system shall allow them to perform update operations on stored records.  | M|
| FR.095.M   | If the user is an admin, then the system shall allow them to perform delete operations on stored records.  | M|

### 2.1.2. Non-functional Requirements
| Requirement ID | Description | MoSCoW |
|------|------|------|
| NFR.001.S   | The user authentication and login process shall take less than 3 seconds to complete  | S  |
| NFR.005.S   | The user authentication and login process shall use secure protocols | S  |
| NFR.010.S   | User passwords shall be stored as a password hash.  | S  |
| NFR.015.S   | Role based access control checks shall take less than 2 seconds to complete  | S  |

## 2.2. Scheduling, Work Scheme and Prescriptions

### 2.2.1. Functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| FR.100.M   | The system shall return a timetable of appointments for doctor users.   | M  |
| FR.110.M   | The system shall return a timetable of appointments for nurse users.   | M  |
| FR.115.M   | The system shall allow doctor and nurse users to mark an appointment as complete.   | M  |
| FR.120.M   | The system shall allow doctor and nurse users to issue a prescription after an appointment is marked as complete.   | M  |
| FR.125.M   | The system shall allow doctor and nurse users to forward a patient to a hospital after an appointment is marked as complete.   | M  |
| FR.130.M   | The system shall provide an appointment booking form for patient users.   | M  |
| FR.135.M   | The system shall integrate appointments with an external calendar service.   | M  |
| FR.140.M   | The system shall allow patient users to request prescrition re-issuance.   | M  |
| FR.145.M   | The system shall create a weekly work scheme that ensures there is 1 doctor and 1 nurse on Monday and Friday.   | M  |
| FR.150.M   | The system shall create a weekly work scheme that ensures there are 2 doctors on Tuesday, Wednesday, Thursday, Saturday and Sunday.   | M  |
| FR.155.M   | The system shall return a timetable of appointments for nurse users.   | M  |

### 2.2.2. Non-functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| NFR.020.S   | The system shall allow nurses and doctors view patient timetables 24 hours a day, 7 days a week.   | S  |
| NFR.025.S   | The system shall allow patients to view their booked appointments 24 hours a day, 7 days a week.   | S  |
| NFR.030.S   | The system shall allow patients to book appointments 24 hours a day, 7 days a week.   | S  |
| NFR.035.S   | The system shall allow patients to request prescription re-issuance 24 hours a day, 7 days a week.   | S  |

## 2.3. Billing and Invoicing

### 2.3.1. Functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| FR.160.M   | The system shall calculate appointment cost based on the duration of the appointment.   | M  |
| FR.165.M   | The system shall calculate appointment cost based on whether a doctor or nurse attended.   | M  |
| FR.170.M   | The system shall automatically produce an invoice after each appointment is marked as completed.   | M  |
| FR.175.M   | The system shall allow invoices to be exported in a pdf format.   | M  |
| FR.180.M   | The system shall allow invoices to be sent directly to the NHS.   | M  |
| FR.185.M   | The system shall allow invoices to be sent directly to private healthcare providers.   | M  |
| FR.190.M   | The system shall allow admin users to produce a report containing patient turnover, private payments and payments sent to the NHS.   | M  |

### 2.3.2. Non-functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| NFR.040.S   | Invoices shall be transferred to external services using secure protocols. | S  |


## 2.4. System Collaboration

#### 2.4.0.1. Functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| FR.195.M   | The system shall allow nurse operations to be forward to other GP practices.   | M  |
| FR.200.M   | The system shall facilitate collaboration with other GP practices via APIs.   | M  |

#### 2.4.0.2. Non-functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| NFR.045.S   | Invoices shall facilitate secure communication with to other GP practices using secure protocols. | S  |
| NFR.050.S   | Invoices shall facilitate secure communication with to other GP practices 24 hours a day, 7 days a week. | S  |

## 2.5. Pages

### 2.5.1. Functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| FR.205.M   | The system shall have a main home page.   | M  |
| FR.210.M   | The system shall have a login page.   | M  |
| FR.215.M   | The system shall have a user registration page.   | M  |
| FR.220.M   | The system shall have a doctor dashboard page.   | M  |
| FR.225.M   | The system shall have a nurse dashboard page.   | M  |
| FR.230.M   | The system shall have a patient dashboard page.   | M  |
| FR.235.M   | The system shall have an admin dashboard page.   | M  |

### 2.5.2. Non-functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| NFR.055.S   | The system shall provide a user interface that allows the user to reach any page within 5 clicks. | S  |
| NFR.060.S   | The system shall allow a user to access their dashboard from any page on the site in one click. | S  |

## 2.6. Full Requirements List

### 2.6.1. Functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| FR.001.M   | The data storage system shall track if a user is a Doctor  | M  |
| FR.005.M   | If a user is a Doctor, then the data storage system shall track if they work full time or part time.  | M |
| FR.010.M   | The data storage system shall track if a user is a Nurse  | M |
| FR.015.M   | The data storage system shall track if a user is a Patient  | M |
| FR.020.M   | The data storage system shall track if a user is an Admin  | M |
| FR.025.M   | When a user is successfully authenticated the system shall re-direct them to their designated dhasboard. |M |
| FR.030.M   | If a user has not been authenticated, then the system shall prevent them from accessing the application. |M  |
| FR.035.M   | If a user has not been authenticated and they attempt to access the site, then the system shall re-direct them to the login/registration page. | M |
| FR.040.M   | The system shall allow new users to register their details to create an account. | M |
| FR.045.M   | When creating a new user account address information shall be retrieved using an external web service. | M |
| FR.050.M   | The system shall allow users to request their account be deleted. |M  |
| FR.055.M   | The system shall allow the user to logout. | M |
| FR.060.M   | When a user has been inactive for 5 minutes the system shall log them out.  | M |
| FR.065.M   | When a user attempts to access a dashboard their right to access it shall be authenticated.   | M |
| FR.070.M   | If the user is an admin, then the system shall allow them to register new doctor users  | M |
| FR.075.M   | If the user is an admin, then the system shall allow them to register new nurse users  | M|
| FR.080.M   | If the user is an admin, then the system shall allow them to perform create operations on stored records.  | M|
| FR.085.M   | If the user is an admin, then the system shall allow them to perform read operations on stored records.  | M|
| FR.090.M   | If the user is an admin, then the system shall allow them to perform update operations on stored records.  | M|
| FR.095.M   | If the user is an admin, then the system shall allow them to perform delete operations on stored records.  | M|
| FR.100.M   | The system shall return a timetable of appointments for doctor users.   | M  |
| FR.110.M   | The system shall return a timetable of appointments for nurse users.   | M  |
| FR.115.M   | The system shall allow doctor and nurse users to mark an appointment as complete.   | M  |
| FR.120.M   | The system shall allow doctor and nurse users to issue a prescription after an appointment is marked as complete.   | M  |
| FR.125.M   | The system shall allow doctor and nurse users to forward a patient to a hospital after an appointment is marked as complete.   | M  |
| FR.130.M   | The system shall provide an appointment booking form for patient users.   | M  |
| FR.135.M   | The system shall integrate appointments with an external calendar service.   | M  |
| FR.140.M   | The system shall allow patient users to request prescrition re-issuance.   | M  |
| FR.145.M   | The system shall create a weekly work scheme that ensures there is 1 doctor and 1 nurse on Monday and Friday.   | M  |
| FR.150.M   | The system shall create a weekly work scheme that ensures there are 2 doctors on Tuesday, Wednesday, Thursday, Saturday and Sunday.   | M  |
| FR.155.M   | The system shall return a timetable of appointments for nurse users.   | M  |
| FR.160.M   | The system shall calculate appointment cost based on the duration of the appointment.   | M  |
| FR.165.M   | The system shall calculate appointment cost based on whether a doctor or nurse attended.   | M  |
| FR.170.M   | The system shall automatically produce an invoice after each appointment is marked as completed.   | M  |
| FR.175.M   | The system shall allow invoices to be exported in a pdf format.   | M  |
| FR.180.M   | The system shall allow invoices to be sent directly to the NHS.   | M  |
| FR.185.M   | The system shall allow invoices to be sent directly to private healthcare providers.   | M  |
| FR.190.M   | The system shall allow admin users to produce a report containing patient turnover, private payments and payments sent to the NHS.   | M  |
| FR.195.M   | The system shall allow nurse operations to be forward to other GP practices.   | M  |
| FR.200.M   | The system shall facilitate collaboration with other GP practices via APIs.   | M  |
| FR.205.M   | The system shall have a main home page.   | M  |
| FR.210.M   | The system shall have a login page.   | M  |
| FR.215.M   | The system shall have a user registration page.   | M  |
| FR.220.M   | The system shall have a doctor dashboard page.   | M  |
| FR.225.M   | The system shall have a nurse dashboard page.   | M  |
| FR.230.M   | The system shall have a patient dashboard page.   | M  |
| FR.235.M   | The system shall have an admin dashboard page.   | M  |

### 2.6.2. Non-functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| NFR.001.S   | The user authentication and login process shall take less than 3 seconds to complete  | S  |
| NFR.005.S   | The user authentication and login process shall use secure protocols | S  |
| NFR.010.S   | User passwords shall be stored as a password hash.  | S  |
| NFR.015.S   | Role based access control checks shall take less than 2 seconds to complete  | S  |
| NFR.020.S   | The system shall allow nurses and doctors view patient timetables 24 hours a day, 7 days a week.   | S  |
| NFR.025.S   | The system shall allow patients to view their booked appointments 24 hours a day, 7 days a week.   | S  |
| NFR.030.S   | The system shall allow patients to book appointments 24 hours a day, 7 days a week.   | S  |
| NFR.035.S   | The system shall allow patients to request prescription re-issuance 24 hours a day, 7 days a week.   | S  |
| NFR.040.S   | Invoices shall be transferred to external services using secure protocols. | S  |
| NFR.045.S   | Invoices shall facilitate secure communication with to other GP practices using secure protocols. | S  |
| NFR.050.S   | Invoices shall facilitate secure communication with to other GP practices 24 hours a day, 7 days a week. | S  |
| NFR.055.S   | The system shall provide a user interface that allows the user to reach anypage within 5 clicks. | S  |
| NFR.060.S   | The system shall allow a user to access their dashboard from any page on the site in one click. | S  |



# 3. References

Mavin, A., Wilkinson, P., Harwood, A. and Novak, M. (2009) Easy Approach to Requirements Syntax (EARS). In: 2009 17th IEEE International Requirements Engineering Conference [online]. 2009 17th IEEE International Requirements Engineering Conference (RE). Atlanta, Georgia, USA, IEEE, pp. 317–322. Available from: http://ieeexplore.ieee.org/document/5328509/ [Accessed 7 February 2024].