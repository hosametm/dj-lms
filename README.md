# LMS API with Django and Django REST Framework

This project provides an API for LMS (Learning Management System) using **Django** and **Django REST Framework (DRF)**.

---
## Features
- Create, update, and delete courses.
- Add, update, and delete lessons.
- Enroll students in courses.
- Mark lessons as completed.
## Prerequisites
Before running the project, make sure you have the following installed:
- Python 3.x
- Django
- Django REST Framework

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hosametm/dj-lms.git
   cd dj-file-upload
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install --upgrade pip
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the server**:
   ```bash
   python manage.py runserver
   ```

6. **Test the API**: Open your browser or use a tool like [Postman](https://www.postman.com/) or `curl` to interact with the API.

---
Here's the documentation section tailored to your project:

---

## **API Endpoints**

### **Courses**
#### **1. List Courses**
- **URL**: `/api/courses/`
- **Method**: `GET`
- **Description**: Retrieves a list of all courses.
- **Response**: A list of course objects.

Example `curl` command:
```bash
curl http://127.0.0.1:8000/api/courses/
```

#### **2. Create a Course**
- **URL**: `/api/courses/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
      "title": "Course Title",
      "description": "Course Description"
  }
  ```

### **3. Enroll in a Course**
- **URL**: `/api/courses/{id}/enroll/`
- **Method**: `POST`
- **Request Body**:
  - `student` (Required): The ID of the student enrolling in the course.
  
- **Description**: Enrolls a student in a course.
- **Response**: A success or error message.

Example `curl` command:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"student": 1}' http://127.0.0.1:8000/api/courses/1/enroll/
```

---

### **4. List Enrolled Students**
- **URL**: `/api/courses/{id}/enrolled-students/`
- **Method**: `GET`
- **Path Parameter**:
  - `id` (Required): The ID of the course.

- **Description**: Retrieves a list of students enrolled in the specified course.
- **Response**: A list of student objects.

Example `curl` command:
```bash
curl http://127.0.0.1:8000/api/courses/1/enrolled-students/
```

---

### **5. Get Students' Progress**
- **URL**: `/api/courses/{id}/students-progress/`
- **Method**: `GET`
- **Query Parameters**:
  - `student` (Optional): Filter progress by student ID.

- **Description**: Retrieves the progress of students in a specific course.

Example `curl` command:
```bash
curl "http://127.0.0.1:8000/api/courses/1/students-progress/?student=1"
```

---




#### **6. Create a Lesson**
- **URL**: `/api/courses/{course_id}/lessons/`
- **Method**: `POST`
- **Form Data**:
  - `title` (Required): The title of the lesson.
  - `media` (Required): The file to upload (e.g., PDF, video).

- **Description**: Creates a lesson for the specified course, including uploading a media file.
- **Response**: Returns the created lesson details.

Example `curl` command:
```bash
curl -X POST -F "title=Lesson 1" -F "media=@/path/to/your/media/file.mp4" http://127.0.0.1:8000/api/courses/1/lessons/
```

---

#### **7. Retrieve, Update, or Delete a Lesson**
- **URL**: `/api/courses/{course_id}/lessons/{id}/`
- **Methods**:
  - `GET`: Retrieve lesson details.
  - `PUT` / `PATCH`: Update lesson details.
  - `DELETE`: Remove a lesson.

---

### **8. Save Lesson Progress**
- **URL**: `/api/courses/{course_id}/lessons/{lesson_id}/save-progress/`
- **Method**: `POST`
- **Request Body**:
  - `student` (Required): The ID of the student saving progress.

- **Description**: Saves progress for a specific lesson.
- **Response**: A success or error message.

Example `curl` command:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"student": 1}' http://127.0.0.1:8000/api/courses/1/lessons/2/save-progress/
```

--- 
## Technologies Used

- **Django**
- **Django REST Framework**
- **SQLite**

