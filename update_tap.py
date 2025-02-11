import json

class TAP:
    """
    A class to update the TAP (template) JSON file using the corpus data.

    Attributes:
        origin (str): The origin of the corpus data.
        corpus_file (str): The filename for the corpus JSON.
        tap_file_in (str): The filename for the input TAP JSON.
        tap_file_out (str): The filename for the updated TAP JSON.
    """

    def __init__(self, origin: str, corpus_file: str,
                 tap_file_in: str = "/home/evlossio/myprojects/corpus/DATA/medicamentos.tap",
                 tap_file_out: str = "/home/evlossio/myprojects/corpus/backup/default_out.tap"):
        """
        Initialize the TAP object with file paths.

        Args:
            corpus_file (str): Path to the corpus JSON file.
            tap_file_in (str): Path to the input TAP JSON file.
            tap_file_out (str): Path to the output TAP JSON file.
        """
        self.origin = origin
        self.corpus_file = corpus_file
        self.tap_file_in = tap_file_in
        self.tap_file_out = tap_file_out
        self.corpus = {}
        self.tap = {}

    def load_corpus(self) -> None:
        """
        Load the corpus data from the specified JSON file.
        """
        with open(self.corpus_file, "r", encoding="utf-8") as file:
            self.corpus = json.load(file)

    def load_tap(self) -> None:
        """
        Load the TAP data from the specified JSON file.
        """
        with open(self.tap_file_in, "r", encoding="utf-8") as file:
            self.tap = json.load(file)

    def update_library_terms(self) -> None:
        """
        Update the terms in the first library of the TAP file using the corpus data.
        
        For each key in the corpus:
            - Create a new term with the key as 'form' and its synonyms as objects.
            - Append the new term to the 'terms' list of the library.
        """
        # Retrieve the library from the TAP JSON structure
        library = self.tap.get("template", {}).get("libraries", [])[0]
        if "terms" not in library or not isinstance(library["terms"], list):
            library["terms"] = []

        # Update library terms using corpus data
        for form_key, synonyms_list in self.corpus.items():
            # Only include non-empty synonyms
            synonyms_objects = [syn for syn in synonyms_list if syn]
            new_term = {
                "form": form_key,
                "synonyms": {
                    "terms": [{"form": syn, "match": 0, "typeid": 1, "inflected": True} for syn in synonyms_objects]
                },
                "typeid": 1,
                "inflected": True,
                "isAddSingleTerms": 2
            }
            library["terms"].append(new_term)

    def save_tap(self) -> None:
        """
        Save the updated TAP data to the specified output JSON file with indentations.
        """
        with open(self.tap_file_out, "w", encoding="utf-8") as file:
            json.dump(self.tap, file, ensure_ascii=False, indent=4)

    def run_update(self) -> None:
        """
        Execute the complete update process:
            1. Load corpus data.
            2. Load TAP data.
            3. Update library terms in TAP data with corpus entries.
            4. Save the updated TAP data.
            5. Print a confirmation message.
        """
        self.load_corpus()
        self.load_tap()
        self.update_library_terms()
        self.save_tap()
        print(f"{self.tap_file_out} created successfully to be used in the IBM Cloud Pak for Data - SPSS Modeler flow!")

if __name__ == "__main__":
    ORIGEM = "abcfarma"
    CORPUS_FILE = f"/home/evlossio/myprojects/corpus/{ORIGEM}_corpus.json"
    tap = TAP(origin=ORIGEM, 
              corpus_file=CORPUS_FILE, 
              tap_file_in="/home/evlossio/myprojects/corpus/DATA/medicamentos.tap",
              tap_file_out=f"/home/evlossio/myprojects/corpus/{ORIGEM}.tap")
    tap.run_update()