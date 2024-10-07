MATCH (potentialDuplicate)-->(sourceProject)
WHERE NOT potentialDuplicate.duplicate
RETURN sourceProject.id AS id1, potentialDuplicate.id AS id2
