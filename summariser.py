from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.tokenize import sent_tokenize
from youtube_transcript_api import YouTubeTranscriptApi
import numpy as np
from langdetect import detect

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        raise e
    transcript_text = ' '.join([d['text'] for d in transcript_list])
    return transcript_text

def is_transcript_english(transcript_text):
    try:
        language = detect(transcript_text)
        return language == 'en'
    except Exception as e:
        return False

def abstractive_summarization(transcript_text, max_len):
    summarizer = pipeline('summarization')
    summary = ''
    for i in range(0, (len(transcript_text)//1000) + 1):
        summary_text = summarizer(transcript_text[i * 1000:(i+1) * 1000], max_length=max_len)[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary

def extractive_summarization(transcript_text):
    sentences = sent_tokenize(transcript_text)
    
    # Vectorize sentences
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(sentences)
    
    # Perform Truncated SVD for dimensionality reduction
    svd = TruncatedSVD(n_components=1, random_state=42)
    svd.fit(X)
    components = svd.transform(X)
    
    # Rank sentences based on the first singular vector
    ranked_sentences = [item[0] for item in sorted(enumerate(components), key=lambda item: -item[1])]
    
    # Select top sentences for summary
    num_sentences = int(0.4 * len(sentences))  # 20% of the original sentences
    selected_sentences = sorted(ranked_sentences[:num_sentences])
    
    # Compile the final summary
    summary = " ".join([sentences[idx] for idx in selected_sentences])
    return summary

def summarise(video_id, max_len):
    try:
        transcript_text = get_transcript(video_id)
    except:
        return "No subtitles available for this video"

    # Extractive summarization using LSA or Frequency-based method
    if len(transcript_text.split()) > 3000:
        summary = extractive_summarization(transcript_text)
    else:
        summary = abstractive_summarization(transcript_text, max_len)

    return summary

