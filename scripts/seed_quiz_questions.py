import sqlite3
import json

# Template for seeding questions for all dashboard courses and levels
# Fill in your actual questions, options, and correct answers for each course/level
QUESTIONS = [
    # Bulk template for all dashboard courses and levels
]
COURSES_LEVELS = [
    ('Python Fundamentals', ['beginner', 'intermediate', 'advanced']),
    ('JavaScript Essentials', ['beginner', 'intermediate', 'advanced']),
    ('Web Development with PHP', ['beginner', 'intermediate', 'advanced']),
    ('Data Structures & Algorithms', ['beginner', 'intermediate', 'advanced']),
    ('Advanced JavaScript', ['beginner', 'intermediate', 'advanced']),
    ('Java Programming', ['beginner', 'intermediate', 'advanced']),
    ('Advanced Java', ['beginner', 'intermediate', 'advanced']),
    ('C++ Fundamentals', ['beginner', 'intermediate', 'advanced']),
    ('HTML & CSS Basics', ['beginner', 'intermediate', 'advanced']),
    ('Advanced CSS & Responsive Design', ['beginner', 'intermediate', 'advanced']),
    ('React Development', ['beginner', 'intermediate', 'advanced']),
    ('Advanced React & Redux', ['beginner', 'intermediate', 'advanced']),
    ('Node.js Backend Development', ['beginner', 'intermediate', 'advanced']),
    ('Python for Data Science', ['beginner', 'intermediate', 'advanced']),
    ('Machine Learning Basics', ['beginner', 'intermediate', 'advanced']),
    ('Deep Learning with TensorFlow', ['beginner', 'intermediate', 'advanced']),
    ('SQL Fundamentals', ['beginner', 'intermediate', 'advanced']),
    ('Advanced SQL & Database Design', ['beginner', 'intermediate', 'advanced']),
    ('Android Development with Java', ['beginner', 'intermediate', 'advanced']),
    ('iOS Development with Swift', ['beginner', 'intermediate', 'advanced']),
    ('Git & Version Control', ['beginner', 'intermediate', 'advanced']),
    ('Docker & Containerization', ['beginner', 'intermediate', 'advanced']),
    ('AWS Cloud Fundamentals', ['beginner', 'intermediate', 'advanced'])
]
for course, levels in COURSES_LEVELS:
    for level in levels:
        for i in range(1, 16):
            QUESTIONS.append({
                'course_title': course,
                'level': level,
                'question': f'Sample question {i} for {course} ({level})',
                'options': json.dumps(['Option A', 'Option B', 'Option C', 'Option D']),
                'correct_answer': 0,
                'explanation': f'This is a sample explanation for question {i}.'
            })
]

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Get course_id for each course_title
course_ids = {}
cursor.execute('SELECT id, title FROM courses')
for row in cursor.fetchall():
    course_ids[row[1]] = row[0]

for q in QUESTIONS:
    course_id = course_ids.get(q['course_title'])
    if course_id:
        cursor.execute(
            'INSERT INTO quiz_questions (course_id, level, question, options, correct_answer, explanation) VALUES (?, ?, ?, ?, ?, ?)',
            (course_id, q['level'], q['question'], q['options'], q['correct_answer'], q['explanation'])
        )

conn.commit()
conn.close()
print('Quiz questions seeded for all dashboard courses and levels.')
