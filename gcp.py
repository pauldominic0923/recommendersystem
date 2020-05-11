from google.cloud import bigquery
client = bigquery.Client()

table_id = "context-aware-system.clothingData.zara1"

# schema = [
#     bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
#     bigquery.SchemaField("gender", "STRING", mode="REQUIRED"),
#     bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
#     bigquery.SchemaField("price_parse", "STRING", mode="REQUIRED"),
#     bigquery.SchemaField("product_link", "STRING", mode="REQUIRED"),
#     bigquery.SchemaField("img_link", "STRING", mode="REQUIRED")
# ]

# table = bigquery.Table(table_id, schema=schema)
# table = client.create_table(table)  # Make an API request.
# print(
#     "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
# )

table = client.get_table(table_id)  # Make an API request.
rows_to_insert = [(u"Phred Phlyntstone", 32), (u"Wylma Phlyntstone", 29)]

errors = client.insert_rows(table, rows_to_insert)  # Make an API request.
if errors == []:
    print("New rows have been added.")