import numpy as np
import pandas as pd

class DataSet:
    def __init__(self):
        self.data = pd.DataFrame()
        self.path = None
        self.separator = ","
        self.column = None
        self.current_description = None
        self.columns = self.data.columns
        self.read_data_success = False
        self.data_type = "modified-radio"
        self.modified_data = pd.DataFrame()
        self.modified_columns = None
        self.display_data = pd.DataFrame()
        self.range = None

    def describe_column_as_df(self):
        self.current_description = self.create_describe_table(self.data, self.column)

    def description_to_cols_rows_datatable(self):
        self.describe_column_as_df()
        cols = [{"name": i, "id": i} for i in self.current_description.columns]
        rows = self.current_description.to_dict('records')
        return cols, rows

    def get_data(self):
        try:
            self.data = pd.read_csv(self.path, sep=self.separator)
            self.columns = self.data.columns
            self.modified_data = self.data.copy(deep=True)
            self.modified_columns = self.modified_data.columns
            self.display_data = self.modified_data
            self.read_data_success = True
        except Exception as e:
            self.read_data_success = False
            print(e)

    def switch_display_data(self, data_type):
        self.data_type = data_type
        if self.data_type == "original-radio":
            self.display_data = self.data
        else:
            self.display_data = self.modified_data

    @staticmethod
    def create_describe_table(dat, colm):
        column_description = pd.DataFrame()
        column_description["count"] = [dat[colm].describe()[0]]
        try:
            column_description["mean"] = [dat[colm].describe()[1]]
            column_description["std"] = [dat[colm].describe()[2]]
            column_description["min"] = [dat[colm].describe()[3]]
            column_description["25%"] = [dat[colm].describe()[4]]
            column_description["50%"] = [dat[colm].describe()[5]]
            column_description["75%"] = [dat[colm].describe()[6]]
            column_description["max"] = [dat[colm].describe()[7]]
            column_description["NaN"] = [dat[colm].isnull().sum()]
        except:
            column_description["unique"] = [dat[colm].describe()[1]]
            column_description["top"] = [dat[colm].describe()[2]]
            column_description["freq"] = [dat[colm].describe()[3]]
        column_description["dtype"] = [str(dat[colm].describe().dtype)]
        return column_description

