## Project Pipelines

For detailed solution and walkthrough please follow this [colab notebook](https://colab.research.google.com/drive/1mPlrVPMt0RpHWzDGojipjX4D5ov0Y9rN?usp=sharing) (recommended)

We are given 3 different tables -- offers, category, and brands

For the offers table we have offers, provided by brands, and retailers.

For the brands table, we have details of different product categories sold by different brands

For the category table, for each product category, we have a higher level category of the product. **Since the higher level categories are abstract, we do not consider the table in this project**. 

**Problem Statement**: Users can make natural language query about product category, brand or retailer to get offer on those products. 

**Solution Overview**

We have used entity linking, LLM powered semantic search and vector stores to create an end-to-end pipeline for supporting natural langauge queries.

**Entity Linking** 

For linking offers with the product categories, we left-joined the offers table with the brands table. 

**Text Representations and Vector Store**

We used `Sentence-Encoder` architecture with base model `msmarco-distilbert-base-v4` which is trained specifically for asymmetric semantic search where the query is short but the documents are long which suits our usecase ideally. 

We extract dense representations of the offers, brands, retailers, and product categories and stored them in an index using **FAISS** tool. FAISS is a approximate nearest neighbor search tool that can store millions of dense representations and efficiently retrieve the closest embedding vector given a query.

**Semantic Search for Offer Retrieval**

Given a query, we create its embedding using the Sentence-Encoder model. 

We first compare it to the embeddings from retailers, brands and product categories. If the embeddings are really close with respect to the Euclidean distance (`distance < 1`), then we retrieve the corresponding offer

Then we compare the query embedding to the embeddings of the offers and retrieve the offers that have `distance < 1.25`. (Thresholds chosen empirically). 

The sentence-encoders output the mean of all the token embeddings in a sentence as the sentence representaiton. By averaging the embeddings, we lose the fine-grained information about specific keywords that can be useful for a query. For example, kroger is present in multiple offer descriptions not in brands, or retailers columns. Therefore, it was important to keep the sentences short at the cost of multiple vector stores. 

### Tradeoffs and Assumptions

1. **Multiple vector stores**: We need multiple vector stores so that each embeddings can store meaningful fine-grained information about different kinds of entities. Here entities are brands, product categories, and retailers. 

2. **Static Vector Store**: FAISS created vector stores are fixed and cannot be changed or edited once created. Therefore, if we want to index a new entry, we have to create the whole index from scratch. However, static vector stores are cheaper than dynamic ones. 

3. **Embedding Model**: Our embedding model is powered by distilled version of pre-trained BERT model which can be computationally expensive to use. However, the quality of text embeddings of pre-trained BERT models or other LLMs are good and can lead to robust semantic search. To reduce the complexity without performance loss, several strategies like pruning, distillation, quantization, model sharding are used for efficient deployment on large-scale. 