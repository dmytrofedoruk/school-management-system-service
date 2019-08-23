from google.cloud import bigquery

# creating Client object
client = bigquery.Client()

# creating dataset reference
dataset_ref = client.dataset('dataset_name', project='project_name')

# API request, fetch the dataset
dataset = client.get_dataset(dataset_ref)

# list all the tables in the dataset
tables = list(client.list_tables(dataset))

# print the name of all tables in the dataset
for table in tables:
	print(table.table_id)

# construct a reference to the 'table' table
table_ref = dataset_ref.table('table_name')

# API request - fetch the table
table = client.get_table(table_ref)

# print information on all the columns in the 'table_name' table 
# in the 'dataset_name' dataset
table.schema

# preview the first five line of the 'table_name' table
client.list_rows(table, max_results=5).to_dataframe()
