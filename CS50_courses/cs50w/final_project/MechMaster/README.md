# CS50W Final Project - MechMaster

#### 🎥 YouTube URL: https://youtu.be/M6WkhHKB79A
[![Watch the video](https://img.youtube.com/vi/M6WkhHKB79A/hqdefault.jpg)](https://youtu.be/M6WkhHKB79A)

## Distinctiveness and Complexity

MechMaster is a unique online learning platform that stands out from other projects in the course due to its innovative approach to education and its comprehensive feature set. While many projects in the course focused on basic CRUD operations, MechMaster implements a complex ecosystem of features including user profiles, course enrollment, a dynamic forum, and interactive quizzes.

The complexity of MechMaster is evident in various aspects:
- **Interactive Learning Experience**: Unlike other projects, MechMaster incorporates video lessons, online resources, and interactive quizzes within each course module, providing a rich and engaging learning experience.
- **User Profiles and Enrollment**: MechMaster's user profile system allows learners to track their progress, view their enrolled courses, and manage their learning journey.
- **Forum with Real-Time Updates**: The integrated forum fosters community engagement among learners. Real-time updates on likes and views in forum topics enhance the user experience.
- **Sophisticated Quiz System**: MechMaster's quiz system allows instructors to create quizzes with multiple-choice questions. It displays a score at the end.

## Project Structure

The project is structured as follows:

- **academy**: The main Django app containing settings, URLs, and core project configurations.
- **users**: Manages user authentication, registration, and user profile functionality.
- **courses**: Handles courses, modules, lessons, and resources.
- **forum**: Implements the dynamic forum with categories, topics, and posts.
- **quizzes**: Manages the quiz creation, attempts, and scoring.
- **static**: Contains static files like CSS, JavaScript, and images.
- **templates**: Holds HTML templates for rendering the frontend.

## Running the Application

To run MechMaster on your local machine, follow these steps:

1. Clone the repository:
   ```shell
   git clone https://github.com/your-username/mechmaster.git
   cd mechmaster
   ```
2. Install the required Python packages:
    ```shell
    pip install -r requirements.txt
    ```
3. Set up the database:
    ```shell
    python manage.py migrate
    ```
4. Create a superuser for admin access:
    ```shell
    python manage.py createsuperuser
    ```
5. Run the development server:
    ```shell
        python manage.py runserver
    ```
6. Access the application in your browser at http://localhost:8000.

## File tree structure description

```
.
├── academy
│   ├── admin.py                    -> Django admin configurations for academy app models.
│   ├── apps.py                     -> App configuration for the academy app.
│   ├── forms.py                    -> Forms for data input and validation in the academy app.
│   ├── models.py                   -> Database models and relationships for the academy app.
│   ├── static
│   │   └── academy
│   │       ├── academy.js           -> JavaScript functionality for the academy app.
│   │       ├── course_page.js       -> JavaScript logic for displaying course pages.
│   │       ├── edit_profile.js      -> JavaScript logic for editing user profiles.
│   │       ├── images               -> Directory for static images used in the app.
│   │       │   ├── course.jpeg      -> Image for a course.
│   │       │   ├── intro.png        -> Introductory image.
│   │       │   ├── learn.jpeg       -> Image related to learning.
│   │       │   ├── login.jpeg       -> Login-related image.
│   │       │   └── no_image.webp    -> Placeholder image.
│   │       ├── style.css            -> Cascading Style Sheets for styling the app.
│   │       ├── tab_logic.js         -> JavaScript logic for handling tabs.
│   │       ├── take_quiz.js         -> JavaScript logic for taking quizzes.
│   │       └── topic_detail.js      -> JavaScript logic for topic detail pages.
│   ├── templates
│   │   └── academy
│   │       ├── course_list.html     -> HTML template for listing courses.
│   │       ├── course_page.html     -> HTML template for displaying a course page.
│   │       ├── course_registration.html -> HTML template for course registration.
│   │       ├── forum
│   │       │   ├── category_list.html  -> HTML template for listing forum categories.
│   │       │   ├── create_topic.html   -> HTML template for creating a forum topic.
│   │       │   ├── topic_detail.html   -> HTML template for displaying a forum topic.
│   │       │   └── topic_list.html     -> HTML template for listing forum topics.
│   │       ├── index.html            -> HTML template for the main index page.
│   │       ├── layout.html           -> Base HTML template for the app's layout.
│   │       ├── login.html            -> HTML template for user login.
│   │       ├── profile.html          -> HTML template for displaying user profiles.
│   │       ├── quiz_finished.html    -> HTML template for displaying finished quizzes.
│   │       ├── quiz_result.html      -> HTML template for displaying quiz results.
│   │       ├── register.html         -> HTML template for user registration.
│   │       ├── resources.html        -> HTML template for displaying resources.
│   │       └── take_quiz.html        -> HTML template for taking quizzes.
│   ├── tests.py                     -> Test cases for the academy app.
│   ├── urls.py                      -> URL routing for the academy app.
│   └── views.py                     -> Views and their logic for the academy app.
├── db.sqlite3                        -> SQLite database file.
├── manage.py                         -> Django management script.
├── MechMaster
│   ├── asgi.py                       -> ASGI interface configuration for the project.
│   ├── settings.py                   -> Project-wide settings and configurations.
│   ├── urls.py                       -> Project-wide URL routing.
│   └── wsgi.py                       -> WSGI interface configuration for the project.
├── media
│   └── images                        -> Directory for user-uploaded media images.
├── README.md                          -> This readme file with project documentation.
└── requirements.txt                   -> List of project dependencies.
```
## Additional Information

- MechMaster makes use of third-party packages like Django's embed_video for video content.
- User authentication and permissions are carefully managed to ensure security and data integrity.
- The project showcases extensive use of Django's ORM for complex database relationships and queries.
- MechMaster employs responsive design principles to ensure optimal user experience across devices.

The project's complexity lies in its holistic approach to online learning, incorporating multimedia content, community engagement, and interactive assessments. MechMaster aims to redefine the e-learning experience and sets itself apart through its comprehensive feature set and user-centric design.