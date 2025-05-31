import google.generativeai as genai

AVAILABLE_MODELS = [
    'gemini-1.0-pro',
    'gemini-1.5-flash',
    'gemini-1.5-flash-8b',
    'gemini-1.5-flash-8b-exp',
    'gemini-1.5-flash-exp',
    'gemini-1.5-pro',
    'gemini-1.5-pro-exp',
    'gemini-2.0-flash-exp'
]

def init_gemini(model_name='gemini-2.0-flash-exp'):
    if model_name not in AVAILABLE_MODELS:
        raise ValueError(f"Model {model_name} not supported")
    return genai.GenerativeModel(model_name)