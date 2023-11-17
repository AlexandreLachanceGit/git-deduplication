MATCH (parent:repository)
OPTIONAL MATCH (child:repository)
WHERE parent.id = child.parent_id
CREATE (child)-[:FORKED]->(parent);

