# Busy Dating

Busy Dating is a sleek and powerful dating platform built on Django, designed for professionals who want to meet their perfect match without the hassle. With cutting-edge profile matching, real-time chat to keep you engaged, and a unique love discovery experience, Busy Dating makes it easier to turn fleeting connections into lasting relationships. Step into a world where finding love fits perfectly into your busy lifestyle

## Features

- **Profile Matching:** Powered by a clever algorithm, the profile matching system doesn’t just find similar interests but also aligns deeper values, ensuring a perfect fit.
- **Real-Time Chat:** Skip the awkward small talk and dive straight into exciting conversations. Real-time chat lets you connect instantly and authentically.
- **Love Search:** Take the guesswork out of dating. The unique love search system helps you discover your true match, sparking genuine connections that lead to something real.

## Installation

Follow these steps to set up the project on your local machine:

### 1. Clone the repository:

git clone https://github.com/vzxtq/busy_dating.git

### 2. Navigate to the project directory:

cd busy_dating

### 3. Create and activate a virtual environment:
```
python3 -m venv venv

source venv/bin/activate
# On Windows, use `venv\Scripts\activate`
```

### 4. Install dependencies:   
```
pip install -r requirements.txt
```
### 5. Create and Apply database migrations:
```
python manage.py makemigrations
python manage.py migrate
```
### 6. Run the development server:
```
python manage.py runserver
```
### 7. Open your browser and go to:

http://127.0.0.1:8000/
