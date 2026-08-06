from pyspark.sql import Row
from pyspark.sql.functions import regexp_extract
from pyspark.sql.dataframe import DataFrame

def bytes_to_megabytes(bytes:int) -> float:
    return bytes / (1024 ** 2)

def bytes_to_gigabytes(byte_count:int) -> float:
    return byte_count / (1024 ** 3)

def create_size_dataframe(file_paths:list) -> DataFrame:
    """
    Given a list of file paths of pyspark tables, create a dataframe listing the table_name, location, and size used by each table
    """
    table_pattern = r"Tables/([^/]+)$"
    rows = []

    for fp in file_paths:
        table_name = re.search(table_pattern, fp).group(1)
        
        temp_df = spark.sql(f"DESCRIBE DETAIL '{fp}'")
    
        new_row = Row(
            table=table_name,
            location=temp_df.select("location").collect()[0][0],
            sizeInBytes=temp_df.select("sizeInBytes").collect()[0][0],
            MB = bytes_to_megabytes(temp_df.select("sizeInBytes").collect()[0][0]),
            GB = bytes_to_gigabytes(temp_df.select("sizeInBytes").collect()[0][0])
        )
        rows.append(new_row)

    size_df = spark.createDataFrame(rows)

    return size_df
