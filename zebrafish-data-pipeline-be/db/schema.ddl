DROP SCHEMA IF EXISTS zebrafishschema CASCADE;
CREATE SCHEMA zebrafishschema;
SET search_path TO zebrafishschema;

-- If I delete a video, should all label data associated with that video also be deleted
CREATE TABLE Video (
    fish_video varchar,
    img bytea,
    PRIMARY KEY (fish_video, img)
);

CREATE TABLE Labelled (
    label_id integer PRIMARY KEY,
    img bytea,
    x integer,
    y integer
);

CREATE TABLE Image (
    img bytea PRIMARY KEY,
    path varchar
);
