import os.path
import pandas as pd
import csv

class DataToCSV:
    """Represents a class to write a stream of data to csv file.

    A class which takes in a stream of data in a dictionary and writes
    them to new csv file if the file does not exist, or appends to the
    existing csv file. The header of the csv files must be the same as
    the keys of the dictionary.

    Attributes:
        file (str): Name of file to write to
        field_names (list): Names of fields in csv file header
        unique_identifiers (list): Names of fields which uniquely identify 
            the data, for prevention of duplicates
        file_exist (bool): Whether the file given exists in the system
        df (pd.DataFrame): DataFrame object of current csv file
    
    """
    def __init__(self, file, field_names, unique_identifiers=[]):
        """Constructor for a DataToCSV instance.

        Args:
            file (str): Name of file to write to
            field_names (list): Names of fields in csv file header
            unique_identifiers (list, optional): list of field names that
                uniquely identifies the data in the file. Defaults to empty list

        Raises:
            AttributeError: If header of csv file does not match field names, or
                unique_identifiers are not subset of field names

        """
        self.file = file
        self.field_names = field_names
        self.unique_identifiers = unique_identifiers
        self.file_exists = os.path.isfile(self.file)
        self.df = pd.read_csv(self.file) if self.file_exists else pd.DataFrame(columns=self.field_names)
        # Error checking to confirm that:
        # 1. Header of read in csv file is same as field names passed in
        # 2. Unique identifiers are subset of field names
        if (not set(self.field_names) == set(self.df.columns)) or (not set(self.unique_identifiers) <= set(self.field_names)):
            raise AttributeError("Invalid field names/unique identifiers")


    def write(self, data_stream):
        """Writes given data to csv file.

        Writes given data stream of dictionary data to csv file.

        Args:
            data_stream (iterable): iterable of dictionaries with keys corresponding
                to field_names of current instance, and values to be written to file

        Returns:
            int: Number of new rows written to the csv file

        Raises:
            AttributeError: If keys of data given do not match field_names

        """
        columns = set(self.field_names)
        rows_written = 0
        for data in data_stream:
            # Ensure set of dictionary keys is equal to field names of current instance,
            # to prevent unexpected behaviour on pd.DataFrame.append
            if (set(data.keys()) == columns):
                if not self._contains_data(data):
                    self.df = self.df.append(data, ignore_index=True)
                    rows_written += 1
            else: 
                raise AttributeError("Keys of data do not match field names of csv file")
        
        self.df.to_csv(self.file, index=False, quoting=csv.QUOTE_NONNUMERIC)
        return rows_written


    def _contains_data(self, data):
        """Checks whether current dataframe instance contains given data.

        Returns True if current data exits in dataframe, False otherwise. 
        Duplicate is checked based on data having equal values for all 
        fields under unique_identifiers.

        Args:
            data (dict): Data to check for duplicate

        Returns:
            bool: If current csv file contains given data. 
                If unique_identifiers is an empty list (default), returns False

        """
        if len(self.unique_identifiers) == 0:
            return False
        # Filter current dataframe based on values of given data
        # corresponding to each unique identifier
        filtered_df = self.df
        for field in self.unique_identifiers:
            filtered_df = filtered_df.loc[filtered_df[field] == data[field]]
        return len(filtered_df) > 0
