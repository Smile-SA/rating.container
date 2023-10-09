-- Insert data into the "template" table
INSERT INTO template (id, t_name, t_group, t_var, t_query)
VALUES ('2023-08-30 10:00:00', 'Template1', 'Group1', 'Var1', 'SELECT * FROM example_table');

-- Insert data into the "metric" table
INSERT INTO metric (id, m_name, timeframe, m_var, t_name)
VALUES ('2023-08-30 11:00:00', 'Metric1', 'Hourly', 'Var1', 'Template1');

-- Insert data into the "instance" table
INSERT INTO instance (start_time, end_time, instance_name, instance_promql, instance_values)
VALUES ('2023-08-30 12:00:00', '2023-08-30 13:00:00', 'Instance1', 'SELECT * FROM Metric1', 'Value1,Value2');
