Create database recetas_schema;
Use recetas_schema;

Create table users (
	id int primary key auto_increment,
    firstname varchar(45),
    lastname varchar(45),
    birthday date,
    gender varchar(100),
    email varchar(100),
    password text,
    created_at datetime,
    updated_at datetime,
    isBlocked boolean default false
);

Create table recipes (
	id int primary key auto_increment,
    name varchar(45),
    description text,
    instructions text,
    made_on date,
    isUnder boolean default false,
    author_id int not null,
	created_at datetime,
    updated_at datetime,
    foreign key (author_id) references users(id)
);

Create table reports (
    id int primary key auto_increment,
    user_id int not null,
    user_ip varchar(45),
	isDeleted boolean default false,
    created_at datetime,
    updated_at datetime,
    foreign key (user_id) references users (id)
);

