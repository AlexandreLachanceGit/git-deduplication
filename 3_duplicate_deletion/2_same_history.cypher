MATCH (sourceProject)-->(potentialDuplicate)
WHERE toStringList(sourceProject.commit_ids)[0] = toStringList(potentialDuplicate.commit_ids)[0]
SET potentialDuplicate.duplicate = true
