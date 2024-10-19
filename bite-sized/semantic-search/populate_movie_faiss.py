import os
import faiss
import tarfile
import requests
import pandas as pd
from tqdm import tqdm
from uuid import uuid4
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore



def download_and_extract_movie_dataset():
    """
    Download and extracts the CMU Movie Summary Corpus
    
    https://www.cs.cmu.edu/~ark/personas/
    """
    
    url = 'https://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz'
    filename = 'MovieSummaries.tar.gz'

    response = requests.get(url, stream=True)

    with open('MovieSummaries.tar.gz', 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    with tarfile.open(filename, 'r:gz') as tar:
        tar.extractall()


def load_and_preprocess_summaries(movie_dataset_dir='MovieSummaries'):
    """
    Load and preprocess movie summaries
    """

    summaries = pd.read_csv(os.path.join(movie_dataset_dir, 'plot_summaries.txt'), sep='\t', header=None)

    summaries.columns = ['wikipedia_id', 'plot_summary']
    
    return summaries

    

def load_and_preprocess_metadata(movie_dataset_dir='MovieSummaries'):
    """
    Load and preprocess movie metadata
    """

    def _metadata_dict_to_list(str_dict):
        return list(eval(str_dict).values())

    metadata = pd.read_csv(os.path.join(movie_dataset_dir, 'movie.metadata.tsv'), sep='\t', header=None)

    metadata.columns = ['wikipedia_id', 'freebase_id', 'name',
                        'release_date', 'box_office', 'runtime',
                        'languages', 'countries', 'genres']
    
    
    metadata['languages'] = metadata['languages'].apply(_metadata_dict_to_list)
    metadata['countries'] = metadata['countries'].apply(_metadata_dict_to_list)
    metadata['genres'] = metadata['genres'].apply(_metadata_dict_to_list)

    metadata = metadata.drop(columns=['freebase_id'])

    return metadata


def load_and_preprocess_characters(movie_dataset_dir='MovieSummaries'):
    """
    Load and preprocess movie character metadata
    """
    
    characters = pd.read_csv(os.path.join(movie_dataset_dir, 'character.metadata.tsv'), sep='\t', header=None)

    characters = characters.drop(columns=[10, 11, 12])  # drop unknown columns

    characters.columns = ['wikipedia_id', 'freebase_id', 'release_date',
                          'character_name', 'dob', 'gender', 'height', 'ethnicity',
                          'actor_name', 'age_at_movie_release']
    
    return characters


def merge_tables(summaries, metadata, characters):
    """
    Extract useful info from characters and metadata dataframes and merge them into summary dataframe
    """

    # Get list of actors per movie
    actors = characters.groupby('wikipedia_id')['actor_name'].unique()
    actors.name = 'actors'
    
    # Merge actors into metadata table
    metadata = pd.merge(metadata, actors, how='left', left_on='wikipedia_id', right_index=True)
    
    # Merge metadata (with actors) into summary table
    movies = pd.merge(summaries, metadata, on='wikipedia_id').drop(columns='wikipedia_id')

    return movies


def load_and_preprocess_movie_data(movie_dataset_dir='MovieSummaries'):
    """
    This function:
        1. loads the movie data in 3 dataframes (summaries, metadata, characters)
        2. preprocesses the above dataframes by removing redundant columns and giving them their proper names
        3. merge useful info from all tables into one
    """
    
    summaries = load_and_preprocess_summaries(movie_dataset_dir=movie_dataset_dir)
    metadata = load_and_preprocess_metadata(movie_dataset_dir=movie_dataset_dir)
    characters = load_and_preprocess_characters(movie_dataset_dir=movie_dataset_dir)
    
    movies = merge_tables(summaries, metadata, characters)
    
    return movies
    

def init_faiss():
    """
    Initialize the FAISS vector store
    """
    
    embeddings = HuggingFaceEmbeddings()  # by default uses 'sentence-transformers/all-mpnet-base-v2'
    # Langchain HuggingFace wrapper documentation:
    # https://api.python.langchain.com/en/latest/embeddings/langchain_community.embeddings.huggingface.HuggingFaceEmbeddings.html

    index = faiss.IndexFlatL2(len(embeddings.embed_query('hello world')))  # 768-dim embeddings by default

    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    
    return vector_store


def add_batch_to_vector_store(batch, store):
    """
    Add a batch of summaries and their metadata to the vector store
    """
    
    documents = []
    
    for i, row in batch.iterrows():

        doc = Document(page_content=row['plot_summary'],
                       metadata=row.drop(columns='plot_summary').to_dict())

        documents.append(doc)

    uuids = [str(uuid4()) for _ in range(len(documents))]

    store.add_documents(documents=documents, ids=uuids)

    
def populate_vector_store(movie_df, vector_store, batch_size=500):
    """
    Populate vector store with data from the movie dataframe, batch-by-batch
    """

    for i in tqdm(range(0, len(movies), batch_size)):

        add_batch_to_vector_store(movies[i:i+BATCH_SIZE], vector_store)
        

        
if __name__ == '__main__':
    BATCH_SIZE = 500
    FAISS_SAVE_DIR = 'movie_faiss'

    print('Downloading CMU movie data...')
    download_and_extract_movie_dataset()
    
    print('Loading and preprocessing data...')
    movies = load_and_preprocess_movie_data()
    
    print(f'Loaded {len(movies)} movies')
    print('Features:', movies.columns)
    
    vector_store = init_faiss()
    
    print('Created FAISS vector store')
    print(' |_ Embedding model:', vector_store.embedding_function.model_name)
    print(' |_ Embeddings dim:', vector_store.index.d)
    
    print(f'Populating vector store in batches of {BATCH_SIZE}...')
    populate_vector_store(movies, vector_store, batch_size=BATCH_SIZE)

    print(f'Vectors indexed in FAISS: {vector_store.index.ntotal}')
    
    print('Saving FAISS index under:', FAISS_SAVE_DIR)
    vector_store.save_local(FAISS_SAVE_DIR)
