# 1. SmartCare System Requirements

- [1. SmartCare System Requirements](#1-smartcare-system-requirements)
  - [1.1. User Stories](#11-user-stories)
    - [1.1.1. Admin](#111-admin)
    - [1.1.2. Doctor](#112-doctor)
    - [1.1.3. Nurse](#113-nurse)
    - [1.1.4. Patient](#114-patient)
    - [1.1.5. All Users](#115-all-users)
  - [1.2. Requirement definitions](#12-requirement-definitions)
    - [1.2.1. User Roles and Access Control](#121-user-roles-and-access-control)
      - [1.2.1.1. Functional Requirements](#1211-functional-requirements)
      - [1.2.1.2. Non-functional Requirements](#1212-non-functional-requirements)
    - [1.2.2. Scheduling, Work Scheme and Prescriptions](#122-scheduling-work-scheme-and-prescriptions)
      - [1.2.2.1. Functional Requirements](#1221-functional-requirements)
      - [1.2.2.2. Non-functional Requirements](#1222-non-functional-requirements)
    - [1.2.3. Patient Appointment Booking](#123-patient-appointment-booking)
    - [1.2.4. Billing and Invoicing](#124-billing-and-invoicing)
      - [1.2.4.1. Functional Requirements](#1241-functional-requirements)
      - [1.2.4.2. Non-functional Requirements](#1242-non-functional-requirements)
    - [1.2.5. System Collaboration](#125-system-collaboration)
      - [1.2.5.1. Functional Requirements](#1251-functional-requirements)
      - [1.2.5.2. Non-functional Requirements](#1252-non-functional-requirements)
    - [1.2.6. Pages](#126-pages)
      - [1.2.6.1. Functional Requirements](#1261-functional-requirements)
      - [1.2.6.2. Non-functional Requirements](#1262-non-functional-requirements)
    - [1.2.7. Full Requirements List](#127-full-requirements-list)
      - [1.2.7.1. Functional Requirements](#1271-functional-requirements)
      - [1.2.7.2. Non-functional Requirements](#1272-non-functional-requirements)
    - [1.2.8. References](#128-references)

## 1.1. User Stories

The following section contains a list of user stories for each of the users that shall be utilising the SmartCare system.

### 1.1.1. Admin

- As an admin, I want to log into the system so I can access all of my management tools.
- As an admin, I want to delete users to comply with GDPR regulations.
- As an admin, I want to edit users information to comply with GDPR regulations.
- As an admin, I want to register new doctors and nurses so I can expand our roster of staff when needed.
- As an admin, I want to edit a doctors to accommodate any changes in their circumstances.
- As an admin, I want to edit nurse information to accommodate any changes in their circumstances.
- As an admin, I want to generate a report containing patient turnover, private payments and payments sent to the NHS so that I can understand how well the business is running.
- As an admin, I want to access comprehensive documentation for system setup, maintenance, and troubleshooting of known issues.

### 1.1.2. Doctor

- As a doctor, I want to log into the system so I can use its features to plan my day.
- As a doctor, I want to view appointment information, such as the patients history and reason for the appointment, so I can prepare for them accordingly.
- As a doctor, I want to see prescriptions that are awaiting approval on my dashboard so that I can quickly and easily approve or decline them.
- As a doctor, I want to see a list of my appointments for today so I can plan what time I have available for administrative work.
- As a doctor, I want to be able to issue prescriptions at the end of appointments so the patient can be treated.
- As a doctor, I want to be able to write up notes at the end of appointments so other healthcare professionals can understand the patients treatment history.
- As a doctor, I want the SmartCare system to automatically generate invoices based on appointment lengths my rate as a doctor so that I can spend my time doing more productive work.

### 1.1.3. Nurse

- As a nurse, I want to view appointment information, such as the patients history and reason for the appointment, so I can prepare for them accordingly.
- As a nurse, I want to see prescriptions that are awaiting approval on my dashboard so that I can quickly and easily approve or decline them.
- As a nurse, I want to see a list of my appointments for today so I can plan what time I have available for administrative work.
- As a nurse, I want the SmartCare system to automatically generate invoices based on appointment lengths and my rate as a nurse so that I can spend my time doing more productive work.

### 1.1.4. Patient

- As a patient, I want to be able to register for an account so that I can book appointments.
- As a patient, I want to book appointments to I can treat my health issues.
- As a patient, I want to be able to see a list of upcoming appointments on my dashboard so that I don't forget when they are.
- As a patient, I want appointment reminders and notifications so that I don't forget to attend.
- As a patient, I want to be able to request a re-issuance of prescriptions so I don't need to spend time seeing a doctor in person.
- As a patient, I want to be able to cancel my appointments so that I can re-arrange them if I become busy or can no longer attend.
- As a patient, I want to be able to attend my appointments virtually so that I can get medical advice without needing to spend time seeing a doctor in person.

### 1.1.5. All Users

- As a user, I want my personal dashboard to be protected by a secure login system.
- As a user, I want to automatically be logged out after inactivity to protect my sensitive information.
- As a user, I want to be able to logout from any page on the website so I can quickly and easily leave at any time.
- As a user, I want to be able to access my dashboard from any page on the website so I access it at my convenience.
- As a user, I want the user interface to be clear so that I can navigate to the page I need quickly and easily.

## 1.2. Requirement definitions

The requirements below are separated into functional and non-functional requirements. Each shall be given a unique identifier. Functional requirements in the form FR.XXX.Y where FR indicates a functional requirement, XXX is replaced with a number and Y is replaced by a letter from the MoSCoW acronym. Non-functional requirements shall take the same form, using NFR to signify a nonfunctional requirement. The easy approach to requirements syntax (EARS) (Mavin et al., 2009) shall be followed for requirement descriptions to ensure they are clear and concise.

### 1.2.1. User Roles and Access Control

#### 1.2.1.1. Functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| FR.001.M   | The data storage system shall track if a user is a Doctor  | M  |
| FR.005.M   | If a user is a Doctor, then the data storage system shall track if they work full time or part time.  | M |
| FR.010.M   | The data storage system shall track if a user is a Nurse  | M |
| FR.015.M   | The data storage system shall track if a user is a Patient  | M |
| FR.020.M   | The data storage system shall track if a user is an Admin  | M |
| FR.025.M   | When a user is successfully authenticated the system shall re-direct them to their designated dashboard. |M |
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

#### 1.2.1.2. Non-functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| NFR.001.S   | The user authentication and login process shall take less than 3 seconds to complete.  | S  |
| NFR.005.S   | The user authentication and login process shall use secure protocols. | S  |
| NFR.010.S   | User passwords shall be stored as a password hash.  | S  |
| NFR.015.S   | Role based access control checks shall take less than 2 seconds to complete.  | S  |

### 1.2.2. Scheduling, Work Scheme and Prescriptions

#### 1.2.2.1. Functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| FR.100.M   | The system shall return a daily timetable of appointments for doctor users.   | M  |
| FR.110.M   | The system shall return a daily timetable of appointments for nurse users.   | M  |
| FR.115.M   | The system shall allow doctor and nurse users to mark an appointment as complete.   | M  |
| FR.120.M   | When marking an appointment as complete the system shall allow the doctor or nurse user to save a description of any notes made during the appointment.   | M  |
| FR.125.M   | The system shall allow doctor and nurse users to issue a prescription after an appointment is marked as complete.   | M  |
| FR.130.M   | The system shall allow doctor and nurse users to forward a patient to a hospital after an appointment is marked as complete.   | M  |
| FR.135.M   | The system shall allow patient users to request prescription re-issuance.   | M  |
| FR.140.M   | The system shall create a weekly work scheme that ensures there is 1 doctor and 1 nurse on Monday and Friday.   | M  |
| FR.145.M   | The system shall create a weekly work scheme that ensures there are 2 doctors on Tuesday, Wednesday, Thursday, Saturday and Sunday.   | M  |

#### 1.2.2.2. Non-functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| NFR.020.S   | The system shall allow nurses and doctors view patient timetables 24 hours a day, 7 days a week.   | S  |
| NFR.025.S   | The system shall allow patients to view their booked appointments 24 hours a day, 7 days a week.   | S  |
| NFR.030.S   | The system shall allow patients to book appointments 24 hours a day, 7 days a week.   | S  |
| NFR.035.S   | The system shall allow patients to request prescription re-issuance 24 hours a day, 7 days a week.   | S  |

### 1.2.3. Patient Appointment Booking

| Requirement ID | Description | MoSCoW |
|------|------|------|
| FR.150.M   | The system shall provide an appointment booking form for patient users.   | M  |
| FR.155.M   | When booking an appointment the system shall ask the user to select a date and time.   | M  |
| FR.160.S   | When booking an appointment the system shall allow the user to provide a short text description of their issue but is not required.   | M  |
| FR.165.M   | The system shall integrate appointments with an external calendar service.   | M  |
| FR.170.M   | The system shall allow patients to cancel a booked appointment.   | M  |
| FR.175.C   | The system shall allow patients to book virtual appointments.   | C  |
| FR.180.C   | The system shall send reminder email notifications to patients.   | C  |

### 1.2.4. Billing and Invoicing

#### 1.2.4.1. Functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| FR.185.M   | The system shall calculate appointment cost based on the duration of the appointment.   | M  |
| FR.190.M   | The system shall calculate appointment cost based on whether a doctor or nurse attended.   | M  |
| FR.195.M   | The system shall automatically produce an invoice after each appointment is marked as completed.   | M  |
| FR.200.C   | The system shall allow invoices to be exported in a pdf format.   | C  |
| FR.205.S   | The system shall allow invoices to be sent directly to the NHS.   | S  |
| FR.210.S   | The system shall allow invoices to be sent directly to private healthcare providers.   | S  |
| FR.215.M   | The system shall allow admin users to produce a report containing patient turnover, private payments and payments sent to the NHS.   | M  |

#### 1.2.4.2. Non-functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| NFR.040.S   | Invoices shall be transferred to external services using secure protocols. | S  |

### 1.2.5. System Collaboration

#### 1.2.5.1. Functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| FR.220.S   | The system shall allow nurse operations to be forward to other GP practices.   | S  |
| FR.225.C   | The system shall facilitate collaboration with other GP practices via APIs.   | C  |

#### 1.2.5.2. Non-functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| NFR.045.S   | Invoices shall facilitate secure communication with to other GP practices using secure protocols. | S  |
| NFR.050.S   | Invoices shall facilitate secure communication with to other GP practices 24 hours a day, 7 days a week. | S  |

### 1.2.6. Pages

#### 1.2.6.1. Functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| FR.230.M   | The system shall have a main home page.   | M  |
| FR.235.M   | The main home page shall display general information about the SmartCare system.   | M  |
| FR.240.M   | If a user is not logged in, then the main home page shall have a login button.   | M  |
| FR.245.M   | If a user is logged in, then all pages shall have a logout button.   | M  |
| FR.250.M   | The system shall have a login page.   | M  |
| FR.255.M   | The system shall have a user registration page.   | M  |
| FR.260.M   | The system shall have a doctor dashboard page.   | M  |
| FR.265.M   | The doctor dashboard shall display a list of prescription re-issuance requests that need approval.   | M  |
| FR.270.M   | The doctor dashboard shall allow doctors to approve a prescription re-issuance requests.   | M  |
| FR.275.M   | The doctor dashboard shall allow doctors to decline a prescription re-issuance requests.   | M  |
| FR.280.C   | If doctor declines a prescription re-issuance request they are given the option to state why.   | C  |
| FR.285.M   | The doctor dashboard shall display a list of appointments assigned to them for the current date including patient information, appointment time and a brief description of the issue.   | M  |
| FR.290.C   | The doctor dashboard shall allow doctors to request days off for holiday or sickness  | C  |
| FR.295.C   | The doctor dashboard shall show a list of shifts that are in need of cover due to holiday or sickness doctors to request days off.   | C  |
| FR.300.M   | The system shall have a nurse dashboard page.   | M  |
| FR.305.M   | The nurse dashboard shall display a list of prescription re-issuance requests that need approval.   | M  |
| FR.310.M   | The nurse dashboard shall display a list of appointments assigned to them for the current date including patient information, appointment time and a brief description of the issue.   | M  |
| FR.315.M   | The system shall have a staff timetable  page.   | M  |
| FR.320.M   | The staff timetable page shall display a working schedule for the current week.   | M  |
| FR.325.M   | The staff timetable page shall display future work week schedules.   | M  |
| FR.330.M   | The system shall have a patient dashboard page.   | M  |
| FR.335.M   | The patient dashboard shall display a list of current prescriptions.   | M  |
| FR.340.M   | The patient dashboard shall display a list of upcoming appointments with the corresponding date and time.   | M  |
| FR.345.M   | The patient dashboard shall display a list of previous appointments including any prescriptions issued.   | M  |
| FR.350.M   | The patient dashboard shall display a list of prescription re-issuance requests that are pending approval.   | M  |
| FR.355.M   | The patient dashboard shall display a list of invoices for appointments and who is responsible for payment.   | M  |
| FR.360.M   | The system shall have an admin dashboard page.   | M  |
| FR.365.M   | The admin dashboard shall allow for the registration of a new doctor user.   | M  |
| FR.370.M   | The admin dashboard shall allow the viewing of a doctor's information.   | M  |
| FR.375.M   | The admin dashboard shall allow for the registration of a new nurse user.   | M  |
| FR.380.M   | The admin dashboard shall allow the viewing of a nurse's information.   | M  |
| FR.385.M   | The admin dashboard shall allow the editing of a patient's personal information including name, email address and home address.   | M  |
| FR.390.M   | The admin dashboard shall allow for the deletion of any existing user.   | M  |

#### 1.2.6.2. Non-functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| NFR.055.S   | The system shall provide a user interface that allows the user to reach any page within 5 clicks. | S  |
| NFR.060.S   | The system shall allow a user to access their dashboard from any page on the site in one click. | S  |
| NFR.065.S   | The system shall allow a user to logout from any page on the site in one click. | S  |

### 1.2.7. Full Requirements List

#### 1.2.7.1. Functional Requirements

| Requirement ID | Description | MoSCoW |
|------|------|------|
| FR.001.M   | The data storage system shall track if a user is a Doctor  | M  |
| FR.005.M   | If a user is a Doctor, then the data storage system shall track if they work full time or part time.  | M |
| FR.010.M   | The data storage system shall track if a user is a Nurse  | M |
| FR.015.M   | The data storage system shall track if a user is a Patient  | M |
| FR.020.M   | The data storage system shall track if a user is an Admin  | M |
| FR.025.M   | When a user is successfully authenticated the system shall re-direct them to their designated dashboard. |M |
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
| FR.100.M   | The system shall return a daily timetable of appointments for doctor users.   | M  |
| FR.110.M   | The system shall return a daily timetable of appointments for nurse users.   | M  |
| FR.115.M   | The system shall allow doctor and nurse users to mark an appointment as complete.   | M  |
| FR.120.M   | When marking an appointment as complete the system shall allow the doctor or nurse user to save a description of any notes made during the appointment.   | M  |
| FR.125.M   | The system shall allow doctor and nurse users to issue a prescription after an appointment is marked as complete.   | M  |
| FR.130.M   | The system shall allow doctor and nurse users to forward a patient to a hospital after an appointment is marked as complete.   | M  |
| FR.135.M   | The system shall allow patient users to request prescription re-issuance.   | M  |
| FR.140.M   | The system shall create a weekly work scheme that ensures there is 1 doctor and 1 nurse on Monday and Friday.   | M  |
| FR.145.M   | The system shall create a weekly work scheme that ensures there are 2 doctors on Tuesday, Wednesday, Thursday, Saturday and Sunday.   | M  |
| FR.150.M   | The system shall provide an appointment booking form for patient users.   | M  |
| FR.155.M   | When booking an appointment the system shall ask the user to select a date and time.   | M  |
| FR.160.S   | When booking an appointment the system shall allow the user to provide a short text description of their issue but is not required.   | M  |
| FR.165.M   | The system shall integrate appointments with an external calendar service.   | M  |
| FR.170.M   | The system shall allow patients to cancel a booked appointment.   | M  |
| FR.175.C   | The system shall allow patients to book virtual appointments.   | C  |
| FR.180.C   | The system shall send reminder email notifications to patients.   | C  |
| FR.185.M   | The system shall calculate appointment cost based on the duration of the appointment.   | M  |
| FR.190.M   | The system shall calculate appointment cost based on whether a doctor or nurse attended.   | M  |
| FR.195.M   | The system shall automatically produce an invoice after each appointment is marked as completed.   | M  |
| FR.200.C   | The system shall allow invoices to be exported in a pdf format.   | C  |
| FR.205.C   | The system shall allow invoices to be sent directly to the NHS.   | C  |
| FR.210.M   | The system shall allow invoices to be sent directly to private healthcare providers.   | M  |
| FR.215.M   | The system shall allow admin users to produce a report containing patient turnover, private payments and payments sent to the NHS.   | M  |
| FR.220.S   | The system shall allow nurse operations to be forward to other GP practices.   | S  |
| FR.225.C   | The system shall facilitate collaboration with other GP practices via APIs.   | C  |
| FR.230.M   | The system shall have a main home page.   | M  |
| FR.235.M   | The main home page shall display general information about the SmartCare system.   | M  |
| FR.240.M   | If a user is not logged in, then the main home page shall have a login button.   | M  |
| FR.245.M   | If a user is logged in, then all pages shall have a logout button.   | M  |
| FR.250.M   | The system shall have a login page.   | M  |
| FR.255.M   | The system shall have a user registration page.   | M  |
| FR.260.M   | The system shall have a doctor dashboard page.   | M  |
| FR.265.M   | The doctor dashboard shall display a list of prescription re-issuance requests that need approval.   | M  |
| FR.270.M   | The doctor dashboard shall allow doctors to approve a prescription re-issuance requests.   | M  |
| FR.275.M   | The doctor dashboard shall allow doctors to decline a prescription re-issuance requests.   | M  |
| FR.280.C   | If doctor declines a prescription re-issuance request they are given the option to state why.   | C  |
| FR.285.M   | The doctor dashboard shall display a list of appointments assigned to them for the current date including patient information, appointment time and a brief description of the issue.   | M  |
| FR.290.C   | The doctor dashboard shall allow doctors to request days off for holiday or sickness  | C  |
| FR.295.C   | The doctor dashboard shall show a list of shifts that are in need of cover due to holiday or sickness doctors to request days off.   | C  |
| FR.300.M   | The system shall have a nurse dashboard page.   | M  |
| FR.305.M   | The nurse dashboard shall display a list of prescription re-issuance requests that need approval.   | M  |
| FR.310.M   | The nurse dashboard shall display a list of appointments assigned to them for the current date including patient information, appointment time and a brief description of the issue.   | M  |
| FR.315.M   | The system shall have a staff timetable  page.   | M  |
| FR.320.M   | The staff timetable page shall display a working schedule for the current week.   | M  |
| FR.325.S   | The staff timetable page shall display future work week schedules.   | S  |
| FR.330.M   | The system shall have a patient dashboard page.   | M  |
| FR.335.M   | The patient dashboard shall display a list of current prescriptions.   | M  |
| FR.340.M   | The patient dashboard shall display a list of upcoming appointments with the corresponding date and time.   | M  |
| FR.345.M   | The patient dashboard shall display a list of previous appointments including any prescriptions issued.   | M  |
| FR.350.M   | The patient dashboard shall display a list of prescription re-issuance requests that are pending approval.   | M  |
| FR.355.M   | The patient dashboard shall display a list of invoices for appointments and who is responsible for payment.   | M  |
| FR.360.M   | The system shall have an admin dashboard page.   | M  |
| FR.365.M   | The admin dashboard shall allow for the registration of a new doctor user.   | M  |
| FR.370.M   | The admin dashboard shall allow the viewing of a doctor's information.   | M  |
| FR.375.M   | The admin dashboard shall allow for the registration of a new nurse user.   | M  |
| FR.380.M   | The admin dashboard shall allow the viewing of a nurse's information.   | M  |
| FR.385.M   | The admin dashboard shall allow the editing of a patient's personal information including name, email address and home address.   | M  |
| FR.390.M   | The admin dashboard shall allow for the deletion of any existing user.   | M  |

#### 1.2.7.2. Non-functional Requirements

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
| NFR.055.S   | The system shall provide a user interface that allows the user to reach any page within 5 clicks. | S  |
| NFR.060.S   | The system shall allow a user to access their dashboard from any page on the site in one click. | S  |
| NFR.065.S   | The system shall allow a user to logout from any page on the site in one click. | S  |

### 1.2.8. References

Mavin, A., Wilkinson, P., Harwood, A. and Novak, M. (2009) Easy Approach to Requirements Syntax (EARS). In: 2009 17th IEEE International Requirements Engineering Conference [online]. 2009 17th IEEE International Requirements Engineering Conference (RE). Atlanta, Georgia, USA, IEEE, pp. 317–322. Available from: http://ieeexplore.ieee.org/document/5328509/ [Accessed 7 February 2024].