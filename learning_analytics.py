from datetime import datetime, timedelta
import numpy as np
from db import get_student_data, get_recent_emotions

def analyze_emotion_patterns(emotions, time_window_minutes=30):
    """Analyze emotion patterns over time with weighted recent emotions"""
    if not emotions:
        return {
            'dominant_emotion': 'unknown',
            'stability': 0,
            'trend': 'neutral'
        }
    
    # Weight recent emotions more heavily
    weights = np.linspace(0.5, 1.0, len(emotions))
    emotion_weights = {}
    
    for emotion, weight in zip(emotions, weights):
        emotion_weights[emotion] = emotion_weights.get(emotion, 0) + weight
    
    # Calculate dominant emotion
    dominant_emotion = max(emotion_weights.items(), key=lambda x: x[1])[0]
    
    # Calculate emotional stability
    unique_emotions = len(emotion_weights)
    stability = 1.0 - (unique_emotions / len(emotions))
    
    # Determine emotional trend
    recent_window = emotions[-min(5, len(emotions)):]
    positive_emotions = ['very_focused', 'focused', 'happy', 'excited']
    negative_emotions = ['very_confused', 'confused', 'frustrated', 'bored']
    
    positive_count = sum(1 for e in recent_window if e in positive_emotions)
    negative_count = sum(1 for e in recent_window if e in negative_emotions)
    
    if positive_count > negative_count:
        trend = 'improving'
    elif negative_count > positive_count:
        trend = 'declining'
    else:
        trend = 'stable'
    
    return {
        'dominant_emotion': dominant_emotion,
        'stability': stability,
        'trend': trend
    }

def calculate_learning_effectiveness(emotion_patterns, progress_data):
    """Calculate learning effectiveness score based on emotions and progress"""
    base_score = 70  # Base score
    
    # Adjust for emotional stability
    stability_factor = emotion_patterns['stability'] * 10
    
    # Adjust for emotional trend
    trend_adjustment = {
        'improving': 10,
        'stable': 0,
        'declining': -10
    }.get(emotion_patterns['trend'], 0)
    
    # Adjust for progress
    progress_factor = (progress_data['completed_topics'] / progress_data['total_topics']) * 20
    
    # Calculate final score
    effectiveness_score = base_score + stability_factor + trend_adjustment + progress_factor
    
    return max(0, min(100, effectiveness_score))

def generate_adaptive_recommendations(user_id):
    """Generate personalized recommendations based on learning analytics"""
    student_data = get_student_data(user_id)
    recent_emotions = get_recent_emotions(user_id)
    
    emotion_patterns = analyze_emotion_patterns([e['emotion'] for e in recent_emotions])
    effectiveness_score = calculate_learning_effectiveness(
        emotion_patterns,
        {
            'completed_topics': student_data['completed_topics'],
            'total_topics': student_data['total_topics']
        }
    )
    
    recommendations = {
        'learning_pace': 'standard',
        'content_format': 'mixed',
        'break_interval': 30,
        'suggested_activities': []
    }
    
    # Adjust recommendations based on effectiveness score
    if effectiveness_score < 50:
        recommendations.update({
            'learning_pace': 'reduced',
            'content_format': 'visual',
            'break_interval': 20,
            'suggested_activities': [
                'Review fundamental concepts',
                'Try interactive exercises',
                'Watch video tutorials'
            ]
        })
    elif effectiveness_score > 80:
        recommendations.update({
            'learning_pace': 'accelerated',
            'content_format': 'advanced',
            'break_interval': 45,
            'suggested_activities': [
                'Tackle challenging problems',
                'Explore advanced topics',
                'Help peers with questions'
            ]
        })
    
    return recommendations