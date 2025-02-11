# %%
import os
import json
import pandas as pd
import numpy as np
import openpyxl
import spacy
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')


class Corpus:
    """
    A class used to manage the creation and storage of a corpus from a pharmaceutical dataset.

    Attributes
    ----------
    nlp : spacy.lang
        The spaCy language model used for text normalization.
    dataset_path : str
        Path to the dataset file.
    corpus_path : str
        Destination path for the saved corpus JSON file.
    """

    def __init__(self, termo: str, sinonimo: str, origem: str, dataset_path: str, corpus_path: str):
        """
        Initialize the Corpus object by loading necessary language models and setting file paths.

        Parameters
        ----------
        dataset_path : str
            Path to the dataset file (CSV or XLSX file).
        corpus_path : str
            Destination path for the output corpus JSON file.
        """
        self.termo = termo
        self.sinonimo = sinonimo
        self.origem = origem
        self.dataset_path = dataset_path
        self.corpus_path = corpus_path
        self.nlp = spacy.load('pt_core_news_sm')

    def load_dataset(self) -> pd.DataFrame:
        """
        Loads the dataset from an Excel file.

        Returns
        -------
        DataFrame
            Loaded dataset contained in a pandas DataFrame.
        """
        return pd.read_excel(self.dataset_path, sheet_name='Planilha1')

    
    def preprocess_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocesses the dataset by renaming columns to lowercase, handling missing values,
        and standardizing text in specific columns.

        Parameters
        ----------
        df : DataFrame
            The DataFrame containing the original dataset.

        Returns
        -------
        DataFrame
            The preprocessed DataFrame.
        """
        # Rename all columns to lowercase and standardize text
        [df.rename(columns={coluna: coluna.lower()}, inplace=True) for coluna in df.columns]     
        for coluna in df.columns:
            
            if df[coluna].dtype == 'object':
                df[coluna] = df[coluna].str.lower()
                
        return df
    
    
    def clean_dataset(self, cols, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocesses the dataset by renaming columns to lowercase, handling missing values,
        and standardizing text in specific columns.

        Parameters
        ----------
        df : DataFrame
            The DataFrame containing the original dataset.

        Returns
        -------
        DataFrame
            The cleaned DataFrame.
        """
        # Remove rows with missing required fields
        df.dropna(subset=cols, inplace=True)

        return df

    
    def get_synonyms(self, word: str) -> list:
        """
        Retrieves a list of synonyms for a given word using NLTK's WordNet.

        Parameters
        ----------
        word : str
            The word for which to find synonyms.

        Returns
        -------
        list
            A list of synonyms.
        """
        synonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name().lower())
        return synonyms

    def normalize_text(self, text: str) -> str:
        """
        Normalizes text by lemmatizing (obtaining the base form of words) using spaCy,
        while filtering out stop words and non-alphabetic tokens.

        Parameters
        ----------
        text : str
            The text to be normalized.

        Returns
        -------
        str
            The normalized text.
        """
        doc = self.nlp(text)
        normalized = ' '.join(token.lemma_ for token in doc if not token.is_stop and token.is_alpha)
        return normalized

    
    def create_corpus(self, df: pd.DataFrame) -> dict:
        """
        Creates a corpus from the DataFrame where the keys are active principles 
        and the values are sorted lists of names containing each active principle.

        Parameters
        ----------
        df : DataFrame
            The preprocessed DataFrame containing at least 'nome' and 'princ_ativo' columns.

        Returns
        -------
        dict
            A dictionary of the corpus.
        """
        corpus = {}
        for _, row in df.iterrows():
            princip_active = row[self.sinonimo]
            nome = row[self.termo]
            if princip_active in corpus:
                corpus[princip_active].add(nome)
            else:
                corpus[princip_active] = {nome}
        # Return dictionary with sorted keys and sorted names lists
        return {k: sorted(list(v)) for k, v in sorted(corpus.items())}

    def save_corpus(self, corpus: dict, output_path: str) -> None:
        """
        Saves the corpus as a JSON file converting any sets in the corpus to lists.

        Parameters
        ----------
        corpus : dict
            The corpus dictionary to be saved.
        output_path : str
            The output file path for the JSON file.
        """
        serializable_corpus = {k: list(v) if isinstance(v, set) else v for k, v in corpus.items()}
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(serializable_corpus, f, ensure_ascii=False, indent=4)

    def run(self) -> None:
        """
        Executes the full processing pipeline: loading, preprocessing, corpus creation,
        saving the corpus, and saving the preprocessed dataset to a Parquet file.
        """
        if not os.path.exists(self.dataset_path):
            print(f"Error: File '{self.dataset_path}' not found!")
            return

        # Load and preprocess dataset
        df = self.load_dataset()
        df = self.preprocess_dataset(df)
        df = self.clean_dataset([self.termo, self.sinonimo], df)
        
        # Create and save corpus
        corpus = self.create_corpus(df)
        self.save_corpus(corpus, self.corpus_path)
        print(f"Corpus salvo em {self.corpus_path}")

        # Save the preprocessed DataFrame as a Parquet file
        df.to_parquet(f'{self.origem}.parquet', index=False)


if __name__ == "__main__":
    # Define dataset and output corpus paths
    TERMO = 'nome'
    SINONIMO = 'composição'
    ORIGEM = 'abcfarma'
    DATASET_FILE = '/home/evlossio/myprojects/corpus/DATA/EANS_NAO_CRUZARAM.xlsx'
    CORPUS_FILE = f'/home/evlossio/myprojects/corpus/{ORIGEM}_corpus.json'
        
    abcfarma = Corpus(termo=TERMO, 
                         sinonimo=SINONIMO,
                         origem=ORIGEM, 
                         dataset_path=DATASET_FILE, 
                         corpus_path=CORPUS_FILE)
    abcfarma.run()
