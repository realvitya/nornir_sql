BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `regions` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL
);
INSERT INTO `regions` (id,name) VALUES (1,'EA');
INSERT INTO `regions` (id,name) VALUES (2,'NA');
INSERT INTO `regions` (id,name) VALUES (3,'SA');
INSERT INTO `regions` (id,name) VALUES (4,'AP');
INSERT INTO `regions` (id,name) VALUES (5,'AF');
CREATE TABLE IF NOT EXISTS `hosts_table` (
	`device_name`	TEXT,
	`device_type`	INTEGER,
	`region`	INTEGER,
	`groups`	TEXT,
	`status`	TEXT,
	`last_scanned`	TEXT
);
INSERT INTO `hosts_table` (device_name,device_type,region,groups,status,last_scanned) VALUES ('FW1',1,1,'HUBDP','deployed','2021-10-20 13:00:31');
INSERT INTO `hosts_table` (device_name,device_type,region,groups,status,last_scanned) VALUES ('FW2',1,2,NULL,'deployed','2021-10-20 13:00:31');
INSERT INTO `hosts_table` (device_name,device_type,region,groups,status,last_scanned) VALUES ('FW3',1,3,NULL,'deployed','2021-10-20 13:00:31');
INSERT INTO `hosts_table` (device_name,device_type,region,groups,status,last_scanned) VALUES ('SW1',4,1,'HUBDP,switch-password','deployed','2021-10-20 13:00:31');
INSERT INTO `hosts_table` (device_name,device_type,region,groups,status,last_scanned) VALUES ('SW2',4,2,NULL,'deployed','2021-10-20 13:00:31');
INSERT INTO `hosts_table` (device_name,device_type,region,groups,status,last_scanned) VALUES ('SW3',4,3,NULL,'deployed','2021-10-20 13:00:31');
INSERT INTO `hosts_table` (device_name,device_type,region,groups,status,last_scanned) VALUES ('SW4',4,4,NULL,'decommed','2020-08-10 12:00:31');
INSERT INTO `hosts_table` (device_name,device_type,region,groups,status,last_scanned) VALUES ('ROUTER1',2,1,'HUBDP','deployed','2021-10-20 13:00:31');
INSERT INTO `hosts_table` (device_name,device_type,region,groups,status,last_scanned) VALUES ('ROUTER2',2,2,NULL,'deployed','2021-10-20 13:00:31');
INSERT INTO `hosts_table` (device_name,device_type,region,groups,status,last_scanned) VALUES ('ROUTER3',2,3,NULL,'deployed','2021-10-20 13:00:31');
INSERT INTO `hosts_table` (device_name,device_type,region,groups,status,last_scanned) VALUES ('FW4',3,4,NULL,'inventory',NULL);
CREATE TABLE IF NOT EXISTS `groups_table` (
	`name`	TEXT NOT NULL,
	`platform`	TEXT,
	`username`	TEXT,
	`password`	TEXT,
	`country`	TEXT,
	`city`	TEXT,
	`region`	TEXT,
	PRIMARY KEY(`name`)
);
INSERT INTO `groups_table` (name,platform,username,password,country,city,region) VALUES ('HUBDP','','','','Hungary','Budapest',NULL);
INSERT INTO `groups_table` (name,platform,username,password,country,city,region) VALUES ('switch-password','','swadmin','swpass','','',NULL);
CREATE TABLE IF NOT EXISTS `device_types` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`pid`	TEXT,
	`os`	TEXT NOT NULL,
	`vendor`	TEXT NOT NULL
);
INSERT INTO `device_types` (id,pid,os,vendor) VALUES (1,'ASA5516','asa','cisco');
INSERT INTO `device_types` (id,pid,os,vendor) VALUES (2,'ISR4431','iosxe','cisco');
INSERT INTO `device_types` (id,pid,os,vendor) VALUES (3,'SRX3600','junos','juniper');
INSERT INTO `device_types` (id,pid,os,vendor) VALUES (4,'WS-C3850-48U-L','cisco','iosxe');
COMMIT;
