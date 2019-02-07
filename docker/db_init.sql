create table assignment
(
  id        varchar not null
    constraint assignment_pkey
      primary key,
  hit_id    varchar not null,
  worker_id varchar not null
);

create table robot
(
  name       varchar not null
    constraint robot_pkey
      primary key,
  short_name varchar not null,
  remote_url varchar not null,
  local_path varchar not null
);

create table robot_assignment
(
  robot_id      varchar not null
    constraint robot_assignment_robot_id_fkey
      references robot
      on update cascade on delete cascade,
  assignment_id varchar not null
    constraint robot_assignment_assignment_id_fkey
      references assignment
      on update cascade on delete cascade,
  constraint robot_assignment_pkey
    primary key (robot_id, assignment_id)
);

create table submission
(
  id                 bigint default nextval('submission_id_seq'::regclass) not null
    constraint submission_pkey
      primary key,
  assignment_id      varchar
    constraint submission_assignment_id_fk
      references assignment
      on update cascade on delete cascade,
  robot_id           varchar
    constraint submission_robot_name_fk
      references robot
      on update cascade on delete cascade,
  design_metaphor    varchar,
  abstraction_slider smallint
);