LOAD CSV FROM 'file:///scores.csv' AS row

WITH toInteger(row[0]) AS id1, toInteger(row[1]) AS id2, toFloat(row[2]) AS similarity

WHERE similarity >= 0.7
MATCH (a:repository {id: id1})
MATCH (b:repository {id: id2})

CREATE (b)-[:SIMILAR {score: similarity}]->(a)
