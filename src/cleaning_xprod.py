import pandas as pd
import regex as re

class Cleaner:
    """
    A class used to clean and process a dataset from an Excel file.

    Attributes:
        input_file (str): The path to the input Excel file.
        output_file (str): The path to the output Excel file.
        patterns (dict): Dictionary of compiled regex patterns.
        df (pandas.DataFrame): DataFrame containing the input data.
    """

    def __init__(self, input_file, output_file):
        """
        Initialize the Cleaner with an input file and an output file.
        
        Args:
            input_file (str): Path to the Excel file to be loaded.
            output_file (str): Path to the Excel file to be saved after cleaning.
        """
        self.input_file = input_file
        self.output_file = output_file
        
        self.patterns = {
            'dose': re.compile(r'((\d+,)?\d+\s?(mg|g|ml|UI)(/\d?(mg|g|ml))?)', flags=re.IGNORECASE),
            'form': re.compile(r'(\s?(?:sach\w+|po|tab|cap|comp|cpr|susp|sol|inj|amp|xpe))', flags=re.IGNORECASE),
            'recipient': re.compile(r'\s*(bg|canet\w+|fa|fr|cx|env|pt)', flags=re.IGNORECASE)
        }

        self.df = None

    def extract_pattern(self, text, pattern):
        """
        Extracts a substring from text using the given regex pattern.
        
        Args:
            text (str): The text from which to extract the pattern.
            pattern (regex.Pattern): A compiled regex pattern.

        Returns:
            str or None: The extracted substring (stripped) if found, else None.
        """
        match = pattern.search(text)
        return match.group(0).strip() if match else None

    def remove_patterns(self, text):
        """
        Removes all occurrences of the regex patterns from text.
        
        Args:
            text (str): The text from which to remove the patterns.

        Returns:
            str: The text after removing all patterns.
        """
        for pattern in self.patterns.values():
            text = pattern.sub('', text)
        return text.strip()

    def load_data(self):
        """
        Loads data from the input Excel file into a pandas DataFrame.
        
        This method reads the Excel file specified in self.input_file and stores
        the resulting DataFrame in self.df.
        """
        try:
            self.df = pd.read_excel(self.input_file)
            self.df['DESCRIÇÃO'] = self.df['DESCRIÇÃO'].astype(str)  # Convert to string once
        except Exception as e:
            print(f"Error loading data: {e}")
            raise

    def process(self):
        """
        Processes the data by applying regex extractions and removals.
        
        The processing includes:
            1. Extracting dose, form, and recipient information into new columns.
            2. Removing all patterns from 'DESCRIÇÃO' to create a new column 'xprod_cleaned'.
            3. Reordering columns so that 'xprod_cleaned' is the last one.
        """

        # Extract patterns
        for key in self.patterns.keys():
            self.df[key] = self.df['DESCRIÇÃO'].apply(lambda x, pattern=self.patterns[key]: self.extract_pattern(x, pattern))

        # Remove all patterns and create a new column 'xprod_cleaned'
        self.df['xprod_cleaned'] = self.df['DESCRIÇÃO'].apply(self.remove_patterns)

        # Reorder columns
        self.df = self.df[[col for col in self.df.columns if col != 'xprod_cleaned'] + ['xprod_cleaned']]

    def save(self):
        """
        Saves the processed DataFrame to an Excel file.
        
        The resulting Excel file is saved to the location specified by self.output_file.
        """
        try:
            self.df.to_excel(self.output_file, index=False)
            print(f"Cleaning complete. Output saved to '{self.output_file}'")
        except Exception as e:
            print(f"Error saving data: {e}")
            raise

    def run(self):
        """
        Runs the cleaning process end-to-end.
        
        This method orchestrates the entire cleaning pipeline which includes:
          1. Loading data.
          2. Processing the data (applying regex operations).
          3. Saving the cleaned data to the output file.
        """
        self.load_data()
        self.process()
        self.save()

if __name__ == "__main__":
    input_file = '/home/evlossio/myprojects/corpus/data/EANS_NAO_CRUZARAM.xlsx'
    output_file = '/home/evlossio/myprojects/corpus/data/cleaned_file.xlsx'
    cleaner = Cleaner(input_file, output_file)
    cleaner.run()