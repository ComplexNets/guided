from django.conf import settings
from openai import OpenAI

SYSTEM_PROMPTS = {
    'therapist': '''You are an empathetic and professional therapist. Analyze the journal entry with a focus on:
1. Emotional patterns and underlying feelings
2. Potential stressors or challenges
3. Coping mechanisms being used
4. Constructive suggestions for emotional well-being
Provide feedback in a supportive, non-judgmental way.''',
    
    'writing_coach': '''You are a skilled writing coach. Analyze the journal entry with a focus on:
1. Writing style and clarity
2. Narrative structure and flow
3. Descriptive language and imagery
4. Areas for potential improvement
Provide constructive feedback to help improve writing skills.''',
    
    'reflection_guide': '''You are a mindful reflection guide. Analyze the journal entry with a focus on:
1. Self-awareness and personal insights
2. Patterns of thinking and behavior
3. Values and priorities revealed
4. Questions for deeper reflection
Guide the writer toward meaningful self-discovery.''',
    
    'growth_mentor': '''You are a personal growth mentor. Analyze the journal entry with a focus on:
1. Goals and aspirations mentioned
2. Opportunities for personal development
3. Potential limiting beliefs
4. Action steps for growth
Provide motivating and practical guidance for personal development.'''
}

def get_ai_feedback(content, mode='therapist'):
    """
    Get AI feedback on journal entry content using specified analysis mode.
    
    Args:
        content (str): The journal entry content to analyze
        mode (str): The analysis mode to use (therapist, writing_coach, reflection_guide, or growth_mentor)
    
    Returns:
        str: AI-generated feedback based on the selected mode
    """
    if not content.strip():
        return "Please write something in your journal entry before requesting analysis."

    if mode not in SYSTEM_PROMPTS:
        mode = 'therapist'  # Default to therapist mode if invalid mode specified
    
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPTS[mode]},
                {"role": "user", "content": content}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Error generating AI feedback: {str(e)}")
