# job-hunter-backend

This repository contains the backend for the job search web application using Django and Djongo ORM to connect to MongoDB.

## Tech Stack

- Django
- Djongo (Django MongoDB ORM)
- MongoDB

## Features

- User Authentication (Sign up and Log in)
- Job Search with fuzzy search functionality

## Requirements

- Python 3.10+
- MongoDB

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/devshoaibsarwar/job-hunter-backend.git
cd job-search-backend/api
```

## Step 2: Create a Virtual Environment

- Create a virtual environment to isolate the project dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate
```

## Step 3: Install Dependencies

- Install the necessary Python packages using pip.

```bash
pip install -r requirements.txt
```

## Step 4: Set Up MongoDB

### Local MongoDB Setup
1. Install MongoDB on your machine. You can follow the official installation guide.

2. Start the MongoDB server. By default, it runs on mongodb://localhost:27017.

### Cloud MongoDB Setup
1. Sign up for a MongoDB Atlas account and create a new cluster.
2. Get the connection string for your cluster. It should look like this:

```bash
mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority
```

- Replace <username>, <password>, and <dbname> with your MongoDB Atlas credentials and database name.

## Step 5: Configure Django Settings

- Create a .env file in the root of the project.

## Step 6: Apply Migrations

- Run the following command to apply database migrations:

## Step 7: Seed Data

- Run command below to populate sample data to database

```bash
python3 seed.py
```

## Step 8: Run the Development Server

- Start the Django development server:

```bash
python manage.py runserver
```

- The backend server should now be running at http://localhost:8000.

## API Endpoints
### Authentication

- Sign Up: POST /auth/sign-up/
- Log In: POST /auth/sign-in/
- Sign Out: POST /auth/sing-out

### Job Search
 
- Search Jobs: GET jobs/search?query=<job_title>
