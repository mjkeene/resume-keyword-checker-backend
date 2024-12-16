import json

def extract_keywords(text):
    # Split the text into words and filter out short words
    words = {word.lower() for word in text.split() if word.isalnum() and len(word) > 2}
    return words

def compare_keywords(resume_text, job_description_text):
    # Extract keywords from both texts
    resume_keywords = extract_keywords(resume_text)
    job_desc_keywords = extract_keywords(job_description_text)
    
    # Find missing keywords
    missing_keywords = job_desc_keywords - resume_keywords
    return missing_keywords

def lambda_handler(event, context):
    try:
        # Parse input from the event body
        body = json.loads(event.get('body', '{}'))
        resume_text = body.get('resume', '')
        job_description_text = body.get('job_description', '')
        
        if not resume_text or not job_description_text:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Both resume and job description are required'})
            }

        # Perform keyword comparison
        missing_keywords = compare_keywords(resume_text, job_description_text)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'missing_keywords': list(missing_keywords)
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

