create database ParisStyles;
use ParisStyles;

create table Cliente(
ID_cliente int primary key not null, Nombre varchar(15) not null, telefono long not null,
correo varchar(25) not null, contraseña int not null, Fecha_registro datetime
);

create table Servicio(
ID_Servicio int primary key not null, Nombre varchar(15) not null, Descripción varchar(30), 
Precio int not null, Duracion int not null 
);

Create table Estilista(
ID_Estilista int primary key not null, Nombre varchar(15) not null, Especialidad varchar(15) not null,
Horario_disp int 
);

create table Reserva(
Fecha_reserva date not null, Hora_reserva int not null, ID_C int, ID_S int, ID_E int,
constraint foreign key (ID_C) references Cliente (ID_cliente),
constraint foreign key (ID_S) references Servicio (ID_Servicio),
constraint foreign key (ID_E) references Estilista (ID_Estilista)
);

create table Producto(
ID_Producto int primary key not null, Nombre varchar (15) not null, 
Descripcion varchar(15) not null, Precio int not null, Stock int not null 
);

create table Curso(
ID_Curso int primary key not null, Nombre varchar (15) not null, 
Descripcion varchar(15) not null, Precio int not null, Fecha varchar(15), Horario varchar(15)
);
