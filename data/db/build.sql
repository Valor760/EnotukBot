CREATE TABLE IF NOT EXISTS CustomCMD(
    CmdName text PRIMARY KEY,
    CmdText text
);

CREATE TABLE IF NOT EXISTS SchedCMDS(
    CmdText text PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Timeouts(
    Nickname text PRIMARY KEY,
    Day integer,
    Month integer,
    Year integer
);

CREATE TABLE IF NOT EXISTS Triggers(
    TriggerWord text PRIMARY KEY,
    TriggerText text
);

CREATE TABLE IF NOT EXISTS qwe(
    number integer PRIMARY KEY
    );