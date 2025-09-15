import sys
import json
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_connection

def add_course_content():
    connection = get_connection()
    cursor = connection.cursor()

    # Clear existing modules and topics
    cursor.execute('DELETE FROM course_topics')
    cursor.execute('DELETE FROM course_modules')

    # Insert course descriptions as JSON with modules and topics
    python_description = json.dumps({
        "overview": "Learn Python programming from basics to advanced.",
        "modules": [
            {
                "title": "Python Basics",
                "topics": ["Variables and Data Types", "Basic Operations", "Input and Output"]
            },
            {
                "title": "Control Flow",
                "topics": ["If Statements", "Loops", "Error Handling"]
            },
            {
                "title": "Functions and Modules",
                "topics": ["Function Basics", "Modules and Packages"]
            },
            {
                "title": "Data Structures",
                "topics": ["Lists and Tuples", "Dictionaries"]
            }
        ]
    })

    ds_description = json.dumps({
        "overview": "Master data structures for efficient programming.",
        "modules": [
            {
                "title": "Array Structures",
                "topics": ["Arrays and Lists", "Dynamic Arrays"]
            },
            {
                "title": "Linked Structures",
                "topics": ["Linked Lists", "Stacks and Queues"]
            },
            {
                "title": "Tree Structures",
                "topics": ["Binary Trees", "Binary Search Trees"]
            },
            {
                "title": "Graph Structures",
                "topics": ["Graph Representation", "Graph Algorithms"]
            }
        ]
    })

    ml_description = json.dumps({
        "overview": "Introduction to machine learning concepts.",
        "modules": [
            {
                "title": "ML Foundations",
                "topics": ["Supervised Learning", "Unsupervised Learning"]
            },
            {
                "title": "Model Evaluation",
                "topics": ["Cross Validation", "Metrics"]
            },
            {
                "title": "Neural Networks",
                "topics": ["Perceptron", "Deep Learning"]
            }
        ]
    })

    aws_description = json.dumps({
        "overview": "Learn the basics of AWS Cloud and its core services.",
        "modules": [
            {
                "title": "Cloud Concepts",
                "topics": ["What is Cloud Computing?", "Benefits of Cloud", "Cloud Deployment Models"]
            },
            {
                "title": "Core AWS Services",
                "topics": ["EC2", "S3", "RDS", "Lambda"]
            },
            {
                "title": "Security and Compliance",
                "topics": ["IAM", "Shared Responsibility Model", "Compliance Programs"]
            }
        ]
    })

    # Update courses table with JSON descriptions
    cursor.execute("UPDATE courses SET description=? WHERE id=1", (python_description,))
    cursor.execute("UPDATE courses SET description=? WHERE id=2", (ds_description,))
    cursor.execute("UPDATE courses SET description=? WHERE id=3", (ml_description,))

    # Add AWS Cloud Fundamentals course if not exists
    cursor.execute("SELECT id FROM courses WHERE title=?", ("AWS Cloud Fundamentals",))
    aws_course = cursor.fetchone()
    if not aws_course:
        cursor.execute("INSERT INTO courses (title, description, language, category, difficulty) VALUES (?, ?, ?, ?, ?)",
            ("AWS Cloud Fundamentals", aws_description, "English", "Cloud", "Beginner"))
        aws_course_id = cursor.lastrowid
    else:
        aws_course_id = aws_course[0]
        cursor.execute("UPDATE courses SET description=? WHERE id=?", (aws_description, aws_course_id))

    # Add modules for AWS Cloud Fundamentals
    cursor.execute("INSERT INTO course_modules (course_id, title, content, order_index) VALUES (?, 'Cloud Concepts', 'Introduction to cloud computing and deployment models', 1)", (aws_course_id,))
    cursor.execute("INSERT INTO course_modules (course_id, title, content, order_index) VALUES (?, 'Core AWS Services', 'Overview of EC2, S3, RDS, Lambda', 2)", (aws_course_id,))
    cursor.execute("INSERT INTO course_modules (course_id, title, content, order_index) VALUES (?, 'Security and Compliance', 'IAM, shared responsibility, compliance', 3)", (aws_course_id,))

    # Get module IDs for topics
    cursor.execute("SELECT id FROM course_modules WHERE course_id=? ORDER BY order_index", (aws_course_id,))
    aws_module_ids = [row[0] for row in cursor.fetchall()]

    # Add at least 15 beginner-level AWS Cloud questions
    aws_beginner_questions = [
        ("What is AWS EC2 used for?", '["Compute resources", "Storage", "Networking", "Security"]', 0, 'easy'),
        ("Which AWS service is for object storage?", '["EC2", "S3", "RDS", "Lambda"]', 1, 'easy'),
        ("What does IAM stand for?", '["Identity and Access Management", "Infrastructure as a Module", "Instance Access Method", "Internet Access Management"]', 0, 'easy'),
        ("Which AWS service is serverless compute?", '["EC2", "S3", "Lambda", "RDS"]', 2, 'easy'),
        ("What is the main benefit of cloud computing?", '["Scalability", "Manual management", "Fixed resources", "No security"]', 0, 'easy'),
        ("Which deployment model is AWS?", '["Public Cloud", "Private Cloud", "Hybrid Cloud", "On-premise"]', 0, 'easy'),
        ("What is S3 mainly used for?", '["Storing files", "Running code", "Networking", "Security"]', 0, 'easy'),
        ("Which service is a managed database?", '["RDS", "EC2", "S3", "IAM"]', 0, 'easy'),
        ("What is the AWS shared responsibility model?", '["Security shared between AWS and customer", "AWS is fully responsible", "Customer is fully responsible", "No responsibility"]', 0, 'easy'),
        ("Which service is used for user access control?", '["IAM", "EC2", "S3", "Lambda"]', 0, 'easy'),
        ("What is a region in AWS?", '["Geographic area", "Security group", "Database", "User role"]', 0, 'easy'),
        ("Which service is used for scalable storage?", '["S3", "EC2", "IAM", "Lambda"]', 0, 'easy'),
        ("What is the main use of AWS Lambda?", '["Run code without servers", "Store files", "Manage users", "Create databases"]', 0, 'easy'),
        ("Which AWS service is best for storing backups?", '["S3", "EC2", "IAM", "Lambda"]', 0, 'easy'),
        ("What is the main function of AWS RDS?", '["Managed relational database", "Object storage", "Compute", "Networking"]', 0, 'easy'),
    ]
    # Use first module for all beginner questions for simplicity
    if aws_module_ids:
        for idx, (question, options, correct, diff) in enumerate(aws_beginner_questions):
            cursor.execute(
                "INSERT INTO topic_quizzes (topic_id, question, options, correct_answer, difficulty) VALUES (?, ?, ?, ?, ?)",
                (aws_module_ids[0], question, options, correct, diff)
            )
    connection = get_connection()
    cursor = connection.cursor()

    # Clear existing modules and topics
    cursor.execute('DELETE FROM course_topics')
    cursor.execute('DELETE FROM course_modules')
    
    # Insert course descriptions as JSON with modules and topics
    python_description = json.dumps({
        "overview": "Learn Python programming from basics to advanced.",
        "modules": [
            {
                "title": "Python Basics",
                "topics": ["Variables and Data Types", "Basic Operations", "Input and Output"]
            },
            {
                "title": "Control Flow",
                "topics": ["If Statements", "Loops", "Error Handling"]
            },
            {
                "title": "Functions and Modules",
                "topics": ["Function Basics", "Modules and Packages"]
            },
            {
                "title": "Data Structures",
                "topics": ["Lists and Tuples", "Dictionaries"]
            }
        ]
    })

    ds_description = json.dumps({
        "overview": "Master data structures for efficient programming.",
        "modules": [
            {
                "title": "Array Structures",
                "topics": ["Arrays and Lists", "Dynamic Arrays"]
            },
            {
                "title": "Linked Structures",
                "topics": ["Linked Lists", "Stacks and Queues"]
            },
            {
                "title": "Tree Structures",
                "topics": ["Binary Trees", "Binary Search Trees"]
            },
            {
                "title": "Graph Structures",
                "topics": ["Graph Representation", "Graph Algorithms"]
            }
        ]
    })

    ml_description = json.dumps({
        "overview": "Introduction to machine learning concepts.",
        "modules": [
            {
                "title": "ML Foundations",
                "topics": ["Supervised Learning", "Unsupervised Learning"]
            },
            {
                "title": "Model Evaluation",
                "topics": ["Cross Validation", "Metrics"]
            },
            {
                "title": "Neural Networks",
                "topics": ["Perceptron", "Deep Learning"]
            }
        ]
    })

    # Update courses table with JSON descriptions
    cursor.execute("UPDATE courses SET description=? WHERE id=1", (python_description,))
    cursor.execute("UPDATE courses SET description=? WHERE id=2", (ds_description,))
    cursor.execute("UPDATE courses SET description=? WHERE id=3", (ml_description,))
    cursor.execute("INSERT INTO course_modules (course_id, title, content, order_index) VALUES (3, 'Introduction to ML', 'Basic concepts of machine learning', 1)")
    cursor.execute("INSERT INTO course_modules (course_id, title, content, order_index) VALUES (3, 'Supervised Learning', 'Understanding supervised learning algorithms', 2)")
    cursor.execute("INSERT INTO course_modules (course_id, title, content, order_index) VALUES (3, 'Unsupervised Learning', 'Understanding unsupervised learning', 3)")
    cursor.execute("INSERT INTO course_modules (course_id, title, content, order_index) VALUES (3, 'Model Evaluation', 'Evaluating machine learning models', 4)")

    # Add AWS Cloud Fundamentals course if not exists
    cursor.execute("SELECT id FROM courses WHERE title=?", ("AWS Cloud Fundamentals",))
    aws_course = cursor.fetchone()
    if not aws_course:
        cursor.execute("INSERT INTO courses (title, description, language, category, difficulty) VALUES (?, ?, ?, ?, ?)",
            ("AWS Cloud Fundamentals", aws_description, "English", "Cloud", "Beginner"))
        aws_course_id = cursor.lastrowid
    else:
        aws_course_id = aws_course[0]
        cursor.execute("UPDATE courses SET description=? WHERE id=?", (aws_description, aws_course_id))
    # Add modules and topics for AWS Cloud Fundamentals
    cursor.execute("INSERT INTO course_modules (course_id, title, content, order_index) VALUES (?, 'Cloud Concepts', 'Introduction to cloud computing and deployment models', 1)", (aws_course_id,))
    cursor.execute("INSERT INTO course_modules (course_id, title, content, order_index) VALUES (?, 'Core AWS Services', 'Overview of EC2, S3, RDS, Lambda', 2)", (aws_course_id,))
    cursor.execute("INSERT INTO course_modules (course_id, title, content, order_index) VALUES (?, 'Security and Compliance', 'IAM, shared responsibility, compliance', 3)", (aws_course_id,))
    # Get module IDs for ML course
    cursor.execute("SELECT id FROM course_modules WHERE course_id=3 ORDER BY order_index")
    ml_module_ids = [row[0] for row in cursor.fetchall()]
    ml_topics = [
        (ml_module_ids[0], 'What is Machine Learning?', 'Introduction to machine learning concepts and applications.', 1, 30),
        (ml_module_ids[0], 'Types of ML', 'Overview of different types of machine learning approaches.', 2, 40),
        (ml_module_ids[1], 'Linear Regression', 'Understanding and implementing linear regression.', 1, 60),
        (ml_module_ids[1], 'Classification', 'Basic classification algorithms and their applications.', 2, 50),
        (ml_module_ids[2], 'Clustering', 'K-means and hierarchical clustering algorithms.', 1, 45),
        (ml_module_ids[2], 'Dimensionality Reduction', 'PCA and other dimensionality reduction techniques.', 2, 50),
        (ml_module_ids[3], 'Model Metrics', 'Understanding different evaluation metrics.', 1, 40),
        (ml_module_ids[3], 'Cross-Validation', 'Cross-validation techniques and model selection.', 2, 45)
    ]
    for topic in ml_topics:
        cursor.execute("INSERT INTO course_topics (module_id, title, content, order_index, estimated_time) VALUES (?, ?, ?, ?, ?)", topic)

    # Add quizzes for topics
    quizzes = [
        (1, 'Which of these is not a Python data type?', '["int", "float", "string", "character"]', 3, 'easy'),
        (1, 'What is the output of type(42)?', '["<class ''int''>", "<class ''str''>", "<class ''float''>", "<class ''number''>"]', 0, 'easy'),
        (4, 'What is the output of: 5 > 3 and 2 < 4?', '["True", "False", "5", "Error"]', 0, 'medium'),
        (5, 'Which loop is used when you know the number of iterations?', '["for loop", "while loop", "do-while loop", "repeat loop"]', 0, 'easy')
    ]
    for quiz in quizzes:
        cursor.execute("INSERT INTO topic_quizzes (topic_id, question, options, correct_answer, difficulty) VALUES (?, ?, ?, ?, ?)", quiz)

    connection.commit()
    connection.close()

if __name__ == '__main__':
    add_course_content()
