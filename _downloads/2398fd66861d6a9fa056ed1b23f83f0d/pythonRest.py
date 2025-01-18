import requests

# helper function to raise exception if the REST endpoint returns an
# unexpected status code
def assert_response_ok(response, message):
    if not response.ok:
        raise Exception(
            message + "\nStatus received={}\n{}".format(response.status_code, response.text))

rdfox_server = "http://localhost:12110"

# Create the data store
response = requests.post(
    rdfox_server + "/datastores/family")
assert_response_ok(response, "Failed to create datastore.")

# Add facts
turtle_data = """
@prefix : <https://rdfox.com/getting-started/> .

:peter :forename "Peter" ;
    a :Person ;
    :marriedTo :lois ;
    :gender "male" .

:lois :forename "Lois" ;
    a :Person ;
    :gender "female" .

:meg :forename "Meg" ;
    a :Person ;
    :hasParent :lois, :peter ;
    :gender "female" .

:chris :forename "Chris" ;
    a :Person ;
    :hasParent :peter ;
    :gender "male" .

:stewie :forename "Stewie" ;
    a :Person ;
    :hasParent :lois ;
    :gender "male" .

:brian :forename "Brian" . # Brian is a dog
"""


payload = {'operation': 'add-content-update-prefixes'}
response = requests.patch(
    rdfox_server + "/datastores/family/content", params=payload, data=turtle_data)
assert_response_ok(response, "Failed to add facts to data store.")

# Issue select query
sparql_text = "SELECT ?p ?n WHERE { ?p a :Person . ?p :forename ?n }"
response = requests.get(
    rdfox_server + "/datastores/family/sparql", params={"query": sparql_text})
assert_response_ok(response, "Failed to run select query.")
print("== Initial query result ==")
print(response.text)

# Issue insert
sparql_insert = "INSERT { ?x :marriedTo ?y } WHERE { ?y :marriedTo ?x }"
response = requests.post(
    rdfox_server + "/datastores/family/sparql", data={"update": sparql_insert})
assert_response_ok(response, "Failed to insert fact via sparql.")

# Add rule
datalog_rule = "[?p, :hasChild, ?c] :- [?c, :hasParent, ?p] ."
response = requests.post(
    rdfox_server + "/datastores/family/content", data=datalog_rule)
assert_response_ok(response, "Failed to add rule.")

# Query to confirm rule
sparql_text = "SELECT ?p ?c WHERE { ?p :hasChild ?c }"
response = requests.get(
    rdfox_server + "/datastores/family/sparql", params={"query": sparql_text})
assert_response_ok(response, "Failed to run select query.")
print("== Query for derived facts ==")
print(response.text)

# Delete fact
datalog_text = "[:stewie, :hasParent, :lois] ."
response = requests.patch(
    rdfox_server + "/datastores/family/content", params={"operation": "delete-content"}, data=datalog_text)
assert_response_ok(response, "Failed to delete fact.")

# Query to confirm derived facts updated (stewie is no longer a child of lois)
sparql_text = "SELECT ?p ?c WHERE { ?p :hasChild ?c }"
response = requests.get(
    rdfox_server + "/datastores/family/sparql", params={"query": sparql_text})
assert_response_ok(response, "Failed to run select query.")
print("== Query for updated derived facts ==")
print(response.text)
