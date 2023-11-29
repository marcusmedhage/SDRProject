

SELECT type, value, time
FROM measurements
WHERE node_id = nodeID
ORDER BY time DESC
LIMIT 1;