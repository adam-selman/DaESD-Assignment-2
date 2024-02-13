# 1. Assignment 2 Planning

- [1. Assignment 2 Planning](#1-assignment-2-planning)
- [2. Requirements from Specification](#2-requirements-from-specification)
  - [2.1. User Roles and Access Control](#21-user-roles-and-access-control)
  - [2.2. Scheduling and Work Scheme](#22-scheduling-and-work-scheme)
  - [2.3. Billing and Invoicing](#23-billing-and-invoicing)
  - [2.4. User Functionalities](#24-user-functionalities)
    - [2.4.1. Doctors and Nurses](#241-doctors-and-nurses)
    - [2.4.2. Patients](#242-patients)
    - [2.4.3. Admin](#243-admin)
  - [2.5. System Collaboration](#25-system-collaboration)
  - [2.6. Integration with External Services](#26-integration-with-external-services)
  - [2.7. Security](#27-security)
- [3. Requirements from Expectations](#3-requirements-from-expectations)
  - [3.1. Pages](#31-pages)
  - [3.2. Navigation](#32-navigation)
  - [3.3. Authentication and Session Management](#33-authentication-and-session-management)
  - [3.4. External Services Integration](#34-external-services-integration)
  - [3.5. Database Deployment](#35-database-deployment)
  - [3.6. Collaboration with Advanced Artificial Intelligence (AAI) Module](#36-collaboration-with-advanced-artificial-intelligence-aai-module)
  - [3.7. Technology Stack](#37-technology-stack)


# 2. Requirements from Specification

## 2.1. User Roles and Access Control

- Doctor (full-time and part-time)
- Nurse (part-time)
- Patient
- Admin
- Users must log in to access the system.
- Logout functionality should be available manually or automatically after a specified non-active time (e.g., 5 minutes).
- Admin authorization is required for doctor and nurse sign-up; patient sign-up can be done automatically.

## 2.2. Scheduling and Work Scheme

- Calendar functionality for booking surgery appointments.
- Doctors and nurses should be able to see daily timetables of patients.
- Patients should be able to book appointments and request re-issuance of repeating prescriptions online.
- Weekly working scheme:
- Monday and Friday: 1 doctor and 1 nurse
- Rest of the week: 2 doctors

## 2.3. Billing and Invoicing

- Charges per consultation based on the length (standard consultation slot is 10 minutes).
- Invoices issued based on consultation length.
- Invoices sent to NHS or paid privately.
- Different invoicing rates for nurse services.
- System should produce an invoice following each surgery.
- Admin responsible for producing weekly documents (turnover, private payments, charges sent to NHS).
- Periodic turnover calculations (daily, weekly, monthly).

## 2.4. User Functionalities

### 2.4.1. Doctors and Nurses

- Issue prescriptions at the end of each consultation and surgery.

### 2.4.2. Patients

- Book appointments.
- Request re-issue of repeating prescriptions online.

### 2.4.3. Admin

- Manage records and user operations.

## 2.5. System Collaboration

- Collaboration with other GP services for exchanging patients and forwarding nurse operations.
- Future version should support collaborative operations with other GP services.

## 2.6. Integration with External Services

- Calendar functionality can be invoked from an existing calendar service (e.g., Google Calendar API).
- Address lookup can be handled through another web service (e.g., Google Map Services).

## 2.7. Security

- Access to functionalities requires user authentication and authorization.
- Substantial login system to ensure security.
- Restriction on accessing one user's dashboard from another without proper authentication.

# 3. Requirements from Expectations

## 3.1. Pages

- Main (home) page for user type and action selection.
- Login/registration page for member users.
- Dashboard page for "doctor" users.
- Dashboard page for "nurse" users.
- Dashboard page for "patient" users.
- Dashboard page for "admin" users with necessary processing operations.

## 3.2. Navigation

- Users should navigate smoothly between pages.
- Access to the user's dashboard and the home page from any page.

## 3.3. Authentication and Session Management

- Users remain logged in until the session times out or they are changed/logged out.
- Secured access to different members' dashboards.

## 3.4. External Services Integration

- Use of external calendar services (e.g., Google Calendar or any calendar service/API) for booking appointments with doctors or nurses.
- Use of another web service (e.g., Google Map services) for automatic address lookup.

## 3.5. Database Deployment

- Database deployment should be separate and connected via Docker containers.
- Reuse of work done for the Advanced Databases module is allowed.

## 3.6. Collaboration with Advanced Artificial Intelligence (AAI) Module

- Work for the AAI module assessment can be deployed on a separate container and accessed via web/restful services.

## 3.7. Technology Stack

- Python Django following MVC (MVT) patterns.
- Separate deployment of a database system (e.g., MySQL, PostgreSQL).
- Deployment conducted via Docker containers.
- Django Restful Framework (DRF) used with Docker for creating, deploying, and accessing services.
