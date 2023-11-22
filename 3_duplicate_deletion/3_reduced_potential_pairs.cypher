MATCH (sourceProject)-->(potentialDuplicate)
WHERE NOT sourceProject.duplicate
RETURN sourceProject, potentialDuplicate


