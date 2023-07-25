DROP SCHEMA IF EXISTS zebrafishschema CASCADE;
CREATE SCHEMA zebrafishschema;
SET search_path TO zebrafishschema;

CREATE TABLE LabeledImage (
    img_id integer PRIMARY KEY,
    img bytea,
    point_data decimal []
);
