# Hospital Management System

This project is a fully functional **Hospital Management System (HMS)** built with Django. It provides a user-friendly interface for managing various hospital operations like doctor information, patient records, appointments, staff details, medical reports, and more.

![Dashboard Interface](https://github.com/naimur-naiyimu/Hospital-Management-System/blob/main/Dashboard.png)

## Live Demo
You can view the live version of the system at:  
👉 **[Hospital Management System - Live](https://hospital-management-system-kymj.onrender.com)**

## Features
The system offers the following key features:
- **Dashboard**: Overview of critical hospital statistics, including the number of doctors, patients, staff, wards, appointments, and prescriptions.
- **Doctor Management**: Add, view, and manage doctor profiles.
- **Patient Management**: Keep track of patient data, admission, and other details.
- **Staff Management**: Manage hospital staff information.
- **Appointment Scheduling**: Set and view appointments for patients.
- **Ward Management**: Manage hospital ward details.
- **Prescription Management**: Add, view, and manage prescriptions.
- **Medical Reports**: Store and retrieve patient medical reports.
- **Invoice Generation**: Manage and generate invoices for hospital services.

## Technologies Used
- **Backend**: Django (Python Framework)
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite (can be switched to PostgreSQL or other databases)
- **Deployment**: Render.com

## Installation Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/naimur-naiyimu/Hospital-Management-System.git
   cd Hospital-Management-System```
2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Run migrations**:

```bash
python manage.py migrate
```

4. **Create a superuser**:

```bash
python manage.py createsuperuser
```
5. **Run the development server**:

```bash
python manage.py runserver
```

## Future Improvements
- **Reporting and Analytics**: Add advanced reporting features to provide insights into hospital operations.
- **Email/Notification System**: Enable email and SMS notifications for appointments and other events.
- **Multi-language Support**: Add support for multiple languages to cater to a wider audience.
- **Role-Based Access Control (RBAC)**: Implement fine-grained user permissions.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
Thanks to everyone who contributed to the development of this project. Special thanks to [Render](https://render.com) for hosting the live application.

