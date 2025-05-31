from .config import init_gemini, AVAILABLE_MODELS
from .prompt_builder import build_story_prompt
import time

def generate_story_chunk(title: str, part_number: int, total_parts: int, previous_parts: list[str], model_name: str) -> str:
    try:
        model = init_gemini(model_name)
        prompt = build_story_prompt(title, part_number, total_parts, previous_parts)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating story part {part_number}: {str(e)}"

def generate_complete_horror_story(title: str, total_parts: int = 3, model_name: str = 'gemini-2.0-flash-exp') -> str:
    story_parts = []
    summaries = []  # Store summaries of previous parts
    
    for part in range(1, total_parts + 1):
        chunk = generate_story_chunk(title, part, total_parts, summaries, model_name)
        story_parts.append(chunk)
        
        # Generate a brief summary of this part for context in next generation
        if part < total_parts:
            try:
                model = init_gemini(model_name)
                summary_prompt = f"Berikan ringkasan singkat (maksimal 400 kata) dari bagian awal paragraf, isi paragraf dan akhir paragraf cerita berikut untuk menjaga kontinuitas:\n\n{chunk}"
                summary = model.generate_content(summary_prompt).text
                summaries.append(summary)
                time.sleep(2)  # Add small delay between requests
            except Exception as e:
                summaries.append(f"Bagian {part}: {chunk[:400]}...")  # Use first 200 chars as fallback
    
    return "\n\n".join(story_parts)