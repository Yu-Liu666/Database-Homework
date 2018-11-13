ALTER TABLE `lahman2017raw`.`people` 
CHANGE COLUMN `playerID` `playerID` VARCHAR(16) NOT NULL ,
ADD PRIMARY KEY (`playerID`);


ALTER TABLE `lahman2017raw`.`fielding` 
CHANGE COLUMN `playerID` `playerID` VARCHAR(16) NOT NULL ,
CHANGE COLUMN `yearID` `yearID` VARCHAR(4) NOT NULL ,
CHANGE COLUMN `stint` `stint` VARCHAR(1) NOT NULL ,
CHANGE COLUMN `teamID` `teamID` VARCHAR(4) NOT NULL ,
CHANGE COLUMN `POS` `POS` VARCHAR(4) NOT NULL ,
ADD PRIMARY KEY (`playerID`, `yearID`, `stint`, `teamID`,  `POS`);


ALTER TABLE `lahman2017raw`.`appearances` 
CHANGE COLUMN `yearID` `yearID` VARCHAR(4) NOT NULL ,
CHANGE COLUMN `teamID` `teamID` VARCHAR(4) NOT NULL ,
CHANGE COLUMN `playerID` `playerID` VARCHAR(16) NOT NULL ,
ADD PRIMARY KEY (`playerID`, `teamID`, `yearID`);


ALTER TABLE `lahman2017raw`.`managers` 
CHANGE COLUMN `playerID` `playerID` VARCHAR(16) NOT NULL ,
CHANGE COLUMN `yearID` `yearID` VARCHAR(4) NOT NULL ,
CHANGE COLUMN `teamID` `teamID` VARCHAR(4) NOT NULL ,
CHANGE COLUMN `G` `G` VARCHAR(4) NOT NULL ,
ADD PRIMARY KEY (`playerID`, `yearID`, `teamID`, `G`);


ALTER TABLE `lahman2017raw`.`batting` 
CHANGE COLUMN `playerID` `playerID` VARCHAR(16) NOT NULL ,
CHANGE COLUMN `yearID` `yearID` VARCHAR(4) NOT NULL ,
CHANGE COLUMN `stint` `stint` VARCHAR(1) NOT NULL ,
CHANGE COLUMN `teamID` `teamID` VARCHAR(4) NOT NULL ,
ADD PRIMARY KEY (`playerID`, `teamID`, `yearID`, `stint`);


ALTER TABLE `lahman2017raw`.`teams` 
CHANGE COLUMN `yearID` `yearID` VARCHAR(4) NOT NULL ,
CHANGE COLUMN `teamID` `teamID` VARCHAR(4) NOT NULL ,
ADD PRIMARY KEY (`yearID`, `teamID`);


ALTER TABLE `lahman2017raw`.`batting`
ADD CONSTRAINT FK_Batting
FOREIGN KEY (playerID) 
REFERENCES `lahman2017raw`.`people`(playerID)
ON UPDATE NO ACTION
ON DELETE NO ACTION;


ALTER TABLE `lahman2017raw`.`appearances`
ADD CONSTRAINT FK_Appearances
FOREIGN KEY (playerID) 
REFERENCES `lahman2017raw`.`people`(playerID)
ON UPDATE NO ACTION
ON DELETE NO ACTION;


ALTER TABLE `lahman2017raw`.`managers`
ADD CONSTRAINT FK_Managers
FOREIGN KEY (playerID) 
REFERENCES `lahman2017raw`.`people`(playerID)
ON UPDATE NO ACTION
ON DELETE NO ACTION;


ALTER TABLE `lahman2017raw`.`fielding`
ADD CONSTRAINT FK_Fielding
FOREIGN KEY (playerID) 
REFERENCES `lahman2017raw`.`people`(playerID)
ON UPDATE NO ACTION
ON DELETE NO ACTION;

