SELECT m1.*
FROM measurements m1
JOIN (
    SELECT type, MAX(time) AS max_time
    FROM measurements
    WHERE node_id = your_node_id
    GROUP BY type
) m2 ON m1.type = m2.type AND m1.time = m2.max_time
WHERE m1.node_id = your_node_id;