# AfyaLink Backend

AfyaLink is a secure multi-hospital digital health infrastructure built using Django and Django REST Framework.
The backend provides a centralized API that allows hospitals to manage healthcare staff, record medical data, and securely access patient information while enforcing strict role-based access control and hospital-level data isolation.

## Overview
Healthcare systems often suffer from fragmented patient data, where medical records are stored separately across different hospitals. This leads to inefficiencies, repeated tests, and limited continuity of care.
AfyaLink addresses this problem by providing a centralized backend system where:
- Patients can register and manage their profiles
- Hospitals can manage their staff
- Doctors can record diagnoses and treatment plans
- Labs and radiologists can upload diagnostic records
- Pharmacists can manage prescriptions
- Hospitals can securely access relevant patient information

The platform ensures that only authorized users can access specific data, protecting patient privacy and maintaining medical data integrity.

## Key Features
Multi-Hospital Support
AfyaLink supports multiple hospitals within the same platform.
Each hospital can:
- Manage its own staff
- Record patient visits
- Access patient records relevant to their facility

Data isolation ensures hospitals cannot access unrelated patient information.

## Role-Based Access Control

AfyaLink uses a structured role system to manage permissions.
Supported roles include:
- Super Admin
- Hospital Admin
- Doctor/Consultant
- Nurse
- Lab Technologist
- Radiologist
- Pharmacist
- Receptionist
- Patient
Each role has specific permissions enforced at the API level using Django REST Framework permission classes.

## Secure Authentication
Authentication is handled using JSON Web Tokens (JWT) via SimpleJWT.
Benefits include:
1.Secure API access
2. Stateless authentication
3. Token-based session management
4. Easy integration with web or mobile frontends

### Patient Identity and Profiles
Patients register on the platform and are associated with a PatientProfile.
This profile stores medical identity information separate from authentication.
Structure:

User (authentication)
    └── PatientProfile (medical identity)

This separation improves security and data organization.

### Medical Records Management
AfyaLink organizes medical records into structured modules.
Healthcare professionals can record:
Lab results
Radiology reports
Diagnoses
Prescriptions
Medical images and reports are stored using Cloudinary.
Hospital Staff Management
  
Hospital administrators can create and manage staff members for their hospital.

Staff roles include:
Doctors
Nurses
Lab Technologists
Radiologists
Pharmacists
Receptionists

This ensures hospitals maintain control over their workforce.

## Technology Stack

1.Backend Framework
 Django
2. API Framework
 Django REST Framework
3. Authentication
 JWT (SimpleJWT)
4.Database
PostgreSQL (recommended)
5.Media Storage
Cloudinary
6.Testing
Postman
7.Development Tools
Python Virtual Environment
Visual Studio Code

## Security Considerations
AfyaLink implements several security practices:
JWT authentication
Role-based permissions
Hospital data isolation
Controlled staff creation
Protected API endpoints
Secure media storage

## Future Improvements
Planned system upgrades include:
React frontend dashboard
Patient mobile application
Real-time notifications
National health data interoperability
Electronic health record (EHR) standards integration
AI-assisted clinical decision support
## Author
Emmanuel Musungu
+254796285410
