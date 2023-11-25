% Hechos: libros con titulo, autor, sinopsis y generos

% libro ( nombre libro,
%    autor,
%    precio,
%    cantidad de paginas,
%    sinopsis,
%    [generos]
% ).



libro('El senior de los anillos',
    'J.R.R. Tolkien',
    '$4000',
    1500,
    'El senior de los anillos sigue la lucha epica entre el bien y el mal en la Tierra Media, con hobbits, elfos, enanos y otras criaturas fantasticas.',
    ['Fantasia', 'Aventura']
).

libro(
    'Dracula',
    'Bram Stoker',
    '$3700',
    500,
    'Dracula es un clasico de terror gotico que sigue la historia del conde Dracula mientras busca extender su influencia no muerta en Inglaterra.',
    ['Terror', 'Fantasia']
).

libro(
    'El hobbit',
    'J.R.R. Tolkien',
    '$1500',
    350,
    'El Hobbit narra la aventura de Bilbo Bolson mientras viaja con un grupo de enanos para reclamar un reino enano y luchar contra el dragon Smaug.',
    ['Fantasia', 'Aventura']
).

libro(
    'El silencio de los corderos',
    'Thomas Harris',
    '$1500',
    400,
    'El silencio de los corderos es un thriller psicologico en el que una joven agente del FBI busca la ayuda de un asesino en serie encarcelado para atrapar a otro.',
    ['Policial', 'Terror']
).

libro(
    'It',
    'Stephen King',
    '$2400',
    1000,
    'It es un libro de terror que sigue a un grupo de amigos que se enfrentan a una entidad maligna que adopta la forma de sus peores miedos.',
    ['Terror']
).

libro(
    'Harry potter y la piedra filosofal',
    'J.K. Rowling',
    '$1500',
    350,
    'La primera entrega de la serie de Harry Potter, donde un joven mago descubre su herencia y asiste a la escuela de magia Hogwarts.',
    ['Fantasia', 'Aventura']
).

libro(
    'El codigo da vinci',
    'Dan Brown',
    '$1200',
    600,
    'Un thriller en el que un profesor de simbologia investiga un asesinato relacionado con sociedades secretas y simbolos enigmaticos.',
    ['Policial', 'Aventura']
).

libro(
    'Los pilares de la tierra',
    'Ken Follett',
    '$1800',
    1200 ,
    'Un drama historico que narra la construccion de una catedral en la Edad Media, entrelazando las vidas de sus personajes.',
    ['Historia', 'Drama']
).



libro(
    'El resplandor',
    'Stephen King',
    '$3400',
    500,
    'Una novela de terror sobre un hombre que acepta un trabajo como cuidador de un hotel aislado durante el invierno y enfrenta fenomenos sobrenaturales.',
    ['Terror']
).

libro(
    'Las cronicas de narnia: el leon, la bruja y el armario',
    'C.S. Lewis',
    '$3500',
    250,
    'El primer libro de la serie que narra las aventuras de ninios que descubren un mundo magico llamado Narnia.',
    ['Fantasia', 'Aventura']
).

libro(
    'Las Aventuras de Sherlock Holmes',
    'Arthur Conan Doyle',
    '$4500',
    400,
    'Una coleccion de relatos cortos protagonizados por el famoso detective Sherlock Holmes y su amigo el Dr. Watson.',
    ['Policial', 'Aventura']
).

libro(
    'La sombra del viento',
    'Carlos Ruiz Zafon',
    '$5000',
    600,
    'Un misterioso libro lleva a un joven a descubrir oscuros secretos en una libreria de Barcelona despues de la Segunda Guerra Mundial.',
    ['Misterio', 'Drama']
).

libro(
    'En llamas',
    'Suzanne Collins',
    '$1650',
    450,
    'La segunda entrega de la trilogia Los juegos del hambre, donde Katniss Everdeen se enfrenta a nuevos desafios en la arena.',
    ['Aventura']
).

libro(
    'Orgullo y prejuicio',
    'Jane Austen',
    '$2800',
    400,
    'Una novela de romance clasica que sigue la vida y amores de Elizabeth Bennet en la sociedad inglesa del siglo XIX.',
    ['Romance', 'Drama']
).

libro(
    'Los miserables',
    'Victor Hugo',
    '$2700',
    1000,
    'Una novela epica que sigue la vida de varios personajes en la Francia del siglo XIX, explorando temas de redencion y justicia.',
    ['Historia', 'Drama']
).

libro(
    'Don quijote de la mancha',
    'Miguel de Cervantes',
    '$4500',
    1000,
    'Una obra cumbre de la literatura en la que un hidalgo enloquecido se embarca en aventuras como caballero andante.',
    ['Aventura', 'Humor']
).

libro(
    'Crimen y castigo',
    'Fyodor Dostoevsky',
    '$1000',
    500,
    'La novela sigue a Raskolnikov, un estudiante que comete un asesinato y luego se enfrenta a una crisis moral y psicologica.',
    ['Policial', 'Drama']
).

libro(
    'Las aventuras de huckleberry finn',
    'Mark Twain',
    '$3500',
    350,
    'La secuela de Las aventuras de Tom Sawyer sigue a Huckleberry Finn en su viaje por el rio Misisipi y sus encuentros con diversos personajes.',
    ['Aventura', 'Humor']
).

libro(
    'La riqueza de las naciones',
    'Adam Smith',
    '$2500',
    1000,
    'Un influyente libro sobre economia que introduce conceptos como la division del trabajo y la mano invisible en la economia de mercado.',
    ['Economia']
).

libro(
    'El arte de amar',
    'Erich Fromm',
    '$1500',
    200,
    'Un libro que explora la naturaleza del amor y las relaciones humanas desde una perspectiva psicologica y filosofica.',
    ['Psicologia']
).

libro(
    'La cocina al desnudo',
    'Julia Child',
    '$1500',
    250,
    'Un libro de cocina que combina recetas deliciosas con consejos y tecnicas de cocina explicados de manera detallada.',
    ['Cocina']
).

libro(
    'La biblia',
    'Varios autores',
    '$1500',
    1000,
    'El texto sagrado del cristianismo que contiene ensenianzas religiosas, historias y relatos espirituales.',
    ['Religion']
).

libro(
    'Hojarasca',
    'Gabriel Garcia Marquez',
    '$1500',
    200,
    'Una coleccion de poesia que aborda temas como el amor, la vida y la naturaleza con la caracteristica prosa poetica del autor.',
    ['Poesia']
).


% Regla para buscar libros por genero

% Regla para obtener todos los titulos de libros
todos_los_libros(Titulos) :-
    findall(Titulo, libro(Titulo, _, _, _, _, _), Titulos).

% Regla existe libro

existe_libro(Titulo) :-libro(Titulo, _, _, _, _, _).

% Regla para consultar titulos de libros por genero
titulos_por_genero(Genero, Titulos) :-
    findall(Titulo, (libro(Titulo, _, _, _, _, Generos), member(Genero, Generos)), Titulos).



% Regla para consultar la sinopsis de un libro dado su titulo
sinopsis_por_titulo(Titulo, Sinopsis) :-
    libro(Titulo, _, _, _, Sinopsis, _).



% Regla para consultar la cantidad de paginas de un libro dado su titulo
paginas_por_titulo(Titulo, Paginas) :-
    libro(Titulo, _, _, Paginas, _, _).



% Regla para consultar el precio de un libro dado su titulo
precio_por_titulo(Titulo, Precio) :-
    libro(Titulo, _, Precio, _, _, _).



% Regla para consultar el autor de un libro dado su titulo
autor_por_titulo(Titulo, Autor) :-
    libro(Titulo, Autor, _, _, _, _).