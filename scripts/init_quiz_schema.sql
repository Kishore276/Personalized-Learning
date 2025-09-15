-- Create course_modules table
CREATE TABLE IF NOT EXISTS course_modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER,
    title TEXT,
    content TEXT,
    order_index INTEGER,
    FOREIGN KEY(course_id) REFERENCES courses(id)
);

-- Create course_topics table
CREATE TABLE IF NOT EXISTS course_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER,
    title TEXT,
    content TEXT,
    order_index INTEGER,
    estimated_time INTEGER,
    FOREIGN KEY(module_id) REFERENCES course_modules(id)
);

-- Create topic_quizzes table
CREATE TABLE IF NOT EXISTS topic_quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER,
    question TEXT,
    options TEXT,
    correct_answer INTEGER,
    difficulty TEXT,
    FOREIGN KEY(topic_id) REFERENCES course_topics(id)
);
