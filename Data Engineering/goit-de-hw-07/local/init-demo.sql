-- Only for a fresh, disposable local MySQL instance.
CREATE DATABASE IF NOT EXISTS olympic_dataset;
CREATE TABLE IF NOT EXISTS olympic_dataset.athlete_event_results (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    medal VARCHAR(16) NULL
);
INSERT INTO olympic_dataset.athlete_event_results (medal)
VALUES ('Bronze'), ('Bronze'),
       ('Silver'), ('Silver'), ('Silver'),
       ('Gold'), ('Gold'), ('Gold'), ('Gold'),
       (NULL), ('None');
CREATE USER IF NOT EXISTS 'olympic_demo'@'%' IDENTIFIED BY 'olympic_demo';
GRANT SELECT ON olympic_dataset.athlete_event_results TO 'olympic_demo'@'%';
GRANT CREATE, SELECT, INSERT ON airflow_hw07.* TO 'olympic_demo'@'%';
