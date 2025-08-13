-- tools/create_tables.sql
CREATE TABLE IF NOT EXISTS Studies (
  StudyID          VARCHAR(64) PRIMARY KEY,
  PatientID        VARCHAR(64),
  Site             VARCHAR(64) NULL,
  HasAneurysm      BIT NULL
);

CREATE TABLE IF NOT EXISTS Series (
  SeriesUID        VARCHAR(128) PRIMARY KEY,
  StudyID          VARCHAR(64) NOT NULL,
  Modality         VARCHAR(8) NOT NULL,
  Plane            VARCHAR(16) NULL,
  NInstances       INT NOT NULL,
  DirPath          NVARCHAR(400) NOT NULL
);
-- Nếu SQL Server không hỗ trợ IF NOT EXISTS theo phiên bản, hãy kiểm tra tồn tại trước khi tạo.

ALTER TABLE Series
ADD CONSTRAINT FK_Series_Studies FOREIGN KEY (StudyID) REFERENCES Studies(StudyID);

CREATE TABLE IF NOT EXISTS Instances (
  SOPInstanceUID   VARCHAR(128) PRIMARY KEY,
  SeriesUID        VARCHAR(128) NOT NULL,
  InstanceNumber   INT,
  FilePath         NVARCHAR(400) NOT NULL,
  SpacingX         FLOAT NULL, SpacingY FLOAT NULL, SpacingZ FLOAT NULL,
  OriginX          FLOAT NULL, OriginY  FLOAT NULL, OriginZ FLOAT NULL
);

ALTER TABLE Instances
ADD CONSTRAINT FK_Instances_Series FOREIGN KEY (SeriesUID) REFERENCES Series(SeriesUID);

CREATE TABLE IF NOT EXISTS AneurysmFindings (
  AnnID            VARCHAR(64) PRIMARY KEY,
  StudyID          VARCHAR(64) NOT NULL,
  SeriesUID        VARCHAR(128) NULL,
  X FLOAT NOT NULL, Y FLOAT NOT NULL, Z FLOAT NOT NULL,
  DiameterMM       FLOAT NULL,
  LocationLabel    VARCHAR(32) NULL
);

ALTER TABLE AneurysmFindings
ADD CONSTRAINT FK_Find_Studies FOREIGN KEY (StudyID) REFERENCES Studies(StudyID);

ALTER TABLE AneurysmFindings
ADD CONSTRAINT FK_Find_Series FOREIGN KEY (SeriesUID) REFERENCES Series(SeriesUID);

CREATE TABLE IF NOT EXISTS Splits (
  SplitName        VARCHAR(64),
  StudyID          VARCHAR(64),
  Fold             INT,
  Role             VARCHAR(16) CHECK (Role IN ('train','val','test')),
  PRIMARY KEY (SplitName, StudyID)
);
