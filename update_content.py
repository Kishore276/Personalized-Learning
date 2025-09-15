from db import get_connection

def update_module_content():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all submodules
    cursor.execute('SELECT id, title, module_id FROM submodules')
    submodules = cursor.fetchall()
    
    for submodule in submodules:
        sub_id, title, module_id = submodule
        
        # Get module info
        cursor.execute('SELECT title, course_id FROM modules WHERE id = ?', (module_id,))
        module_info = cursor.fetchone()
        
        if module_info:
            module_title, course_id = module_info
            
            # Get course info
            cursor.execute('SELECT language FROM courses WHERE id = ?', (course_id,))
            course_info = cursor.fetchone()
            language = course_info[0] if course_info else 'general'
            
            # Generate content based on submodule type
            if 'Theory' in title:
                content = f"""
                <div class="theory-content">
                    <h3>📚 {title}</h3>
                    <p>Welcome to the theoretical foundation of <strong>{module_title}</strong>!</p>
                    
                    <h4>🎯 Learning Objectives</h4>
                    <ul>
                        <li>Understand core {language} concepts</li>
                        <li>Learn fundamental principles</li>
                        <li>Build theoretical knowledge</li>
                        <li>Prepare for practical application</li>
                    </ul>
                    
                    <h4>📖 What You'll Study</h4>
                    <p>This section covers the essential theoretical concepts that form the foundation of {module_title}. You'll learn the why behind the concepts before diving into practical implementation.</p>
                    
                    <div class="key-points">
                        <h5>Key Points to Remember:</h5>
                        <ul>
                            <li>Focus on understanding concepts deeply</li>
                            <li>Take notes on important principles</li>
                            <li>Ask questions if anything is unclear</li>
                            <li>Connect theory to real-world applications</li>
                        </ul>
                    </div>
                </div>
                """
            elif 'Examples' in title:
                content = f"""
                <div class="examples-content">
                    <h3>💻 {title}</h3>
                    <p>See <strong>{module_title}</strong> concepts in action with practical {language} examples!</p>
                    
                    <h4>🔍 What You'll See</h4>
                    <ul>
                        <li>Real {language} code examples</li>
                        <li>Step-by-step explanations</li>
                        <li>Common use cases</li>
                        <li>Best practice demonstrations</li>
                    </ul>
                    
                    <div class="example-preview">
                        <h5>Example Preview:</h5>
                        <pre><code>
# {language} example for {module_title}
def example_function():
    # Your code examples will be here
    print("Learning {language} is fun!")
    return True
                        </code></pre>
                    </div>
                    
                    <div class="study-tips">
                        <h5>💡 Study Tips:</h5>
                        <ul>
                            <li>Run the examples in your own environment</li>
                            <li>Modify the code to see what happens</li>
                            <li>Understand each line of code</li>
                            <li>Connect examples back to theory</li>
                        </ul>
                    </div>
                </div>
                """
            elif 'Exercises' in title:
                content = f"""
                <div class="exercises-content">
                    <h3>🏋️ {title}</h3>
                    <p>Practice your <strong>{module_title}</strong> skills with hands-on {language} exercises!</p>
                    
                    <h4>🎯 Exercise Goals</h4>
                    <ul>
                        <li>Apply theoretical knowledge</li>
                        <li>Build practical coding skills</li>
                        <li>Solve real programming problems</li>
                        <li>Gain confidence in {language}</li>
                    </ul>
                    
                    <div class="exercise-types">
                        <h5>Types of Exercises:</h5>
                        <ul>
                            <li><strong>Coding Challenges:</strong> Write {language} code to solve problems</li>
                            <li><strong>Debug Tasks:</strong> Find and fix errors in existing code</li>
                            <li><strong>Project Tasks:</strong> Build small applications</li>
                            <li><strong>Creative Problems:</strong> Design your own solutions</li>
                        </ul>
                    </div>
                    
                    <div class="getting-started">
                        <h5>🚀 Getting Started:</h5>
                        <ol>
                            <li>Read the exercise instructions carefully</li>
                            <li>Plan your approach before coding</li>
                            <li>Write code step by step</li>
                            <li>Test your solution thoroughly</li>
                            <li>Review and optimize your code</li>
                        </ol>
                    </div>
                </div>
                """
            elif 'Quiz' in title:
                content = f"""
                <div class="quiz-content">
                    <h3>🧠 {title}</h3>
                    <p>Test your understanding of <strong>{module_title}</strong> concepts!</p>
                    
                    <h4>📋 Quiz Information</h4>
                    <ul>
                        <li><strong>Questions:</strong> 10 multiple-choice questions</li>
                        <li><strong>Time Limit:</strong> 15 minutes</li>
                        <li><strong>Passing Score:</strong> 70%</li>
                        <li><strong>Attempts:</strong> Unlimited retakes</li>
                    </ul>
                    
                    <div class="quiz-topics">
                        <h5>📚 Topics Covered:</h5>
                        <ul>
                            <li>Core concepts from {module_title}</li>
                            <li>Practical applications</li>
                            <li>{language} best practices</li>
                            <li>Problem-solving approaches</li>
                        </ul>
                    </div>
                    
                    <div class="preparation">
                        <h5>📖 How to Prepare:</h5>
                        <ol>
                            <li>Complete all theory sections</li>
                            <li>Study the code examples</li>
                            <li>Finish the practice exercises</li>
                            <li>Review key concepts</li>
                        </ol>
                    </div>
                    
                    <div class="quiz-tips">
                        <h5>💡 Quiz Tips:</h5>
                        <ul>
                            <li>Read questions carefully</li>
                            <li>Think through each option</li>
                            <li>Use process of elimination</li>
                            <li>Don't rush - you have time</li>
                        </ul>
                    </div>
                </div>
                """
            else:
                content = f"""
                <div class="general-content">
                    <h3>📚 {title}</h3>
                    <p>Learn important concepts in <strong>{module_title}</strong>!</p>
                    
                    <h4>What You'll Learn</h4>
                    <ul>
                        <li>Essential {language} programming concepts</li>
                        <li>Practical skills and techniques</li>
                        <li>Best practices and conventions</li>
                        <li>Real-world applications</li>
                    </ul>
                </div>
                """
            
            # Update the submodule with content
            cursor.execute('UPDATE submodules SET content = ? WHERE id = ?', (content, sub_id))
    
    conn.commit()
    conn.close()
    print("All module content updated successfully!")

if __name__ == '__main__':
    update_module_content()
