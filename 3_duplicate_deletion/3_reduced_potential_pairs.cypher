MATCH (potentialDuplicate)-->(sourceProject)
WHERE NOT sourceProject.duplicate
RETURN sourceProject.id AS id1, potentialDuplicate.id AS id2


