
create table if not exists valhalla_warriors
(
    username varchar(64) not null
        primary key,
    password char(64) not null
);

create table if not exists personal.valhalla_secrets
(
    app_name          varchar(128)                        not null,
    username          varchar(128)                        not null,
    password          varchar(128)                        not null,
    created_at        timestamp default CURRENT_TIMESTAMP null,
    updated_at        timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    last_accessed     timestamp                           null,
    id                int auto_increment
        primary key,
    valhalla_username varchar(64)                         not null,
    constraint valhalla_secrets_auth_user_null_fk
        foreign key (valhalla_username) references personal.valhalla_warriors (username)
);
