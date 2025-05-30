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


