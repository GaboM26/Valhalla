
create table if not exists valhalla_warriors
(
    username varchar(64) not null
        primary key,
    password char(64) not null
);

create table if not exists crypto_cuentas
(
    app_name          varchar(64)                         not null,
    username          varchar(64)                         not null,
    password          varchar(256)                        not null,
    created_at        timestamp default CURRENT_TIMESTAMP null,
    updated_at        timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    last_accessed     timestamp                           null,
    id                int                                 not null
        primary key,
    valhalla_username varchar(64)                         null,
    constraint crypto_cuentas_auth_user_null_fk
        foreign key (valhalla_username) references auth_user (username)
);
