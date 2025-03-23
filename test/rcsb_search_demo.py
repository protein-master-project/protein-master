from rcsbapi.search import AttributeQuery, TextQuery
from rcsbapi.search import search_attributes as attrs

# Construct a "full-text" sub-query for structures associated with the term "Hemoglobin"
q1 = TextQuery(value="Hemoglobin")

# Construct an "attribute" sub-query to search for structures from humans
q2 = AttributeQuery(
    attribute="rcsb_entity_source_organism.scientific_name",
    operator="exact_match",  # Other operators include "contains_phrase", "exists", and more
    value="Homo sapiens"
)
# OR, do so by using Python bitwise operators:
q2 = attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens"

# Combine the sub-queries (can sub-group using parentheses and standard operators, "&", "|", etc.)
query = q1 & q2

# Fetch the results by iterating over the query execution
for rId in query():
    print(rId)

# OR, capture them into a variable
results = list(query())



# from rcsbapi.data import DataQuery as Query
# query = Query(
#     input_type="polymer_entities",
#     input_ids=["2CPK_1", "3WHM_1", "2D5Z_1"],
#     return_data_list=[
#         "polymer_entities.rcsb_id",
#         "rcsb_entity_source_organism.ncbi_taxonomy_id",
#         "rcsb_entity_source_organism.ncbi_scientific_name",
#         "cluster_id",
#         "identity"
#     ]
# )
# print(query.exec())