import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_connection, init_db

def add_course_content():
    connection = get_connection()
    cursor = connection.cursor()

    # Python Course Content
    python_course_modules = [
        {
            'title': 'Introduction to Python',
            'content': 'Basic introduction to Python programming language',
            'topics': [
                {
                    'title': 'What is Python?',
                    'content': '''Python is a high-level, interpreted programming language known for its simplicity and readability.
                    Key points:
                    - Easy to learn
                    - Extensive library support
                    - Cross-platform compatibility
                    - Large community''',
                    'estimated_time': 30,
                    'quiz': [
                        {
                            'question': 'Which of these is a key feature of Python?',
                            'options': '["Complex syntax", "Readability", "Limited library support", "Machine-level programming"]',
                            'correct_answer': 1
                        }
                    ]
                },
                {
                    'title': 'Setting up Python Environment',
                    'content': '''Learn how to set up Python development environment:
                    1. Installing Python
                    2. Using IDEs (VSCode, PyCharm)
                    3. Running first Python program
                    4. Understanding Python package management''',
                    'estimated_time': 45,
                    'quiz': [
                        {
                            'question': 'What command is used to install Python packages?',
                            'options': '["install python", "apt-get install", "pip install", "python install"]',
                            'correct_answer': 2
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Python Basics',
            'content': 'Fundamental concepts of Python programming',
            'topics': [
                {
                    'title': 'Variables and Data Types',
                    'content': '''Learn about Python variables and data types:
                    - Numbers (int, float)
                    - Strings
                    - Lists
                    - Dictionaries
                    - Tuples
                    - Sets
                    - Boolean values''',
                    'estimated_time': 60,
                    'quiz': [
                        {
                            'question': 'Which of these is a mutable data type in Python?',
                            'options': '["Tuple", "String", "List", "Integer"]',
                            'correct_answer': 2
                        }
                    ]
                }
            ]
        }
    ]

    # Data Structures Course Content
    data_structures_modules = [
        {
            'title': 'Introduction to Data Structures',
            'content': 'Understanding basic data structures and their importance',
            'topics': [
                {
                    'title': 'Arrays and Lists',
                    'content': '''Learn about fundamental data structures:
                    - Arrays
                    - Dynamic Arrays
                    - Linked Lists
                    - Time Complexity
                    - Space Complexity''',
                    'estimated_time': 45,
                    'quiz': [
                        {
                            'question': 'What is the time complexity of accessing an element in an array by index?',
                            'options': '["O(1)", "O(n)", "O(log n)", "O(n^2)"]',
                            'correct_answer': 0
                        }
                    ]
                }
            ]
        }
    ]

    # Machine Learning Course Content
    ml_modules = [
        {
            'title': 'Introduction to Machine Learning',
            'content': 'Basic concepts and types of machine learning',
            'topics': [
                {
                    'title': 'What is Machine Learning?',
                    'content': '''Understanding machine learning basics:
                    - Definition and importance
                    - Types of ML (Supervised, Unsupervised, Reinforcement)
                    - Applications of ML
                    - Basic terminology''',
                    'estimated_time': 45,
                    'quiz': [
                        {
                            'question': 'Which type of learning uses labeled data?',
                            'options': '["Unsupervised Learning", "Supervised Learning", "Reinforcement Learning", "None of these"]',
                            'correct_answer': 1
                        }
                    ]
                }
            ]
        }
    ]

    # Add content for each course
    courses = {
        1: python_course_modules,
        2: data_structures_modules,
        3: ml_modules
    }

    for course_id, modules in courses.items():
        for i, module in enumerate(modules):
            # Add module
            cursor.execute('''
                INSERT INTO course_modules (course_id, title, content, order_index)
                VALUES (?, ?, ?, ?)
            ''', (course_id, module['title'], module['content'], i))
            module_id = cursor.lastrowid

            # Add topics for this module
            for j, topic in enumerate(module['topics']):
                cursor.execute('''
                    INSERT INTO course_topics (module_id, title, content, order_index, estimated_time)
                    VALUES (?, ?, ?, ?, ?)
                ''', (module_id, topic['title'], topic['content'], j, topic['estimated_time']))
                topic_id = cursor.lastrowid

                # Add quiz questions for this topic
                for question in topic['quiz']:
                    cursor.execute('''
                        INSERT INTO topic_quizzes (topic_id, question, options, correct_answer)
                        VALUES (?, ?, ?, ?)
                    ''', (topic_id, question['question'], question['options'], question['correct_answer']))

    connection.commit()
    connection.close()
    print("Course content added successfully!")

if __name__ == '__main__':
    init_db()
    add_course_content()
