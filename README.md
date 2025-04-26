# MultiBed Browser

A web application for managing and browsing multi-bed genomic files.

## Project Description

MultiBed Browser is a Flask-based web application that allows users to upload, search, and manage genomic data files. The application includes user authentication and role-based access control.

## Features

- User authentication (login/logout)
- User management (admin users can create, edit, and delete users)
- File upload functionality
- Search capability for genomic data
- Role-based access control (admin/user roles)

## Project Structure

```
multibedbrowser/
├── app/
│   ├── templates/         # HTML templates
│   │   ├── base.html      # Base template with layout
│   │   ├── login.html     # Login page
│   │   ├── home.html      # Home page
│   │   ├── users.html     # User management page
│   │   ├── create_user.html  # Create user form
│   │   ├── edit_user.html    # Edit user form
│   │   └── ...
│   ├── static/            # Static files (CSS, JS, images)
│   ├── config.py          # Configuration settings
│   ├── login.py           # Main application file
│   ├── users.py           # User management functionality
│   ├── search.py          # Search functionality
│   └── upload.py          # File upload functionality
├── requirements.txt       # Dependencies
└── run.py                 # Application entry point
```

## Setup and Installation

### 1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # for Linux/Mac
# or
venv\Scripts\activate     # for Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up the database

Make sure your database configuration in `app/config.py` is correct.

### 4. Run the application

```bash
python run.py
```

The application will be accessible at http://localhost:5000

## Development

### Updating dependencies

After installing new packages, update the requirements file:

```bash
pip freeze > requirements.txt
```

### Git workflow

1. Ensure to pull any code before working on the project:
```bash
git pull
```

2. Commit any changes you've made:
```bash
git add .
git commit -m "Your descriptive message"
```

3. Push changes to the repository:
```bash
git push
```

## User Roles

- **Admin**: Can manage users, access all features
- **User**: Can upload and search files

## Database Structure

The application uses a MariaDB/MySQL database with the following main tables:
- Users: Stores user information and credentials
- Files: Stores uploaded file information
- Studies: Organizes files into research studies


## Files and Directories Proposed for Removal

The following files and directories are identified as unused and proposed for removal in the next iteration:

### Templates
- `templates/images` - Contains unused images. Copy of it in static/images
- `templates/test.html` - Testing template no longer needed
- `templates/shared_css.css` - css files must be located in static/css folder
- `templates/help.css` - css files must be located in static/css folder
- `templates/bedtools-form.js`- js files must be located in static/js folder

### Static Files
- `css` - in root of the project



### Python Files
- `app/test.py`


Please review and confirm these files can be safely removed before deletion. Ensure no active code depends on these resources.

Note: This list should be reviewed and approved by all team members before proceeding with removal.
