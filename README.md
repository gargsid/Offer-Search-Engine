# Offer Search Engine
Take home assignement for Data Science Apprenticeship role.

In this project, we create an offer retrieval engine, where we are given a table of offers on variety of products from different retailers and brands. We are also given a separated table of brands and the categories of the product they sell. 

The user can make a natural language query to get offers on product categories, brands, or retailers. We have used entity linking, LLM powered semantic search and vector stores to create an end-to-end pipeline for supporting natural langauge queries. 

For a detailed and thorough walkthrough please check out this [colab notebook](https://colab.research.google.com/drive/1mPlrVPMt0RpHWzDGojipjX4D5ov0Y9rN?usp=sharing) 

## Instructions

To install the dependencies, please use

```
pip install -r requirements.txt
```

[Optional] You can also clone the environment using the provided yaml file. For doing that use

```
conda env create -f environment.yml
conda activate env
```

`env` is the name of the environment. You can change the name by editing `environment.yml` file

### Running the app

To run the code interactively in streamlit app, use

```
streamlit run app.py
```

You can make your queries. An example is shown below. 

<p float="left">
  <img src="https://github.com/gargsid/Offer-Search-Engine/blob/main/assets/app_screenshot.png" width="2000" height="300" />
</p> 
