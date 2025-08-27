import json
import os
from db import get_connection

def populate_courses_from_json():
    """Extract course information from JSON files and populate the courses table"""
    quiz_dir = 'data/quiz_questions'
    
    if not os.path.exists(quiz_dir):
        print(f"Quiz directory {quiz_dir} not found!")
        return
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Clear existing courses
    cursor.execute('DELETE FROM courses')
    
    courses = []
    
    # Process each JSON file
    for filename in os.listdir(quiz_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(quiz_dir, filename)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                course_id = data.get('course_id')
                course_title = data.get('course_title')
                language = data.get('language', 'unknown')
                
                if course_id and course_title:
                    # Create description based on title
                    description = f"Learn {course_title} programming concepts and best practices."
                    
                    # Determine difficulty level
                    title_lower = course_title.lower()
                    if 'fundamentals' in title_lower or 'basics' in title_lower:
                        difficulty = 'beginner'
                    elif 'advanced' in title_lower:
                        difficulty = 'advanced'
                    else:
                        difficulty = 'intermediate'
                    
                    courses.append((course_id, course_title, description, language, difficulty))
                    print(f"Found course: {course_id} - {course_title} ({language}, {difficulty})")
                
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    # Sort courses by ID
    courses.sort(key=lambda x: x[0])
    
    # Insert courses into database
    cursor.executemany('''
        INSERT INTO courses (id, title, description, language, difficulty) 
        VALUES (?, ?, ?, ?, ?)
    ''', courses)
    
    conn.commit()
    conn.close()
    
    print(f"\nSuccessfully populated {len(courses)} courses:")
    for course in courses:
        print(f"  {course[0]}: {course[1]} ({course[3]}, {course[4]})")

if __name__ == '__main__':
    populate_courses_from_json()
