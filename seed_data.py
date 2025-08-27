#!/usr/bin/env python3
"""
Seed the database with sample courses and content
"""

import json
from db import get_connection, init_db

def create_sample_courses():
    """Create sample courses with proper JSON structure"""
    
    courses = [
        {
            'title': 'Python Fundamentals',
            'language': 'python',
            'difficulty': 'beginner',
            'level': 'beginner',
            'prerequisites': '',
            'description': json.dumps({
                'overview': 'Learn Python programming from scratch with hands-on examples and exercises.',
                'modules': [
                    {
                        'title': 'Python Basics',
                        'topics': [
                            'Introduction to Python',
                            'Variables and Data Types',
                            'Basic Operations',
                            'Input and Output'
                        ],
                        'exercises': 5
                    },
                    {
                        'title': 'Control Flow',
                        'topics': [
                            'If Statements',
                            'Loops',
                            'Break and Continue',
                            'Nested Structures'
                        ],
                        'exercises': 8
                    },
                    {
                        'title': 'Functions',
                        'topics': [
                            'Defining Functions',
                            'Parameters and Arguments',
                            'Return Values',
                            'Scope and Local Variables'
                        ],
                        'exercises': 6
                    }
                ],
                'resources': {
                    'documentation': 'https://docs.python.org/3/',
                    'practice': 'https://python.org/practice'
                }
            })
        },
        {
            'title': 'JavaScript Essentials',
            'language': 'javascript',
            'difficulty': 'beginner',
            'level': 'beginner',
            'prerequisites': '',
            'description': json.dumps({
                'overview': 'Master JavaScript fundamentals for web development.',
                'modules': [
                    {
                        'title': 'JavaScript Basics',
                        'topics': [
                            'Introduction to JavaScript',
                            'Variables and Constants',
                            'Data Types',
                            'Operators'
                        ],
                        'exercises': 4
                    },
                    {
                        'title': 'DOM Manipulation',
                        'topics': [
                            'Selecting Elements',
                            'Modifying Content',
                            'Event Handling',
                            'Dynamic Styling'
                        ],
                        'exercises': 7
                    }
                ],
                'resources': {
                    'documentation': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
                    'practice': 'https://javascript.info'
                }
            })
        },
        {
            'title': 'Web Development with PHP',
            'language': 'php',
            'difficulty': 'intermediate',
            'level': 'intermediate',
            'prerequisites': 'Basic HTML knowledge',
            'description': json.dumps({
                'overview': 'Build dynamic web applications with PHP.',
                'modules': [
                    {
                        'title': 'PHP Fundamentals',
                        'topics': [
                            'PHP Syntax',
                            'Variables and Arrays',
                            'Control Structures',
                            'Functions'
                        ],
                        'exercises': 6
                    },
                    {
                        'title': 'Web Development',
                        'topics': [
                            'Forms and User Input',
                            'Sessions and Cookies',
                            'File Handling',
                            'Database Integration'
                        ],
                        'exercises': 8
                    }
                ],
                'resources': {
                    'documentation': 'https://www.php.net/docs.php',
                    'practice': 'https://www.w3schools.com/php/'
                }
            })
        },
        {
            'title': 'Data Structures & Algorithms',
            'language': 'python',
            'difficulty': 'intermediate',
            'level': 'intermediate',
            'prerequisites': 'Basic Python knowledge',
            'description': json.dumps({
                'overview': 'Master fundamental data structures and algorithms for efficient programming.',
                'modules': [
                    {
                        'title': 'Basic Data Structures',
                        'topics': [
                            'Arrays and Lists',
                            'Stacks and Queues',
                            'Linked Lists',
                            'Hash Tables'
                        ],
                        'exercises': 8
                    },
                    {
                        'title': 'Trees and Graphs',
                        'topics': [
                            'Binary Trees',
                            'Binary Search Trees',
                            'Graph Representation',
                            'Graph Traversal'
                        ],
                        'exercises': 10
                    },
                    {
                        'title': 'Sorting and Searching',
                        'topics': [
                            'Bubble Sort',
                            'Quick Sort',
                            'Merge Sort',
                            'Binary Search'
                        ],
                        'exercises': 6
                    },
                    {
                        'title': 'Advanced Algorithms',
                        'topics': [
                            'Dynamic Programming',
                            'Greedy Algorithms',
                            'Backtracking',
                            'Complexity Analysis'
                        ],
                        'exercises': 12
                    }
                ],
                'resources': {
                    'documentation': 'https://docs.python.org/3/tutorial/datastructures.html',
                    'practice': 'https://leetcode.com/',
                    'visualization': 'https://visualgo.net/'
                }
            })
        }
    ]
    
    return courses

def seed_database():
    """Seed the database with sample data"""
    print("Initializing database...")
    init_db()
    
    connection = get_connection()
    cursor = connection.cursor()
    
    # Clear existing courses
    cursor.execute('DELETE FROM courses')
    cursor.execute('DELETE FROM progress')
    
    # Add programming languages
    languages = [
        ('Python', 'A versatile, high-level programming language', 'fab fa-python'),
        ('JavaScript', 'The language of the web', 'fab fa-js-square'),
        ('PHP', 'Server-side scripting language', 'fab fa-php'),
        ('SQL', 'Database query language', 'fas fa-database'),
        ('React', 'JavaScript library for building user interfaces', 'fab fa-react')
    ]
    
    cursor.execute('DELETE FROM programming_languages')
    for lang in languages:
        cursor.execute('''
            INSERT INTO programming_languages (name, description, icon_class)
            VALUES (?, ?, ?)
        ''', lang)
    
    # Add courses
    courses = create_sample_courses()
    for course in courses:
        cursor.execute('''
            INSERT INTO courses (title, description, language, difficulty, level, prerequisites)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            course['title'],
            course['description'],
            course['language'],
            course['difficulty'],
            course['level'],
            course['prerequisites']
        ))
    
    connection.commit()
    connection.close()
    
    print(f"Successfully seeded database with {len(courses)} courses and {len(languages)} programming languages.")

if __name__ == "__main__":
    seed_database()
    print("\nDatabase seeding complete!")
    print("You can now run the application and test the 'Start Learning' functionality.")
