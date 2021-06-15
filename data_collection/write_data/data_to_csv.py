import os.path
import pandas as pd
import csv

class DataToCSV:
    """
    Represents a class to write a stream of data to csv file

    Attributes
    ----------
    file (str)
        name of file to write to
    field_names (list)
        names of fields in csv file header
    unique_identifiers (list)
        names of fields to uniquely identify the data, for
        prevention of duplicates
    file_exist (bool)
        whether the file given exists in the system
    df (pd.DataFrame)
        dataframe object of current csv file
    
    Methods
    ----------
    write(data_stream):
        iterable of key value pairs corresponding to
        field_names to write to file
    __contains_data(data):
        checks whether current file contains given data,
        based on list of unique_identifiers
    """
    def __init__(self, file, field_names, unique_identifiers=[]):
        """
        Constructor for a DataToCSV instance

        Parameters:
            file (str): name of file to write to
            field_names (list): names of fields in csv file header
            unique_identifiers (list), optional: list of field names that
            uniquely identifies the data in the file
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
        """
        Writes given data to csv file 

        Parameters:
            data_stream (iterable): iterable of dictionaries with keys corresponding
            to field_names of current instance, and values to be written to file

        Raises:
            AttributeError: If keys of data given do not match field_names

        Returns:
            number of new rows written to the csv file
        """
        columns = set(self.field_names)
        rows_written = 0
        for data in data_stream:
            # Ensure set of dictionary keys is equal to field names of current instance,
            # to prevent unexpected behaviour on pd.DataFrame.append
            if (set(data.keys()) == columns):
                if not self.__contains_data(data):
                    self.df = self.df.append(data, ignore_index=True)
                    rows_written += 1
            else: 
                raise AttributeError("Keys of data do not match field names of csv file")
        
        self.df.to_csv(self.file, index=False, quoting=csv.QUOTE_NONNUMERIC)
        return rows_written


    def __contains_data(self, data):
        """
        Checks whether current csv file contains given data. Duplicate is checked
        based on data having equal values for all fields under unique_identifiers

        Parameters:
            data (dict): data to check for duplicate

        Returns:
            True if current csv file contains given data, False otherwise. If
            unique_identifiers is an empty list (default), returns False
        """
        if len(self.unique_identifiers) == 0:
            return False
        # Filter current dataframe based on values of given data
        # corresponding to each unique identifier
        filtered_df = self.df
        for field in self.unique_identifiers:
            filtered_df = filtered_df.loc[filtered_df[field] == data[field]]
        return len(filtered_df) > 0