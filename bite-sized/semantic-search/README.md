# Semantic Search

This bite-sized course is a short intro to semantic search and vector databases.

For the demo we'll first populate a FAISS in-memory vector store with movie plot summaries and their metadata and then query them to find movies that we are interested in.

## How to run

1. Install dependencies:
	- requirements can be found in the `requirements.txt` file.
	- recommended way is through a virtual environment  
	```
	python -m venv semantic-search-env  # create the virtual env
	source semantic-search-env/bin/activate  # activate it
	pip install -r requirements.txt  # install pip dependencies to virtual env
	pip install ipykernel  
	python -m ipykernel install --user --name=semantic-search-env  # add virtual env to jupyter
	```  
	**Note**: If you have access to a GPU you might want to change the `faiss-cpu` package to `faiss-gpu`.
	
2. Create and populate the FAISS db:
	```
	python populate_movie_faiss.py
	```
	
3. Run the notebook with the demo queries

## Dataset

The dataset used in this demo is the [CMU Movie Summary Corpus](https://www.cs.cmu.edu/~ark/personas/). This dataset that consists of info about movies (name, release date, actors, etc.), along with their plot summaries.

