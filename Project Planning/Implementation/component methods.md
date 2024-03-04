# 1. Component Methods

- [1. Component Methods](#1-component-methods)
  - [1.1. Patients](#11-patients)
    - [1.1.1. Appointments](#111-appointments)
      - [1.1.1.1. get\_future\_appointments](#1111-get_future_appointments)
      - [1.1.1.2. get\_appointment\_history](#1112-get_appointment_history)
      - [1.1.1.3. cancel\_appointment](#1113-cancel_appointment)
      - [1.1.1.4. Appointment Booking](#1114-appointment-booking)
        - [1.1.1.4.1. get\_available\_practicioners](#11141-get_available_practicioners)
        - [1.1.1.4.2. repopulateBookingFormData](#11142-repopulatebookingformdata)
        - [1.1.1.4.3. get\_list\_of\_services](#11143-get_list_of_services)
    - [1.1.2. Prescriptions](#112-prescriptions)
      - [1.1.2.1. issue\_prescription](#1121-issue_prescription)
      - [1.1.2.2. request\_repeat\_prescription](#1122-request_repeat_prescription)
      - [1.1.2.3. get\_current\_prescriptions](#1123-get_current_prescriptions)
      - [1.1.2.4. get\_prescription\_history](#1124-get_prescription_history)
  - [1.2. Invoices](#12-invoices)
    - [1.2.1. calculate\_appointment\_cost](#121-calculate_appointment_cost)
    - [1.2.2. get\_invoice\_history](#122-get_invoice_history)
    - [add\_new\_invoice](#add_new_invoice)
    - [mark\_invoice\_as\_paid](#mark_invoice_as_paid)
    - [1.2.3. create\_invoice\_file](#123-create_invoice_file)
    - [1.2.4. generate\_invoice](#124-generate_invoice)
  - [1.3. Doctor and Nurse Timetabling](#13-doctor-and-nurse-timetabling)
    - [1.3.1. get\_day\_timetable](#131-get_day_timetable)
    - [1.3.2. get\_week\_timetable](#132-get_week_timetable)
    - [1.3.3. Appointment Completion](#133-appointment-completion)
      - [1.3.3.1. issue\_prescription](#1331-issue_prescription)
      - [1.3.3.2. add\_appointment\_notes](#1332-add_appointment_notes)
    - [1.3.4. External APIs](#134-external-apis)
      - [1.3.4.1. addToCalendar](#1341-addtocalendar)
      - [1.3.4.2. getAddress](#1342-getaddress)
  - [1.4. Admin Functions](#14-admin-functions)
    - [1.4.1. create\_admin\_report\_file](#141-create_admin_report_file)
    - [1.4.2. generate\_admin\_report](#142-generate_admin_report)

## 1.1. Patients

### 1.1.1. Appointments

#### 1.1.1.1. get_future_appointments

```python
def get_future_appointments(userID: int) -> list[object]
```

This python method retrieves a list of all upcoming appointments for a given user. This shall return a list of ojects or `None` if no appointments have been made.

#### 1.1.1.2. get_appointment_history

```python
def get_appointment_history(userID: int) -> list[object]
```

This python method retrieves a list of all upcoming appointments for a given user. This shall return a list of ojects or `None` if no appointments have been made.

#### 1.1.1.3. cancel_appointment

```python
def cancel_appointment(appointmentID: int) -> JsonResponse
```

This python method removes an  appointment booking form the database for a given user. This shall return a `JsonResponse` containing info about whether it was successful or not and if not an accompanying message to display to the user. 

#### 1.1.1.4. Appointment Booking

##### 1.1.1.4.1. get_available_practicioners

```python
def get_available_practicioners(date: datetime) -> list[list[object, booking_times]]
```

This python method shall retrieve a list of practicioners, including doctors and nurses, who are available on a given date. A 2D list of `Nurse` or `Doctor` objects shall be returned paired with their correspodning appointments available for that given date. `None` shall be returned if there is no availability.

##### 1.1.1.4.2. repopulateBookingFormData

```javascript
function repopulateBookingFormData (formID, formData)
```

This javascript method shall receive the form data returned from AJAX calls to the DB to fetch information such as [get\_available\_practicioners](#1111-get_available_practicioners). This populate the necessary data into the form, including what has been returned from an AJAX call. 

##### 1.1.1.4.3. get_list_of_services

```python
def get_list_of_services() -> list[object]
```

This method shall retrieve a list of available services. A list of `Service` or Doctor objects shall be returned paired with their correspodning appointments available for that given date. `None` shall be returned if table is empty.

### 1.1.2. Prescriptions

#### 1.1.2.1. issue_prescription

```python
def issue_prescription(formData) -> JsonResponse
```

This python method shall receive prescription form data and add a new prescription to the database. This shall return a `JsonResponse` containing info about whether it was successful or not and if not an accompanying message to display to the user. 

#### 1.1.2.2. request_repeat_prescription

```python
def request_repeat_prescription() -> JsonResponse
```

This python method adds a new entry to the prescription re-issuance table in the database.

#### 1.1.2.3. get_current_prescriptions

```python
def get_future_appointments(userID: int) -> list[object]
```

This python method retrieves a list of current prescriptions for a given user. This shall return a list of ojects or `None` if no prescriptions have been issued.

#### 1.1.2.4. get_prescription_history

```python
def get_prescription_history(userID: int) -> list[object]
```

This python method retrieves a list of current prescriptions for a given user. This shall return a list of ojects or `None` if no prescriptions have been issued.

## 1.2. Invoices

### 1.2.1. calculate_appointment_cost

```python
def calculate_appointment_cost(appointmentID) -> float
```

This python method calculates the cost of the appointment given its ID. This shall incorporate the practicioner type and the length of the appointment. This value shall then be returned.

### 1.2.2. get_invoice_history

```python
def get_prescription_history(userID: int) -> list[object]
```

This python method retrieves a list of invoices for a given user. This shall return a list of ojects or `None` if no invoices have been issued.

### add_new_invoice

```python
def add_invoice(amount: float, appointmentID: int, patientID: int, billingParty: str) -> JsonResponse
```

This method shall be used to add a new invoice entry to the database. This shall return `0` if successful or `-1` if an error occurred. 



### mark_invoice_as_paid

```python
def mark_invoice_as_paid(invoiceID: int) -> JsonResponse
```

This python method shall update an invoice to be marked as paid.

This shall return `0` if successful or `-1` if an error occurred. 

### 1.2.3. create_invoice_file

```python
def create_invoice_file(description: str, costs: dict[str:float] ) -> str
```

This python method creates a text file containing the invoice information aninhe desired format and returns a link to a temporary file storage where the file can be downloaded.

The costs are passed as a dict where the key is the service or item and the value is the associated cost.

see the following for what needs to be included for an invoice

- a unique identification number
- your company name, address and contact information
- the company name and address of the customer you’re invoicing
- a clear description of what you’re charging for
- the date the goods or service were provided (supply date)
- the date of the invoice
- the amount(s) being charged
- VAT amount if applicable
- the total amount owed

<https://www.gov.uk/invoicing-and-taking-payment-from-customers/invoices-what-they-must-include>

### 1.2.4. generate_invoice

```python
def generate_invoice() -> FileResponse
```

This python method generates and returns an invoice based on the `calculate_appointment_cost` and `create_invoice_file` methods.

It shall return a `FileResponse` if successful or an error response if not.

Remember to include the following to make it download as an attachment

```python
return FileResponse(open_file, as_attachment=True, filename="INVOICE_NAME.txt")
```

See here for guidance <https://nemecek.be/blog/165/django-how-to-let-user-download-a-file>

## 1.3. Doctor and Nurse Timetabling

### 1.3.1. get_day_timetable 

```python
def get_day_timetable(date: datetime) -> list[object]
```

This python method returns a list of `Doctor` and `Nurse` objects that are working on the given day.

### 1.3.2. get_week_timetable

```python
def get_timetable_range(startDate: datetime, endDate: datetime) -> list[datetime, list[object]]
```

This python method returns a 2D list of `Doctor` and `Nurse` objects that are working on the given day.

### 1.3.3. Appointment Completion

#### 1.3.3.1. issue_prescription

see [1.1.2.1. issue\_prescription](#1121-issue_prescription).

#### 1.3.3.2. add_appointment_notes

```python
def add_appointment_notes(appointmentID: int, notes: str) -> JsonResponse
```

This python method adds appointment notes to a given appointment. It expects the appointment ID and the notes to associate with it. This shall return `0` if successful or `-1` if an error occurred.

### 1.3.4. External APIs

#### 1.3.4.1. addToCalendar

Google Calendar Insert Event - <https://developers.google.com/calendar/api/v3/reference/events/insert>

#### 1.3.4.2. getAddress

```javascript
function getAddress(address_info)
```

This javascript method shall use an external API to help autocomplete the address of users when they are completing their registration. This information shall then be displayed to the user as autocomplete options.

Simple APIs for UK Addresses - https://getaddress.io/

Google Maps Address Validation API - <https://developers.google.com/maps/documentation/address-validation>

Google Maps Places API - <https://developers.google.com/maps/documentation/places/web-service/overview>

## 1.4. Admin Functions

### 1.4.1. create_admin_report_file

```python
def create_admin_report_file() -> str
```

This python method is used to create a report containing patient turnover, private payments and payments sent to the NHS. A link to a temporary file storage where the file can be downloaded is returned.

### 1.4.2. generate_admin_report

```python
def generate_admin_report() -> FileResponse
```

This python method generates and returns an admin report based on the `create_admin_report_file` method. It shall return a `FileResponse` if successful or an error response if not.

Remember to include the following to make it download as an attachment

```python
return FileResponse(open_file, as_attachment=True, filename="REPORT_NAME.txt")
```

See here for guidance <https://nemecek.be/blog/165/django-how-to-let-user-download-a-file>
