CALL apoc.load.json("file:///more.json") YIELD value
WITH value AS repo
UNWIND repo AS r
CALL apoc.create.node(["repository"], {id: r.id, name: r.full_name}) YIELD node
RETURN node;

