import sqlite3
from db import get_connection

def create_module_content():
    """Create detailed content for all modules and submodules"""
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all modules with their course information
    cursor.execute('''
        SELECT m.id, m.title, m.description, m.course_id, c.title as course_title, c.language
        FROM modules m
        JOIN courses c ON m.course_id = c.id
        ORDER BY m.course_id, m.module_order
    ''')
    
    modules = cursor.fetchall()
    
    for module in modules:
        module_id, module_title, module_desc, course_id, course_title, language = module
        
        # Generate content based on language and module
        content = generate_content_by_language(language, module_title, course_title)
        
        # Update module with detailed content
        cursor.execute('''
            UPDATE modules 
            SET description = ? 
            WHERE id = ?
        ''', (content['description'], module_id))
        
        # Update submodules with detailed content
        cursor.execute('''
            SELECT id, title, submodule_order 
            FROM submodules 
            WHERE module_id = ?
            ORDER BY submodule_order
        ''', (module_id,))
        
        submodules = cursor.fetchall()
        
        for submodule in submodules:
            sub_id, sub_title, sub_order = submodule
            
            # Generate submodule content based on type
            if 'Theory' in sub_title:
                sub_content = content['theory']
            elif 'Examples' in sub_title:
                sub_content = content['examples']
            elif 'Exercises' in sub_title:
                sub_content = content['exercises']
            elif 'Quiz' in sub_title:
                sub_content = content['quiz']
            else:
                sub_content = content['theory']  # Default
            
            cursor.execute('''
                UPDATE submodules 
                SET content = ? 
                WHERE id = ?
            ''', (sub_content, sub_id))
    
    conn.commit()
    conn.close()
    print("Module content updated successfully!")

def generate_content_by_language(language, module_title, course_title):
    """Generate detailed content based on programming language and module"""
    
    content_templates = {
        'python': {
            'description': f"Master {module_title.replace('Module ', '').replace(': ', ' - ')} concepts in Python programming. This module covers essential Python skills needed for real-world development.",
            'theory': f"""
            <div class="module-content">
                <h3>📚 Theoretical Foundation</h3>
                <p>Welcome to <strong>{module_title}</strong> in the {course_title} course!</p>
                
                <div class="learning-objectives">
                    <h4>🎯 Learning Objectives</h4>
                    <ul>
                        <li>Understand core Python concepts and syntax</li>
                        <li>Learn best practices for Python development</li>
                        <li>Master problem-solving approaches</li>
                        <li>Build confidence in Python programming</li>
                    </ul>
                </div>
                
                <div class="key-concepts">
                    <h4>🔑 Key Concepts</h4>
                    <p>In this module, you'll explore fundamental Python concepts including:</p>
                    <ul>
                        <li><strong>Syntax & Structure:</strong> Python's clean and readable syntax</li>
                        <li><strong>Data Types:</strong> Numbers, strings, lists, dictionaries</li>
                        <li><strong>Control Flow:</strong> Conditional statements and loops</li>
                        <li><strong>Functions:</strong> Creating reusable code blocks</li>
                    </ul>
                </div>
                
                <div class="why-important">
                    <h4>💡 Why This Matters</h4>
                    <p>These concepts form the foundation of all Python programming. Understanding them deeply will enable you to write efficient, maintainable code and tackle complex programming challenges.</p>
                </div>
            </div>
            """,
            'examples': f"""
            <div class="module-content">
                <h3>💻 Practical Examples</h3>
                <p>Let's see <strong>{module_title}</strong> concepts in action with real Python code!</p>
                
                <div class="code-example">
                    <h4>Example 1: Basic Implementation</h4>
                    <pre><code class="python">
# Python Example for {module_title}
def welcome_message(name):
    '''
    A simple function demonstrating Python basics
    '''
    greeting = f"Hello, {{name}}! Welcome to Python programming."
    return greeting

# Using the function
student_name = "Alex"
message = welcome_message(student_name)
print(message)

# Output: Hello, Alex! Welcome to Python programming.
                    </code></pre>
                </div>
                
                <div class="code-example">
                    <h4>Example 2: Practical Application</h4>
                    <pre><code class="python">
# Real-world example
students = ["Alice", "Bob", "Charlie", "Diana"]
grades = [85, 92, 78, 96]

# Creating a student grade dictionary
student_grades = dict(zip(students, grades))

# Finding top performer
top_student = max(student_grades, key=student_grades.get)
print(f"Top performer: {{top_student}} with {{student_grades[top_student]}}%")
                    </code></pre>
                </div>
                
                <div class="explanation">
                    <h4>🔍 Code Explanation</h4>
                    <p>These examples demonstrate key Python features:</p>
                    <ul>
                        <li><strong>Functions:</strong> Organizing code into reusable blocks</li>
                        <li><strong>String formatting:</strong> Using f-strings for readable output</li>
                        <li><strong>Data structures:</strong> Working with lists and dictionaries</li>
                        <li><strong>Built-in functions:</strong> Leveraging Python's powerful standard library</li>
                    </ul>
                </div>
            </div>
            """,
            'exercises': f"""
            <div class="module-content">
                <h3>🏋️ Hands-on Exercises</h3>
                <p>Practice what you've learned in <strong>{module_title}</strong> with these interactive exercises!</p>
                
                <div class="exercise">
                    <h4>Exercise 1: Basic Implementation</h4>
                    <div class="exercise-description">
                        <p><strong>Task:</strong> Create a Python program that demonstrates the concepts from this module.</p>
                        <p><strong>Requirements:</strong></p>
                        <ul>
                            <li>Use appropriate Python syntax</li>
                            <li>Include comments explaining your code</li>
                            <li>Test your code with different inputs</li>
                            <li>Handle potential errors gracefully</li>
                        </ul>
                    </div>
                    
                    <div class="starter-code">
                        <h5>Starter Code:</h5>
                        <pre><code class="python">
# Your code here
def main():
    # Implement your solution
    pass

if __name__ == "__main__":
    main()
                        </code></pre>
                    </div>
                </div>
                
                <div class="exercise">
                    <h4>Exercise 2: Problem Solving</h4>
                    <div class="exercise-description">
                        <p><strong>Challenge:</strong> Build a small project that combines multiple concepts.</p>
                        <ul>
                            <li>Design a solution approach</li>
                            <li>Implement step by step</li>
                            <li>Test thoroughly</li>
                            <li>Optimize for readability</li>
                        </ul>
                    </div>
                </div>
                
                <div class="tips">
                    <h4>💡 Tips for Success</h4>
                    <ul>
                        <li>Start with simple cases and build complexity gradually</li>
                        <li>Use meaningful variable names</li>
                        <li>Write small functions that do one thing well</li>
                        <li>Test your code frequently</li>
                    </ul>
                </div>
            </div>
            """,
            'quiz': f"""
            <div class="module-content">
                <h3>🧠 Knowledge Assessment</h3>
                <p>Test your understanding of <strong>{module_title}</strong> concepts!</p>
                
                <div class="quiz-info">
                    <h4>📋 Quiz Overview</h4>
                    <ul>
                        <li><strong>Questions:</strong> 10 multiple-choice questions</li>
                        <li><strong>Time Limit:</strong> 15 minutes</li>
                        <li><strong>Passing Score:</strong> 70%</li>
                        <li><strong>Attempts:</strong> Unlimited</li>
                    </ul>
                </div>
                
                <div class="quiz-topics">
                    <h4>🎯 Topics Covered</h4>
                    <ul>
                        <li>Core concepts from this module</li>
                        <li>Practical applications</li>
                        <li>Best practices</li>
                        <li>Common pitfalls to avoid</li>
                    </ul>
                </div>
                
                <div class="preparation">
                    <h4>📚 How to Prepare</h4>
                    <ol>
                        <li>Review the theory section thoroughly</li>
                        <li>Practice with the code examples</li>
                        <li>Complete all exercises</li>
                        <li>Understand the why behind each concept</li>
                    </ol>
                </div>
                
                <div class="quiz-action">
                    <button class="btn btn-primary btn-lg" onclick="startQuiz()">
                        🚀 Start Quiz
                    </button>
                    <p class="text-muted mt-2">Make sure you're ready before starting!</p>
                </div>
            </div>
            """
        },
        'javascript': {
            'description': f"Explore {module_title.replace('Module ', '').replace(': ', ' - ')} in JavaScript. Learn modern JavaScript concepts essential for web development.",
            'theory': f"""
            <div class="module-content">
                <h3>📚 JavaScript Fundamentals</h3>
                <p>Welcome to <strong>{module_title}</strong> in JavaScript!</p>
                
                <div class="learning-objectives">
                    <h4>🎯 What You'll Learn</h4>
                    <ul>
                        <li>JavaScript syntax and core concepts</li>
                        <li>Modern ES6+ features</li>
                        <li>DOM manipulation techniques</li>
                        <li>Asynchronous programming patterns</li>
                    </ul>
                </div>
                
                <div class="key-concepts">
                    <h4>🔑 Core JavaScript Concepts</h4>
                    <ul>
                        <li><strong>Variables & Scope:</strong> let, const, var and scope rules</li>
                        <li><strong>Functions:</strong> Arrow functions, callbacks, closures</li>
                        <li><strong>Objects & Arrays:</strong> Data manipulation and methods</li>
                        <li><strong>DOM Interaction:</strong> Selecting and modifying elements</li>
                    </ul>
                </div>
                
                <div class="modern-features">
                    <h4>⚡ Modern JavaScript</h4>
                    <p>We'll focus on contemporary JavaScript practices including:</p>
                    <ul>
                        <li>Template literals and destructuring</li>
                        <li>Promises and async/await</li>
                        <li>Modules and import/export</li>
                        <li>Functional programming concepts</li>
                    </ul>
                </div>
            </div>
            """,
            'examples': f"""
            <div class="module-content">
                <h3>💻 JavaScript in Action</h3>
                
                <div class="code-example">
                    <h4>Example 1: Modern JavaScript Syntax</h4>
                    <pre><code class="javascript">
// Modern JavaScript example for {module_title}
const students = [
    {{ name: 'Alice', grade: 85 }},
    {{ name: 'Bob', grade: 92 }},
    {{ name: 'Charlie', grade: 78 }}
];

// Using arrow functions and array methods
const topStudents = students
    .filter(student => student.grade >= 80)
    .map(student => `${{student.name}}: ${{student.grade}}%`)
    .join(', ');

console.log(`Top students: ${{topStudents}}`);
                    </code></pre>
                </div>
                
                <div class="code-example">
                    <h4>Example 2: DOM Manipulation</h4>
                    <pre><code class="javascript">
// Interactive web page example
document.addEventListener('DOMContentLoaded', () => {{
    const button = document.querySelector('#myButton');
    const output = document.querySelector('#output');
    
    button.addEventListener('click', async () => {{
        try {{
            const data = await fetchUserData();
            output.innerHTML = `Welcome, ${{data.name}}!`;
        }} catch (error) {{
            output.innerHTML = 'Error loading data';
        }}
    }});
}});

async function fetchUserData() {{
    // Simulated API call
    return new Promise(resolve => {{
        setTimeout(() => resolve({{ name: 'User' }}), 1000);
    }});
}}
                    </code></pre>
                </div>
            </div>
            """
        },
        'java': {
            'description': f"Deep dive into {module_title.replace('Module ', '').replace(': ', ' - ')} with Java. Master object-oriented programming and enterprise development patterns.",
            'theory': f"""
            <div class="module-content">
                <h3>📚 Java Programming Concepts</h3>
                <p>Master <strong>{module_title}</strong> in Java programming!</p>
                
                <div class="learning-objectives">
                    <h4>🎯 Learning Goals</h4>
                    <ul>
                        <li>Object-oriented programming principles</li>
                        <li>Java syntax and best practices</li>
                        <li>Exception handling and debugging</li>
                        <li>Collections and data structures</li>
                    </ul>
                </div>
                
                <div class="java-features">
                    <h4>☕ Java Fundamentals</h4>
                    <ul>
                        <li><strong>Classes & Objects:</strong> Building blocks of Java</li>
                        <li><strong>Inheritance:</strong> Code reuse and polymorphism</li>
                        <li><strong>Interfaces:</strong> Contracts and abstraction</li>
                        <li><strong>Packages:</strong> Organizing large applications</li>
                    </ul>
                </div>
            </div>
            """
        }
    }
    
    # Default template for other languages
    default_template = {
        'description': f"Learn {module_title.replace('Module ', '').replace(': ', ' - ')} concepts and practical applications in {language}.",
        'theory': f"""
        <div class="module-content">
            <h3>📚 {language.title()} Fundamentals</h3>
            <p>Welcome to <strong>{module_title}</strong>!</p>
            
            <div class="learning-objectives">
                <h4>🎯 What You'll Learn</h4>
                <ul>
                    <li>Core {language} concepts and syntax</li>
                    <li>Best practices and conventions</li>
                    <li>Practical problem-solving skills</li>
                    <li>Real-world applications</li>
                </ul>
            </div>
            
            <div class="key-concepts">
                <h4>🔑 Key Topics</h4>
                <p>This module covers essential {language} programming concepts that form the foundation for advanced development.</p>
            </div>
        </div>
        """,
        'examples': f"""
        <div class="module-content">
            <h3>💻 Code Examples</h3>
            <p>Practical examples demonstrating {module_title} concepts in {language}.</p>
            
            <div class="code-example">
                <h4>Example: Basic Implementation</h4>
                <pre><code>
// {language} example for {module_title}
// Your code examples will go here
                </code></pre>
            </div>
        </div>
        """,
        'exercises': f"""
        <div class="module-content">
            <h3>🏋️ Practice Exercises</h3>
            <p>Apply what you've learned with hands-on {language} exercises!</p>
            
            <div class="exercise">
                <h4>Exercise: Implement Core Concepts</h4>
                <p>Create a {language} program that demonstrates the key concepts from this module.</p>
            </div>
        </div>
        """,
        'quiz': f"""
        <div class="module-content">
            <h3>🧠 Knowledge Check</h3>
            <p>Test your understanding of {module_title} concepts!</p>
            
            <div class="quiz-info">
                <ul>
                    <li>Multiple choice questions</li>
                    <li>Immediate feedback</li>
                    <li>Unlimited attempts</li>
                </ul>
            </div>
            
            <button class="btn btn-primary" onclick="startQuiz()">Start Quiz</button>
        </div>
        """
    }
    
    return content_templates.get(language.lower(), default_template)

if __name__ == '__main__':
    create_module_content()
