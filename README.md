# Busy Dating

Busy Dating is a modern dating platform built with Django, designed to help busy professionals connect easily. With features like profile matching, real-time chat, and photo sharing, it simplifies the process of finding meaningful connections.

## Features

- **Profile Matching**: Smart matching system to find the most compatible partners.
- **Real-Time Chat**: Communicate instantly with your matches.
- **Photo Sharing**: Share moments from your life directly in the chat.

## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/vzxtq/busy_dating.git
Navigate to the project directory:

cd busy_dating
Create and activate a virtual environment:


python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install dependencies:


pip install -r requirements.txt
Apply database migrations:


python manage.py migrate
Run the development server:


python manage.py runserver
Open your browser and go to: http://127.0.0.1:8000/

Contributing
We welcome contributions from the community! To contribute:

Fork the repository.

Create a new branch for your feature or bug fix:


git checkout -b feature-name
Commit your changes:


git commit -m "Add feature description"
Push to your branch:

git push origin feature-name
