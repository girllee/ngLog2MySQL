CREATE TABLE ngLog (
  reqTime DATETIME NOT NULL ,
  ip VARCHAR(16) NOT NULL ,
  method VARCHAR(16) ,
  uri VARCHAR(512) ,
  status VARCHAR(8),
  bodyBytes int UNSIGNED,
  referrer VARCHAR(256),
  userAgent VARCHAR(256),
  os VARCHAR(32),
  browser VARCHAR(32)
)DEFAULT CHARSET utf8;