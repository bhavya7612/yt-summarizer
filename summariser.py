from transformers import pipeline, T5Tokenizer
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

# def chunk_text(text, max_chunk_size=1024):
#     # Split the text into chunks with a maximum size of `max_chunk_size` tokens
#     chunks = []
#     words = text.split()
#     current_chunk = []
#     current_chunk_size = 0

#     for word in words:
#         current_chunk.append(word)
#         current_chunk_size += len(word) + 1  # Word length + space
#         if current_chunk_size > max_chunk_size:
#             chunks.append(" ".join(current_chunk))
#             current_chunk = []
#             current_chunk_size = 0

#     # Add the last chunk if any
#     if current_chunk:
#         chunks.append(" ".join(current_chunk))

#     return chunks

def abstractive_summarization(transcript_text, max_len):

    # summarizer = pipeline('summarization',model='t5-small')
    # chunks=chunk_text(transcript_text)
    # summaries = []
    # for chunk in chunks:
    #     chunk_summary=summarizer(chunk, min_length=30, max_length=max_len, length_penalty=1.5, do_sample=False)
    #     summaries.append(chunk_summary[0]['summary_text'])
    
    # final_summary=" ".join(summaries)
    # return final_summary

    # --------------------OR-----------------------

    summarizer = pipeline('summarization',model='t5-small')
    summary=''
    # tokenizer = T5Tokenizer.from_pretrained('t5-small')
    # input_ids = tokenizer.encode(transcript_text, return_tensors='pt', truncation=True)

    # chunk_size = 512
    # chunks = [input_ids[0][i:i + chunk_size] for i in range(0, len(input_ids[0]), chunk_size)]
    # for chunk in chunks:
    #     chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
    #     summary_text = summarizer(chunk_text, max_length=max_len, truncation=True)[0]['summary_text']
    #     summary += summary_text + ' '
    
    for i in range(0, (len(transcript_text)//500) + 1):
        summary_text = summarizer(transcript_text[i * 500:(i+1) * 500], max_length=max_len)[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary

    #---------------------OR-------------------------

    # summarizer = pipeline('summarization', model='t5-small')
    # chunk_size = 1000
    # summary_parts = []

    # # Summarize each chunk
    # for i in range(0, (len(transcript_text) // chunk_size) + 1):
    #     chunk = transcript_text[i * chunk_size : (i + 1) * chunk_size]
    #     if chunk.strip():  # Ensure the chunk isn't empty
    #         summary_text = summarizer(chunk, max_length=100, truncation=True)[0]['summary_text']
    #         summary_parts.append(summary_text)

    # # Combine chunk summaries into an intermediate summary
    # intermediate_summary = ' '.join(summary_parts)

    # # Re-summarize the intermediate summary to fit max_len
    # final_summary = summarizer(intermediate_summary, max_length=max_len, truncation=True)[0]['summary_text']

    # return final_summary

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

