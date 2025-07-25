# Welcome To The Multi Bed Browser

A Flask-based web application designed for managing, analyzing, and visualizing genomic BED files using Bedtools. Built for bioinformatics researchers, educators, and students, the platform enables secure file upload, project/study organization, multi-file analysis, and collaborative data review — all within a user-friendly interface.

## Purpose 

The Multi-Bed Browser provides a centralized, accessible environment for working with genomic interval data (e.g., BED files). It supports:

- Uploading files and associating them with projects and studies

- Viewing and managing metadata for genomic files

- Running secure, user-driven Bedtools operations (intersect, merge subtract, etc.)

- Saving and downloading results from custom analyses

- User registration with admin approval

- Role-based access (guest, user, admin)

## Repo includes:

- SQL script to create and populate database (multibed_scripts.sql)
- HTML template files (/templates)
- Project Description and setup instructions (README.md)
- Main Flask App (test3.py)


## Features

#### File & Project Management
- Upload BED files and annotate them with metadata (species, genome version, description, etc.)

- Create and manage projects and studies

- Assign PI ownership


#### Bedtools Integration
- Run Bedtools commands through a guided interface

- Select multiple input files for multi-file operations

- Generate dynamic output filenames (e.g., fileA_fileB_intersect.bed)

- Prevent path leakage (filenames only shown in UI)

#### Secure User System
- Password-protected registration with role selection

- Admin approval required before activating accounts

-  Role-based navigation and permissions


#### Admin Tools
- View all users

- Add, edit, or delete user accounts

- Approve or deny pending registrations

#### Interface Highlights

- Responsive Bootstrap UI

- Datatables for file listing and filtering

- Helpful guides and examples for users (help.html)


## Setup Instructions

You will need:

1. a computer with an internet server (Apache or similar)
2. to install mod_wsgi (works with Apache to serve flask programs)
3. Python 3.7 +
4. MariaDB 
5. Bedtools installed on system path
6. Flask + dependencies (requirements.txt)


## Contribution Guidelines
We welcome community involvement. Please:

- Fork the repo and submit pull requests for new features or bug fixes

- Follow best practices for Python and Flask development

- Add docstrings and comments for clarity

- Open issues for suggestions, bugs, or improvements

## Graphical Overview

## Credit 

##### Developers :  Aretha McDonald, Riya Jadhav, Yu Huang, and Zhanna Abdrassulova. 

This program was created as part of a course in Spring 2025 in collaboration with Prof. David Waxman, Boston University. 

## How Your Interface Should Look: 

#### Login.html
![Login](images/login.png)


#### Home.html
![Home1](images/home1.png)
![Home2](images/home2.png)
![Home3](images/home3.png)

#### Upload.html
![Upload1](images/upload1.png)
![Upload2](images/upload2.png)
![Upload3](images/upload3.png)

#### Search.html
![Search1](images/search1.png)
![Search2](images/search2.png)
![Search3](images/search3.png)
![Search4](images/search4.jpg)
![Search5](images/search5.jpg)
![Search6](images/search6.jpg)

#### Help.html
![Help1](images/help1.png)
![Help2](images/help2.png)
![Help3](images/help3.png)

#### View.html
![View](images/view.png)

#### Users.html
![Users](images/users.png)
