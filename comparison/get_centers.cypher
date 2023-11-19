MATCH (n)
WHERE ()-->(n) 
AND NOT (n)-->()
RETURN n;

MATCH (a:repository), (b:repository)
WHERE
()-->(a)
AND NOT (a)-->()
AND NOT ()-->(b)
AND NOT (b)-->()
AND last(toStringList(a.commit_ids)) = last(toStringList(b.commit_ids))
CREATE (a)-[:CLONED_PUSHED]->(b)
