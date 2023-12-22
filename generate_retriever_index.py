import pandas as pd
import numpy as np
import ftfy, re
import html
import os, sys 
import pickle 

from sentence_transformers import SentenceTransformer
from faiss import read_index

# initialize sentence transformer model
# model = SentenceTransformer('bert-base-nli-mean-tokens')
model = SentenceTransformer('msmarco-distilbert-base-v4')

offers_df = pd.read_csv('assets/offers_df.csv')

with open('assets/lists.pickle', 'rb') as f:
  lists = pickle.load(f)

with open('assets/embeddings.pickle', 'rb') as f:
  embeddings = pickle.load(f)

indexes = {}
for name in lists.keys():
  indexes[name] = read_index(f'assets/indexes/{name}.index')

def embed_input(inputs):
  embeddings = model.encode(inputs)
  embeddings /= np.expand_dims(np.linalg.norm(embeddings, ord=2, axis=-1), axis=1)
  return embeddings

def get_offers(query):
  query_embedding = embed_input([query])

  search_order = ['brand', 'retailer', 'category', 'parent_category', 'offer']
  results = {}
  for name in search_order:
    index = indexes[name]
    dists, indices = index.search(query_embedding, 10)
    results[name] = []
    for idx, dist in zip(indices[0], dists[0]):
      if idx>=0:
        matched_phrase = lists[name][idx]
        if matched_phrase == '':
          continue
        results[name].append((matched_phrase, dist, idx))

  retrieved_indices = set()
  scores = {}

  for name in search_order:
    # print('name:', name)
    for phrase, dist, idx in results[name]:
      if dist < 1:
        retrieved_indices.add(idx)
        if idx not in scores.keys():
          scores[idx] = min(1/dist, 100)
          scores[idx] = np.log(scores[idx]+1)
        # print(phrase,'|', lists['offer'][idx], '|', dist)
    # print()

  # print('name: offer')
  for phrase, dist, idx in results['offer']:
    if dist < 1.25:
      retrieved_indices.add(idx)
      if idx not in scores.keys():
        scores[idx] = min(1/dist, 100)
        scores[idx] = np.log(1+scores[idx])
      # print(phrase,'|', '|', dist)
  # print()

  retrieved_indices = list(retrieved_indices)
  score_col = [(idx, scores[idx]) for idx in retrieved_indices]
  # print(score_col)
  score_col.sort(key=lambda x : x[1], reverse=True)
  # print(score_col)
  retrieved_indices = [idx for idx, score in score_col]
  scores = [score for idx, score in score_col]
  retrieved_offers = offers_df.iloc[retrieved_indices]
  retrieved_offers['SCORE'] = scores
  retrieved_offers = retrieved_offers[['OFFER', 'RETAILER', 'BRAND', 'PRODUCT_CATEGORY', 'SCORE']]
  return retrieved_offers

#   print(retrieved_offers)

# def get_offers(query):
#   query_embedding = embed_input([query])

#   d, i = index.search(query_embedding, 10)
#   # print(d, i)

#   returned_offers = set()

#   outputs = []

#   for dist, iidx in zip(d[0], i[0]):
#     if iidx>=0:
#       phrase = all_phrases[iidx]
#       if phrase == '' or dist>0.6:
#         continue
#       offer_idx = phrases_to_offers[phrase]
#       if offer_idx not in returned_offers:
#         returned_offers.add(offer_idx)
#         # print('offer:',only_offers[offer_idx])
#         # print('phrase:',phrase, 'dist:', dist)
#         # print()

#         outputs.append((only_offers[offer_idx], dist))
#   return outputs

# def print_outputs(outputs):
#   if len(outputs) == 0:
#     print('No offers')
#     return 
#   for offer, dist in outputs:
#     print('offer:', offer, 'score:', 1-dist)
#     print()

