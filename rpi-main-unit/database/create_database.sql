
CREATE TABLE devices (
    node_id TINYINT,
    name VARCHAR(32),
    desc VARCHAR(128),
    type VARCHAR(16),
    PRIMARY KEY (node_id)
);

CREATE TABLE measurements (
    node_id TINYINT,
    time VARCHAR(19),
    type VARCHAR(16),
    value INTEGER,
    PRIMARY KEY (node_id, time, type),
    FOREIGN KEY (node_id) REFERENCES devices(node_id)
);