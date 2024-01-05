
# Whisper AI with Django, Celery, and Redis Project

## Overview
This project integrates Whisper, an advanced artificial intelligence for natural language processing and audio comprehension, with the robustness of Django, the efficiency of Celery for asynchronous task management, and the speed of Redis as a messaging system. Our objective was to create a dynamic and interactive web application that offers an unparalleled user experience.

## Features
- **Whisper AI Integration**: Utilizes Whisper for state-of-the-art natural language processing and audio understanding.
- **Django Framework**: Secure and scalable web application foundation.
- **Asynchronous Tasks**: Managed by Celery to ensure smooth performance.
- **Redis**: Used as an efficient message broker and storage system.
- **SRT Subtitle Download**: Users can download subtitles in SRT format, which is widely used in video editing.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/jravolio/Transcriber
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Setup Redis and ensure it's running on your system.

4. Run the Django migrations:
   ```
   python manage.py migrate
   ```

## Usage
- Start the Django development server:
  ```
  python manage.py runserver
  ```
- Start the Celery worker:
  ```
  python -m celery -A transcriber_project worker -l info
  ```
- Access the web application through the provided local server address.

## Contributing
We welcome contributions to this project. If you have suggestions or improvements, please fork the repository and create a pull request.
