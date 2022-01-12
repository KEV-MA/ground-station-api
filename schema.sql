DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS ws;
DROP TABLE IF EXISTS hab;

CREATE TABLE device (
    id TEXT PRIMARY KEY,
    lat DECIMAL(10,2),
    long DECIMAL(10,2)
);

CREATE TABLE ws (
    time TEXT NOT NULL,
    date TEXT NOT NULL,
    temperature DECIMAL(10,2),
    humidity DECIMAL(10,2),
    device_id REFERENCES device(id)
);

CREATE TABLE hab (
    time TEXT NOT NULL,
    date TEXT NOT NULL,
    temperature DECIMAL(10,2),
    humidity DECIMAL(10,2),
    altitude DECIMAL(10,2),
    device_id REFERENCES device(id)
);

