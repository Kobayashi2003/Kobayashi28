-- Create enum types (unchanged)
CREATE TYPE devstatus_enum AS ENUM ('Finished', 'In development', 'Cancelled');
CREATE TYPE tag_category_enum AS ENUM ('cont', 'ero', 'tech');
CREATE TYPE producer_type_enum AS ENUM ('co', 'in', 'ng');
CREATE TYPE gender_enum AS ENUM ('m', 'f');
CREATE TYPE blood_type_enum AS ENUM ('a', 'b', 'ab', 'o');
CREATE TYPE cup_size_enum AS ENUM ('AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K');
CREATE TYPE character_role_enum AS ENUM ('main', 'primary', 'side', 'appears');
CREATE TYPE sex_enum AS ENUM ('m', 'f', 'b', 'n');

-- Create VN table
CREATE TABLE vn (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    titles JSONB,
    aliases TEXT[],
    olang VARCHAR(10),
    devstatus devstatus_enum,
    released DATE,
    languages TEXT[],
    platforms TEXT[],
    image JSONB,
    length INTEGER,
    length_minutes INTEGER,
    description TEXT,
    screenshots JSONB[],
    relations JSONB[],
    tags JSONB[],
    developers JSONB[],
    staff JSONB[],
    va JSONB[],
    extlinks JSONB[]
);

-- Create TAG table
CREATE TABLE tag (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    aliases TEXT[],
    description TEXT,
    category tag_category_enum,
    searchable BOOLEAN,
    applicable BOOLEAN
);

-- Create PRODUCER table
CREATE TABLE producer (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    original VARCHAR(255),
    aliases TEXT[],
    lang VARCHAR(10),
    type producer_type_enum,
    description TEXT
);

-- Create STAFF table
CREATE TABLE staff (
    id VARCHAR(255) PRIMARY KEY,
    ismain BOOLEAN,
    name VARCHAR(255),
    original VARCHAR(255),
    lang VARCHAR(10),
    gender gender_enum,
    description TEXT,
    aliases JSONB[]
);

-- Create CHARACTER table
CREATE TABLE character (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    original VARCHAR(255),
    aliases TEXT[],
    description TEXT,
    image JSONB,
    blood_type blood_type_enum,
    height INTEGER,
    weight INTEGER,
    bust INTEGER,
    waist INTEGER,
    hips INTEGER,
    cup cup_size_enum,
    age INTEGER,
    birthday INTEGER[],
    sex sex_enum[],
    vns JSONB[],
    traits JSONB[]
);

-- Create TRAIT table
CREATE TABLE trait (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    aliases TEXT[],
    description TEXT,
    searchable BOOLEAN,
    applicable BOOLEAN,
    group_id VARCHAR(255),
    group_name VARCHAR(255),
    char_count INTEGER
);

-- Create local tables for each main table
CREATE TABLE local_vn (
    id VARCHAR(255) PRIMARY KEY REFERENCES vn(id),
    downloaded BOOLEAN DEFAULT TRUE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE local_tag (
    id VARCHAR(255) PRIMARY KEY REFERENCES tag(id),
    downloaded BOOLEAN DEFAULT TRUE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE local_producer (
    id VARCHAR(255) PRIMARY KEY REFERENCES producer(id),
    downloaded BOOLEAN DEFAULT TRUE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE local_staff (
    id VARCHAR(255) PRIMARY KEY REFERENCES staff(id),
    downloaded BOOLEAN DEFAULT TRUE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE local_character (
    id VARCHAR(255) PRIMARY KEY REFERENCES character(id),
    downloaded BOOLEAN DEFAULT TRUE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE local_trait (
    id VARCHAR(255) PRIMARY KEY REFERENCES trait(id),
    downloaded BOOLEAN DEFAULT TRUE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for frequently accessed fields
CREATE INDEX idx_vn_title ON vn(title);
CREATE INDEX idx_character_name ON character(name);
CREATE INDEX idx_staff_name ON staff(name);
CREATE INDEX idx_producer_name ON producer(name);
CREATE INDEX idx_tag_name ON tag(name);
CREATE INDEX idx_trait_name ON trait(name);

-- Create indexes for local tables
CREATE INDEX idx_local_vn_downloaded ON local_vn(downloaded);
CREATE INDEX idx_local_tag_downloaded ON local_tag(downloaded);
CREATE INDEX idx_local_producer_downloaded ON local_producer(downloaded);
CREATE INDEX idx_local_staff_downloaded ON local_staff(downloaded);
CREATE INDEX idx_local_character_downloaded ON local_character(downloaded);
CREATE INDEX idx_local_trait_downloaded ON local_trait(downloaded);