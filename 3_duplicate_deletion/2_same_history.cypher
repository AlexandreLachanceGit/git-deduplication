MATCH (n)
SET n.duplicate = false;

MATCH (potentialDuplicate)-->(sourceProject)
WHERE potentialDuplicate.commit_ids[0] IN sourceProject.commit_ids
SET potentialDuplicate.duplicate = true

// 1412 results
