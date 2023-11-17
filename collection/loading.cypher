CALL apoc.load.json("file:///full.json") YIELD value
WITH value AS repo
UNWIND repo AS r
CALL apoc.create.node(["repository"], {
    forge: r.forge, 
    id: r.id, 
    name: r.name, 
    full_name: r.full_name,
    description: r.description,
    created_at: datetime(r.created_at),
    updated_at: datetime(r.updated_at),
    allow_forking: r.allow_forking,
    forks_count: r.forks_count,
    stars: r.stars,
    owner_id: r.owner_id,
    owner_username: r.owner_username,
    commit_ids: r.commit_ids,
    fork: r.fork,
    parent_id: r.parent_id,
    parent_name: r.parent_name,
    parent_full_name: r.parent_full_name,
    parent_creator_id: r.parent_creator_id,
    source_id: r.source_id,
    source_name: r.source_name,
    source_full_name: r.source_full_name,
    source_creator_id: r.source_creator_id
    }) YIELD node
RETURN node;

