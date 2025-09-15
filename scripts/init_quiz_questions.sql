-- Quiz questions table for scalable random selection
CREATE TABLE IF NOT EXISTS quiz_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER,
    level TEXT,
    question TEXT,
    options TEXT,
    correct_answer INTEGER,
    explanation TEXT,
    FOREIGN KEY(course_id) REFERENCES courses(id)
);
