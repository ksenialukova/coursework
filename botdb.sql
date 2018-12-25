CREATE TABLE Users (
  ID           NUMBER    NOT NULL primary key,
  STATE  NUMBER  NOT NULL,
  NAME VARCHAR2(256),
  SURNAME varchar2(256),
  USERNAME varchar2(256)
);

create table Income(
  ID           NUMBER    NOT NULL primary key,
  DATETIME DATE  NOT NULL,
  type_id NUMBER NOT NULL,
  user_id NUMBER NOT NULL,
  price FLOAT NOT NULL
);

create table IncomeType(
  ID           NUMBER    NOT NULL primary key,
  NAME  VARCHAR2(50)  NOT NULL
);

create table OutcomeType(
  ID           NUMBER    NOT NULL primary key,
  NAME  VARCHAR2(50)  NOT NULL
);

create table Outcome(
  ID           NUMBER    NOT NULL primary key,
  DATETIME DATE  NOT NULL,
  type_id NUMBER NOT NULL,
  user_id NUMBER NOT NULL,
  price FLOAT NOT NULL
);

create table BoarderPrice(
  ID           NUMBER    NOT NULL primary key,
  type_id NUMBER NOT NULL,
  user_id NUMBER NOT NULL,
  price FLOAT NOT NULL
);

CREATE SEQUENCE user_seq START WITH 1 INCREMENT BY 1;

CREATE SEQUENCE income_seq START WITH 1 INCREMENT BY 1;

CREATE SEQUENCE boarderprice_seq START WITH 1 INCREMENT BY 1;

CREATE SEQUENCE outcome_seq START WITH 1 INCREMENT BY 1;

ALTER TABLE Income ADD
FOREIGN KEY (user_id) REFERENCES Users (id);

ALTER TABLE Income ADD
FOREIGN KEY (type_id) REFERENCES IncomeType (id);

ALTER TABLE Outcome ADD
FOREIGN KEY (type_id) REFERENCES OutcomeType (id);

ALTER TABLE BoarderPrice ADD
FOREIGN KEY (type_id) REFERENCES OutcomeType (id);

ALTER TABLE BoarderPrice ADD
FOREIGN KEY (user_id) REFERENCES Users (id);

ALTER TABLE Outcome ADD
FOREIGN KEY (user_id) REFERENCES Users (id);

insert into IncomeType values (1, 'SALARY');

insert into OutcomeType values (1, 'FOOD');
insert into OutcomeType values (2, 'MEDICINE');
insert into OutcomeType values (3, 'ENTERTAINMENT');
insert into OutcomeType values (4, 'FLAT');
insert into OutcomeType values (5, 'COFFEE');