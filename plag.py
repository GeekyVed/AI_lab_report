import heapq
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# Download necessary NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def levenshtein_distance(s1, s2):
    len_s1, len_s2 = len(s1) + 1, len(s2) + 1
    matrix = np.zeros((len_s1, len_s2))
    
    for x in range(len_s1):
        matrix[x, 0] = x
    for y in range(len_s2):
        matrix[0, y] = y

    for x in range(1, len_s1):
        for y in range(1, len_s2):
            cost = 0 if s1[x-1] == s2[y-1] else 1
            matrix[x, y] = min(matrix[x-1, y] + 1,     # deletion
                               matrix[x, y-1] + 1,     # insertion
                               matrix[x-1, y-1] + cost) # substitution
    return matrix[len_s1-1, len_s2-1]

def preprocess(text):
    stop_words = set(stopwords.words('english'))
    sentences = sent_tokenize(text.lower())
    processed_sentences = []
    
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tokens = [t for t in tokens if t.isalnum() and t not in stop_words]
        processed_sentences.append(" ".join(tokens))
    
    return processed_sentences

def similarity_score(s1, s2):
    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    return 1 - (distance / max_len)

def a_star_plagiarism_detection(H, H_o):
    H_preprocessed = preprocess(H)
    H_o_preprocessed = preprocess(H_o)
    
    open_set = [(0, (0, 0))]
    heapq.heapify(open_set)
    
    g_score = {(0, 0): 0}
    f_score = {(0, 0): len(H_preprocessed) + len(H_o_preprocessed)}
    
    came_from = {}
    alignments = []

    while open_set:
        _, (i, j) = heapq.heappop(open_set)
        
        if i == len(H_preprocessed) and j == len(H_o_preprocessed):
            break
        
        neighbors = [(i+1, j), (i, j+1), (i+1, j+1)]
        for next_i, next_j in neighbors:
            if next_i <= len(H_preprocessed) and next_j <= len(H_o_preprocessed):
                tentative_g_score = g_score[(i, j)]
                
                if next_i > i and next_j > j:
                    sim = similarity_score(H_preprocessed[i], H_o_preprocessed[j])
                    tentative_g_score += 1 - sim
                    
                    # Adjust the threshold for similarity
                    if sim >= 0.4:  
                        alignments.append((H_preprocessed[i], H_o_preprocessed[j], sim))
                
                else:
                    tentative_g_score += 1

                if (next_i, next_j) not in g_score or tentative_g_score < g_score[(next_i, next_j)]:
                    came_from[(next_i, next_j)] = (i, j)
                    g_score[(next_i, next_j)] = tentative_g_score
                    f_score[(next_i, next_j)] = tentative_g_score + (len(H_preprocessed) - next_i) + (len(H_o_preprocessed) - next_j)
                    heapq.heappush(open_set, (f_score[(next_i, next_j)], (next_i, next_j)))
    
    return alignments

def compare_files(file1, file2):
    H = read_txt_file(file1)
    H_o = read_txt_file(file2)
    
    alignments = a_star_plagiarism_detection(H, H_o)
    
    total_sentences_H = len(sent_tokenize(H))
    total_sentences_H_o = len(sent_tokenize(H_o))
    
    plagiarism_percentage = (len(alignments) / min(total_sentences_H, total_sentences_H_o)) * 100

    print(f"Total sentences in file 1: {total_sentences_H}")
    print(f"Total sentences in file 2: {total_sentences_H_o}")
    print(f"Number of similar sentences: {len(alignments)}")
    print(f"Plagiarism Percentage: {plagiarism_percentage:.2f}%")
    print("\nDetected Alignments:")
    for i, (s1, s2, sim) in enumerate(alignments, 1):
        print(f"{i}. Similarity: {sim:.2f}")
        print(f"   File 1: {s1}")
        print(f"   File 2: {s2}")
        print()

# Example usage:
file1 = 'D:\\file1.txt'  # Path to your first .txt file
file2 = 'D:\\file2.txt'  # Path to your second .txt file
compare_files(file1, file2)
