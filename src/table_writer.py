"""
Module for writing tables to storage locations
"""
import json

class FileWriter:
    def __init__(self, file_type:str):
        self.file_type = file_type
        file_path_lookup = dict()

        file_path_lookup = {
            "column": r"data\column.csv",
            "dashboard": r"data\dashboard.csv",
            "dataset": r"rdata\dataset.csv",
            "dataflow": r"data\dataflow.csv",
            "datamart": r"data\datamart.csv",
            "report": r"data\report.csv",
            "user": r"data\user.csv",
            "workspace": r"data\workspace.csv",
            "datasourceUsage": r"data\datasourceUsage.csv",
            "endorsementDetail": r"data\endorsementDetails.csv",
            "expression": r"data\expression.csv",
            "measure": r"data\measure.csv",
            "member": r"data\member.csv",
            "role": r"data\role.csv",
            "table": r"data\table.csv",
            "tablePermission": r"data\tablePermission.csv",
            "upstreamDataflow": r"data\upstreamDataflow.csv"
        }

        # lookup file path for file type
        self.file_path = file_path_lookup[file_type]



    def write_file(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f)

    def line_exists(self, line:str):
        with open(self.file_path, 'r') as f:
            for l in f:
                if line in l:
                    return True
        return False
    
    def append_line_to_file(self, line:str):
        with open(self.file_path, 'a') as f:
            f.write(line)

    def write_file_to_blob(self):
        pass

    def write_file_to_adls(self):
        pass

    def write_file_to_sql(self):
        pass

    def write_file_to_cosmos(self):
        pass

    def write_file_to_table(self):
        pass



class TableWriter:
    def __init__(self, data:dict, storage_account:str, storage_key:str, container:str):
        self.data = data
        self.storage_account = storage_account
        self.storage_key = storage_key
        self.container = container

    def write_table(self):
        pass

    def write_table_to_blob(self):
        pass

    def write_table_to_adls(self):
        pass

    def write_table_to_sql(self):
        pass

    def write_table_to_cosmos(self):
        pass

    def write_table_to_table(self):
        pass


# quick test
fw = FileWriter(file_type='column')