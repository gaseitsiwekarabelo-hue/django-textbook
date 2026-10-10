# Django Textbook Project

## 1. Project Overview

This repository contains my Django learning project. It is being developed while I work through the Django Textbook chapters and practise building web applications with Python and Django.

The initial project focuses on creating a Django Hello World application. The next stage is to develop a library management application while learning how Django models, databases, migrations, the admin interface, and the Object-Relational Mapper (ORM) work.

## 2. Technologies Used

* Python
* Django
* Git
* GitHub
* SQLite
* Visual Studio Code
* Git Bash

## 3. Work Completed in Chapter 1

The following project setup tasks have been completed:

1. Created the `django-textbook` project directory.
2. Set up a Python virtual environment called `myenv`.
3. Created a Django project called `my_first_project`.
4. Created a Django application called `hello_world`.
5. Configured Git to track the project.
6. Created a `.gitignore` file to exclude unnecessary files.
7. Added the project files to Git.
8. Created the initial Git commit.
9. Connected the local repository to GitHub.
10. Prepared the project for version-controlled development.

### Git Repository

GitHub repository: `gaseitsiwekarabelo-hue/django-textbook`

Main branch: `main`

Learning branch: `liabrary`

## 4. Project Structure

```text
django-textbook/
├── .gitignore
├── README.md
├── manage.py
├── hello_world/
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── my_first_project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── myenv/
```

The virtual environment is excluded from version control.

## 5. Chapter 2: Models and Databases

Chapter 2 focuses on designing database schemas, managing data, and understanding how Django communicates with databases.

The chapter covers the following sections.

### 2.1 Introduction to Databases and Django's ORM

Topics:

* Understanding relational databases.
* Tables, rows, columns, and records.
* Introduction to SQL.
* Understanding the Object-Relational Mapper (ORM).
* Mapping Django models to database tables.
* Benefits and limitations of using an ORM.
* Using Python code instead of writing SQL for every database operation.

Example ORM operations:

```python
Book.objects.all()
Book.objects.filter(genre="Fiction")
Book.objects.get(id=1)
```

### 2.2 Configuring Your Database

Topics:

* Understanding Django's default SQLite database.
* Configuring PostgreSQL.
* Configuring MySQL.
* Managing database credentials securely.
* Using environment variables.
* Checking database connectivity.
* Running initial migrations.
* Understanding test databases.
* Troubleshooting common database errors.

Useful commands:

```bash
python manage.py check
python manage.py migrate
```

SQLite is suitable for getting started with this learning project.

### 2.3 Defining Models

Topics:

* Creating models using Python classes.
* Inheriting from `django.db.models.Model`.
* Defining database fields.
* Understanding Django field types.
* Using field options such as `max_length`, `default`, `blank`, `null`, and `unique`.
* Defining the `__str__()` method.
* Using model metadata through the `Meta` class.
* Validating model data.
* Using field choices, validators, indexes, and constraints.

Common field types include:

* `CharField`
* `TextField`
* `IntegerField`
* `DecimalField`
* `DateField`
* `DateTimeField`
* `BooleanField`
* `EmailField`
* `ForeignKey`
* `ManyToManyField`
* `OneToOneField`

The library application will use models to represent books and other library information.

### 2.4 Migrations

Topics:

* Understanding database migrations.
* Creating migration files.
* Applying migrations.
* Reviewing migration SQL.
* Checking migration history.
* Rolling back migrations.
* Understanding data migrations.
* Managing migration dependencies.
* Troubleshooting migration errors.

Migration workflow:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

Migrations allow database schema changes to be tracked alongside the application code.

### 2.5 The Django Admin Interface

Topics:

* Accessing the Django admin interface.
* Creating a superuser.
* Registering models.
* Managing records through the admin dashboard.
* Customizing the model administration interface.
* Adding search and filter options.
* Displaying selected fields.
* Managing related models.
* Understanding admin permissions and security.

Useful commands:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The admin interface can be accessed locally at:

`http://127.0.0.1:8000/admin/`

### 2.6 The Database API

Topics:

* Understanding QuerySets.
* Creating database records.
* Retrieving records.
* Filtering and excluding records.
* Updating records.
* Deleting records.
* Ordering query results.
* Using field lookups.
* Understanding lazy evaluation.
* Using complex queries with `Q` objects.
* Comparing field values with `F` objects.
* Aggregating and annotating data.
* Improving database query performance.

Common ORM operations:

```python
Book.objects.create(...)
Book.objects.all()
Book.objects.filter(is_available=True)
Book.objects.exclude(genre="F")
Book.objects.get(pk=1)
```

These operations demonstrate the basic create, read, update, and delete (CRUD) workflow.

### 2.7 Model Relationships

Topics:

* One-to-many relationships using `ForeignKey`.
* Many-to-many relationships using `ManyToManyField`.
* One-to-one relationships using `OneToOneField`.
* Understanding `on_delete`.
* Using `related_name`.
* Querying related models.
* Creating intermediary models for relationships with additional information.
* Optimizing relationship queries.

Possible library relationships include:

* One author can have multiple books.
* A publisher can publish multiple books.
* A book can have multiple authors.
* A book can have multiple physical copies.
* A book can receive multiple reviews.

### 2.8 Advanced Model Features

Topics:

* Abstract base classes.
* Multi-table model inheritance.
* Proxy models.
* Custom model managers.
* Custom QuerySets.
* Model instance methods.
* Class methods and properties.
* Django signals.
* Database constraints.
* Database indexes.
* Custom field types.
* Model metadata.

These features help developers create reusable, maintainable, and efficient Django applications.

### 2.9 Chapter Summary

The main learning objectives for Chapter 2 are:

* Understand relational databases and Django's ORM.
* Configure and test a database.
* Design Django models.
* Create and apply migrations.
* Manage records through the Django admin.
* Perform database operations using QuerySets.
* Establish relationships between models.
* Apply advanced model features when needed.
* Maintain database integrity and improve query performance.

## 6. Planned Library Application

The next development stage is to create a Django application named `library`.

The application will be used to practise the Chapter 2 concepts.

Planned features include:

* Managing book information.
* Recording author information.
* Recording publisher information.
* Categorizing books by genre.
* Tracking book availability.
* Managing physical book copies.
* Recording borrowing information.
* Managing book reviews.
* Using Django's admin interface to manage records.
* Querying related records through the ORM.

These are learning objectives and planned features; they should not be considered implemented until the corresponding code has been added and tested.

## 7. Planned Library App Setup

Create the application using:

```bash
python manage.py startapp library
```

Add the application to `INSTALLED_APPS` in `my_first_project/settings.py`:

```python
INSTALLED_APPS = [
    # Existing Django applications...
    "library",
]
```

The exact existing settings should be preserved when adding the new application.

After defining models, create and apply migrations:

```bash
python manage.py makemigrations library
python manage.py migrate
```

Check the project configuration:

```bash
python manage.py check
```

## 8. Git and GitHub Workflow

Git is used to track changes to the project. GitHub hosts the remote repository.

### Check the current branch

```bash
git branch
```

### Create and switch to the library learning branch

```bash
git switch -c liabrary
```

### Check changed files

```bash
git status
```

### Stage changes

```bash
git add .
```

### Commit changes

```bash
git commit -m "Add library learning documentation"
```

### Push the branch to GitHub

```bash
git push -u origin liabrary
```

After the first push, future changes on this branch can normally be uploaded using:

```bash
git add .
git commit -m "Describe your changes"
git push
```

Only commit files that belong in the repository. Do not commit the virtual environment, private credentials, or secrets.

## 9. Development Goals

The main goals of this project are to:

1. Build a working understanding of Django.
2. Practise Python and web application development.
3. Understand how Django applications are structured.
4. Learn to design and manage database models.
5. Practise migrations and database operations.
6. Use the Django admin interface.
7. Understand relationships between database records.
8. Apply Git branching and version control.
9. Maintain clear documentation of project progress.
10. Build a foundation for future Django applications.

## 10. Current Status

The initial Django project has been committed to Git, and the local repository is configured to use GitHub.

The `liabrary` branch is intended for the library learning work described in this README.

The library application, its models, and its database functionality must be implemented and tested as development continues.

---

**Project:** Django Textbook

**Repository:** `django-textbook`

**Learning branch:** `liabrary`

**Primary learning focus:** Django models, databases, migrations, the admin interface, ORM queries, and model relationships.
