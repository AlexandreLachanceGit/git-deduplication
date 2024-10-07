LOAD CSV FROM 'file:///scores_full.csv' AS row

WITH toInteger(row[0]) AS id1, toInteger(row[1]) AS id2, toFloat(row[2]) AS similarity

WHERE similarity >= 0.75
MATCH (a:repository {id: id1})
MATCH (b:repository {id: id2})

SET b.duplicate = true
