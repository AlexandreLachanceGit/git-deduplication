MATCH (b:repository), (a:repository)
WHERE
()-->(a)
AND NOT (a)-->()
AND NOT ()-->(b)
AND NOT (b)-->()
AND last(a.commit_ids) = last(b.commit_ids)
CREATE (b)-[:CLONED_PUSHED]->(a)
