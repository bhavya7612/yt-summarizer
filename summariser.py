import os
import google.generativeai as genai
import re
import video_info
from dotenv import load_dotenv
load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def abstractive_summarization(transcript_text, max_len, temperature):
    prompt=f"You are Youtube transcript summarizer. Summarize the given transcript text within {max_len} words. The transcript text is:\n{transcript_text} "
    model=genai.GenerativeModel("gemini-1.5-flash")
    try:
        response=model.generate_content(
                prompt,
                generation_config = genai.GenerationConfig(
                        temperature = temperature
                )
            )
        return response.text
    except Exception as e:
        raise e

def summarise(video_id, max_len=150, temperature=0.2):
    try:
        transcript_text = video_info.get_video_transcript(video_id)
    except:
        return "No subtitles available for this video"

    summary = abstractive_summarization(transcript_text, max_len, temperature)

    return (summary, transcript_text)

def process_summary(summary):
    blocks = summary.strip().split("\n\n")  # Split by double newlines (paragraph separators)
    
    formatted_blocks = []
    bold_pattern = re.compile(r"\*\*(.*?)\*\*")  # Regex to find text within **double asterisks**

    for block in blocks:
        lines = block.strip().split("\n")  # Split by single newlines

        if all(re.match(r"^\s*[-•\d.]", line) for line in lines if line.strip()):
            # If all lines start with bullet points or numbers, treat as a list
            formatted_blocks.append({
                "type": "list",
                "content": [bold_pattern.sub(r"<strong>\1</strong>", line.strip("-• ").strip()) for line in lines]
            })
        else:
            # Otherwise, treat as a paragraph
            formatted_blocks.append({
                "type": "paragraph",
                "content": bold_pattern.sub(r"<strong>\1</strong>", block.strip())  # Replace **text** with <strong>text</strong>
            })

    return formatted_blocks


# from transformers import pipeline, T5Tokenizer
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.decomposition import TruncatedSVD
# from nltk.tokenize import sent_tokenize
# from youtube_transcript_api import YouTubeTranscriptApi
# from langdetect import detect
# import os
# import google.generativeai as genai
# import translator
# from dotenv import load_dotenv
# load_dotenv()

# def get_transcript(video_id):
#     try:
#         transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
#     except Exception as e:
#         raise e
#     transcript_text = ' '.join([d['text'] for d in transcript_list])
#     return transcript_text

# def is_transcript_english(transcript_text):
#     try:
#         language = detect(transcript_text)
#         return language == 'en'
#     except Exception as e:
#         return False

# def abstractive_summarization(transcript_text, lang, max_len):
#     api_key=os.getenv("GEMINI_API_KEY")
#     genai.configure(api_key=api_key)
#     prompt=f"You are Youtube transcript summarizer. Summarize the given transcript text within {max_len} words. The transcript text is:\n{transcript_text} "
#     model=genai.GenerativeModel("gemini-1.5-pro")
#     try:
#         response=model.generate_content(prompt)
#         response=translator.translate(response.text, lang)
#         return response
#     except Exception as e:
#         raise e

#     # --------------------OR-----------------------

#     # summarizer = pipeline('summarization',model='t5-small')
#     # summary=''

#     # for i in range(0, (len(transcript_text)//500) + 1):
#     #     summary_text = summarizer(transcript_text[i * 500:(i+1) * 500], max_length=max_len)[0]['summary_text']
#     #     summary = summary + summary_text + ' '
#     # return summary

# def extractive_summarization(transcript_text, lang):
#     try:
#         sentences = sent_tokenize(transcript_text)
        
#         # Vectorize sentences
#         vectorizer = CountVectorizer(stop_words='english')
#         X = vectorizer.fit_transform(sentences)
        
#         # Perform Truncated SVD for dimensionality reduction
#         svd = TruncatedSVD(n_components=1, random_state=42)
#         svd.fit(X)
#         components = svd.transform(X)
        
#         # Rank sentences based on the first singular vector
#         ranked_sentences = [item[0] for item in sorted(enumerate(components), key=lambda item: -item[1])]
        
#         # Select top sentences for summary
#         num_sentences = int(0.4 * len(sentences))  # 20% of the original sentences
#         selected_sentences = sorted(ranked_sentences[:num_sentences])
        
#         # Compile the final summary
#         summary = " ".join([sentences[idx] for idx in selected_sentences])

#         # Translate the summary into desired language
#         response=translator.translate(summary, lang)
#         return response
#     except Exception as e:
#         raise e

# def summarise(video_id, max_len=150, lang="en"):
#     try:
#         transcript_text = get_transcript(video_id)
#     except:
#         return "No subtitles available for this video"

#     # Extractive summarization using LSA or Frequency-based method
#     if len(transcript_text.split()) > 3000:
#         summary = extractive_summarization(transcript_text, lang)
#     else:
#         summary = abstractive_summarization(transcript_text, lang, max_len)

#     return summary