from django.conf import settings
from openai import OpenAI

GUIDED_PROMPTS = {
    'expressive_writing': {
        1: '''You are guiding a user through an Expressive Writing session focused on factual description.
Purpose: Help the user describe an event as objectively as possible.

Review their writing and provide feedback that:
1. Identifies the key factual elements present
2. Notes any missing important details (who, what, when, where)
3. Gently redirects if they include emotional content
4. Asks specific questions to help them complete the factual picture

Keep feedback focused on the objective details. Save emotional exploration for later sessions.''',

        2: '''You are guiding a user through an Expressive Writing session focused on emotional exploration.
Purpose: Help the user explore and understand their emotional response to the event.

Review their writing and provide feedback that:
1. Validates and acknowledges the emotions expressed
2. Identifies emotional patterns or themes
3. Explores both past (during event) and present emotions
4. Asks gentle questions to deepen emotional awareness

Create a safe space for emotional exploration while maintaining therapeutic boundaries.''',

        3: '''You are guiding a user through an Expressive Writing session focused on making connections.
Purpose: Help the user explore how this event connects to other experiences and influences.

Review their writing and provide feedback that:
1. Identifies recurring themes or patterns
2. Highlights connections to other life experiences
3. Notes potential influences on current behaviors/thoughts
4. Asks insightful questions about these connections

Encourage deeper reflection while maintaining a supportive, non-judgmental stance.''',

        4: '''You are guiding a user through the final Expressive Writing session focused on future growth.
Purpose: Help the user find closure and plan future steps.

Review their writing and provide feedback that:
1. Acknowledges their journey through the process
2. Highlights opportunities for reframing
3. Identifies specific growth opportunities
4. Suggests concrete steps forward

Focus on empowerment and practical next steps while honoring their experience.'''
    }
}

def get_guided_feedback(content, program_name, session_number, user=None):
    """
    Get AI feedback for a guided writing session.
    
    Args:
        content (str): The user's writing content
        program_name (str): Name of the guided program (e.g., 'expressive_writing')
        session_number (int): Current session number
        user (User): The user object to get profile information from
    
    Returns:
        str: AI-generated feedback specific to the guided writing session
    """
    if not content.strip():
        return "Please write something before requesting feedback."

    if program_name not in GUIDED_PROMPTS or session_number not in GUIDED_PROMPTS[program_name]:
        return "Invalid program or session number."
    
    # Get user profile information if available
    profile_context = ""
    if user and hasattr(user, 'userprofile'):
        profile = user.userprofile
        profile_context = f"""
User Profile Information:
- Age: {profile.age if profile.age else 'Not specified'}
- Personal Goals: {profile.goals if profile.goals else 'Not specified'}
- Values: {profile.values if profile.values else 'Not specified'}

Personality Dimensions (0-100 scale):
- Openness to Experience: {profile.openness}
- Conscientiousness: {profile.conscientiousness}
- Extraversion: {profile.extraversion}
- Agreeableness: {profile.agreeableness}
- Neuroticism: {profile.neuroticism}

Consider this profile information when providing feedback, especially regarding emotional sensitivity and growth orientation.
"""
    
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        messages = [
            {"role": "system", "content": GUIDED_PROMPTS[program_name][session_number]},
        ]
        
        # Add profile context if available
        if profile_context:
            messages.append({"role": "system", "content": profile_context})
            
        # Add the writing content
        messages.append({"role": "user", "content": content})
        
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating feedback: {str(e)}"
