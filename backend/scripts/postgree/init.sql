CREATE DATABASE alunos;
CREATE DATABASE ultron;

\connect alunos;
CREATE TABLE students (
  ra TEXT PRIMARY KEY,
  bio TEXT
);

\connect ultron;
CREATE TABLE interactions (
  uc TEXT,
  ra TEXT,
  pergunta TEXT,
  resposta TEXT,
  timestamp TIMESTAMP
);
