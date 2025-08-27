from db import (
    save_progress as db_save_progress,
    save_emotion as db_save_emotion,
    get_student_data as db_get_student_data
)


def save_progress(user_id, course_id, status):
    db_save_progress(user_id, course_id, status)


def save_emotion(user_id, emotion, timestamp):
    db_save_emotion(user_id, emotion, timestamp)


def get_student_data(user_id):
    return db_get_student_data(user_id)


def analyze_learning_state(emotions, duration_minutes):
    """Analyze learning state based on emotions over time"""
    if not emotions:
        return "unknown"
    
    # Count emotion frequencies
    emotion_counts = {}
    for emotion in emotions:
        emotion_counts[emotion['emotion']] = emotion_counts.get(emotion['emotion'], 0) + 1
    
    # Calculate dominant emotion
    dominant_emotion = max(emotion_counts, key=emotion_counts.get)
    total_emotions = len(emotions)
    
    # Define learning states based on emotion patterns
    positive_emotions = ['very_focused', 'focused', 'happy', 'excited']
    negative_emotions = ['very_confused', 'confused', 'frustrated', 'bored']
    
    confusion_ratio = sum(emotion_counts.get(e, 0) for e in ['slightly_confused', 'confused', 'very_confused']) / total_emotions
    engagement_ratio = sum(emotion_counts.get(e, 0) for e in ['very_focused', 'focused']) / total_emotions
    
    if confusion_ratio > 0.5:
        return "needs_help"
    elif engagement_ratio > 0.6:
        return "good_progress"
    elif dominant_emotion in positive_emotions:
        return "engaged"
    elif dominant_emotion in negative_emotions:
        return "struggling"
    else:
        return "neutral"
