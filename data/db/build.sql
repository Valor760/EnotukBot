CREATE TABLE IF NOT EXISTS CustomCMD(
    CmdName text PRIMARY KEY,
    CmdText text,
    CoolDown integer DEFAULT 0
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