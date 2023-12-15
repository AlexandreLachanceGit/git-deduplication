MATCH (n)
SET n.duplicate = false;

MATCH (sourceProject)-->(potentialDuplicate)
WHERE potentialDuplicate.commit_ids[0] IN sourceProject.commit_ids
SET potentialDuplicate.duplicate = true
