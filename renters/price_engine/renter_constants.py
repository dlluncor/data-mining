
### Constants for CSV file generation.

import random
from collections import OrderedDict

first_names = ['Liam', 'Charlotte', 'Noah', 'Amelia', 'Emilia', 'Oliver', 'Aria', 'Arya', 'Ethan', 'Olivia', 'Asher', 'Violet', 'Benjamin', 'Ava', 'Henry', 'Sophia', 'Sofia', 'Owen', 'Emma', 'Caleb', 'Kaleb', 'Scarlett', 'Scarlet', 'Jackson', 'Jaxon', 'Nora', 'Norah', 'Grayson', 'Greyson', 'Audrey', 'Declan', 'Aurora', 'Landon', 'Landen', 'Vivienne', 'Vivien', 'Vivian', 'Alexander', 'Lily', 'Lilly', 'Levi', 'Abigail', 'Aidan', 'Aiden', 'Aden', 'Chloe', 'Khloe', 'Finn', 'Fynn', 'Adalyn', 'Elijah', 'Ella', 'Lucas', 'Lukas', 'Elizabeth', 'Elisabeth', 'Gavin', 'Alice', 'Gabriel', 'Grace', 'Elliot', 'Eliot', 'Elliott', 'Hazel', 'Emmett', 'Harper', 'William', 'Adelaide', 'James', 'Isla', 'Sebastian', 'Sebastien', 'Claire', 'Clare', 'Jack', 'Arianna', 'Ariana', 'Theodore', 'Isabella', 'Izabella', 'Wyatt', 'Penelope', 'Hudson', 'Eleanor', 'Jasper', 'Evelyn', 'Silas', 'Lucy', 'Lucie', 'Isaac', 'Juliet', 'Juliette', 'Logan', 'Stella', 'Jacob', 'Jakob', 'Sadie', 'Everett', 'Genevieve', 'Andrew', 'Hannah', 'Hanna', 'Luke', 'Clara', 'Nathan', 'Cora', 'Jace', 'Jase', 'Evangeline', 'Samuel', 'Ivy', 'Cole', 'Kole', 'Luna', 'Holden', 'Ruby', 'Chase', 'Lorelei', 'Archer', 'Lydia', 'Matthew', 'Mathew', 'Caroline', 'Aaron', 'Aron', 'Savannah', 'Savanna', 'Leo', 'Rosalie', 'Nathaniel', 'Annabelle', 'Anabel', 'Mason', 'Eloise', 'Connor', 'Conor', 'Conner', 'Isabelle', 'Isabel', 'Milo', 'Piper', 'Daniel', 'Emily', 'Dominic', 'Dominick', 'Brielle', 'Eli', 'Natalie', 'Lincoln', 'Arabella', 'Miles', 'Adeline', 'Sawyer', 'Rose', 'Atticus', 'Everly', 'Joshua', 'Lila', 'Lilah', 'Ezra', 'Fiona', 'Harrison', 'Felicity', 'Graham', 'Graeme', 'Paige', 'Rhys', 'Reece', 'Reese', 'Avery', 'Thomas', 'Layla', 'Leila', 'Zachary', 'Zachery', 'Zackery', 'Mia', 'Colton', 'Madeline', 'Madelyn', 'Madelynn', 'August', 'Mila', 'Jonah', 'Anna', 'Ana', 'Charles', 'Gemma', 'Jude', 'Zoey', 'Felix', 'Keira', 'Kira', 'Adam', 'Elsa', 'Carter', 'Leah', 'Lea', 'Easton', 'Naomi', 'Ronan', 'Willow', 'Ian', 'Eliana', 'Parker', 'Eva', 'Michael', 'Iris', 'Isaiah', 'Autumn', 'Micah', 'Lillian', 'Xander', 'Zander', 'Zoe', 'Hunter', 'Anastasia', 'Evan', 'Phoebe', 'Xavier', 'Victoria', 'Nicholas', 'Nicolas', 'Josephine', 'Bennett', 'Addison', 'Addyson', 'Nolan', 'Sophie', 'Sofie', 'Dylan', 'Dillon', 'Dillan', 'Quinn', 'Gideon', 'Daphne', 'Max', 'Elise', 'Joseph', 'Julia', 'Adrian', 'Eden', 'David', 'Sienna', 'Elias', 'Hadley', 'Ryder', 'Rider', 'Delilah', 'Seth', 'Jane', 'Christopher', 'Gabriella', 'Josiah', 'Tessa', 'Griffin', 'Alexandra']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Wilson', 'Martinez', 'Anderson', 'Taylor', 'Thomas', 'Hernandez', 'Moore', 'Martin', 'Jackson', 'Thompson', 'White', 'Lopez', 'Lee', 'Gonzalez', 'Harris', 'Clark', 'Lewis', 'Robinson', 'Walker', 'Perez', 'Hall', 'Young', 'Allen', 'Sanchez', 'Wright', 'King', 'Scott', 'Green', 'Baker', 'Adams', 'Nelson', 'Hill', 'Ramirez', 'Campbell', 'Mitchell', 'Roberts', 'Carter', 'Phillips', 'Evans', 'Turner', 'Torres', 'Parker', 'Collins', 'Edwards', 'Stewart', 'Flores', 'Morris', 'Nguyen', 'Murphy', 'Rivera', 'Cook', 'Rogers', 'Morgan', 'Peterson', 'Cooper', 'Reed', 'Bailey', 'Bell', 'Gomez', 'Kelly', 'Howard', 'Ward', 'Cox', 'Diaz', 'Richardson', 'Wood', 'Watson', 'Brooks', 'Bennett', 'Gray', 'James', 'Reyes', 'Cruz', 'Hughes', 'Price', 'Myers', 'Long', 'Foster', 'Sanders', 'Ross', 'Morales', 'Powell', 'Sullivan', 'Russell', 'Ortiz', 'Jenkins', 'Gutierrez', 'Perry', 'Butler', 'Barnes', 'Fisher', 'Henderson', 'Coleman', 'Simmons', 'Patterson', 'Jordan', 'Reynolds', 'Hamilton', 'Graham', 'Kim', 'Gonzales', 'Alexander', 'Ramos', 'Wallace', 'Griffin', 'West', 'Cole', 'Hayes', 'Chavez', 'Gibson', 'Bryant', 'Ellis', 'Stevens', 'Murray', 'Ford', 'Marshall', 'Owens', 'Mcdonald', 'Harrison', 'Ruiz', 'Kennedy', 'Wells', 'Alvarez', 'Woods', 'Mendoza', 'Castillo', 'Olson', 'Webb', 'Washington', 'Tucker', 'Freeman', 'Burns', 'Henry', 'Vasquez', 'Snyder', 'Simpson', 'Crawford', 'Jimenez', 'Porter', 'Mason', 'Shaw', 'Gordon', 'Wagner', 'Hunter', 'Romero', 'Hicks', 'Dixon', 'Hunt', 'Palmer', 'Robertson', 'Black', 'Holmes', 'Stone', 'Meyer', 'Boyd', 'Mills', 'Warren', 'Fox', 'Rose', 'Rice', 'Moreno', 'Schmidt', 'Patel', 'Ferguson', 'Nichols', 'Herrera', 'Medina', 'Ryan', 'Fernandez', 'Weaver', 'Daniels', 'Stephens', 'Gardner', 'Payne', 'Kelley', 'Dunn', 'Pierce', 'Arnold', 'Tran', 'Spencer', 'Peters', 'Hawkins', 'Grant', 'Hansen', 'Castro', 'Hoffman', 'Hart', 'Elliott', 'Cunningham', 'Knight', 'Bradley', 'Carroll', 'Hudson', 'Duncan', 'Armstrong', 'Berry', 'Andrews', 'Johnston', 'Ray', 'Lane', 'Riley', 'Carpenter', 'Perkins', 'Aguilar', 'Silva', 'Richards', 'Willis', 'Matthews', 'Chapman', 'Lawrence', 'Garza', 'Vargas', 'Watkins', 'Wheeler', 'Larson', 'Carlson', 'Harper', 'George', 'Greene', 'Burke', 'Guzman', 'Morrison', 'Munoz', 'Jacobs', 'Obrien', 'Lawson', 'Franklin', 'Lynch', 'Bishop', 'Carr', 'Salazar', 'Austin', 'Mendez', 'Gilbert', 'Jensen', 'Williamson', 'Montgomery', 'Harvey', 'Oliver', 'Howell', 'Dean', 'Hanson', 'Weber', 'Garrett', 'Sims', 'Burton', 'Fuller', 'Soto', 'Mccoy', 'Welch', 'Chen', 'Schultz', 'Walters', 'Reid', 'Fields', 'Walsh', 'Little', 'Fowler', 'Bowman', 'Davidson', 'May', 'Day', 'Schneider', 'Newman', 'Brewer', 'Lucas', 'Holland', 'Wong', 'Banks', 'Santos', 'Curtis', 'Pearson', 'Delgado', 'Valdez', 'Pena', 'Rios', 'Douglas', 'Sandoval', 'Barrett', 'Hopkins', 'Keller', 'Guerrero', 'Stanley', 'Bates', 'Alvarado', 'Beck', 'Ortega', 'Wade', 'Estrada', 'Contreras', 'Barnett', 'Caldwell', 'Santiago', 'Lambert', 'Powers', 'Chambers', 'Nunez', 'Craig', 'Leonard', 'Lowe', 'Rhodes', 'Byrd', 'Gregory', 'Shelton', 'Frazier', 'Becker', 'Maldonado', 'Fleming', 'Vega', 'Sutton', 'Cohen', 'Jennings', 'Parks', 'Mcdaniel', 'Watts', 'Barker', 'Norris', 'Vaughn', 'Vazquez', 'Holt', 'Schwartz', 'Steele', 'Benson', 'Neal', 'Dominguez', 'Horton', 'Terry', 'Wolfe', 'Hale', 'Lyons', 'Graves', 'Haynes', 'Miles', 'Park', 'Warner', 'Padilla', 'Bush', 'Thornton', 'Mccarthy', 'Mann', 'Zimmerman', 'Erickson', 'Fletcher', 'Mckinney', 'Page', 'Dawson', 'Joseph', 'Marquez', 'Reeves', 'Klein', 'Espinoza', 'Baldwin', 'Moran', 'Love', 'Robbins', 'Higgins', 'Ball', 'Cortez', 'Le', 'Griffith', 'Bowen', 'Sharp', 'Cummings', 'Ramsey', 'Hardy', 'Swanson', 'Barber', 'Acosta', 'Luna', 'Chandler', 'Blair', 'Daniel', 'Cross', 'Simon', 'Dennis', 'Oconnor', 'Quinn', 'Gross', 'Navarro', 'Moss', 'Fitzgerald', 'Doyle', 'Mclaughlin', 'Rojas', 'Rodgers', 'Stevenson', 'Singh', 'Yang', 'Figueroa', 'Harmon', 'Newton', 'Paul', 'Manning', 'Garner', 'Mcgee', 'Reese', 'Francis', 'Burgess', 'Adkins', 'Goodman', 'Curry', 'Brady', 'Christensen', 'Potter', 'Walton', 'Goodwin', 'Mullins', 'Molina', 'Webster', 'Fischer', 'Campos', 'Avila', 'Sherman', 'Todd', 'Chang', 'Blake', 'Malone', 'Wolf', 'Hodges', 'Juarez', 'Gill', 'Farmer', 'Hines', 'Gallagher', 'Duran', 'Hubbard', 'Cannon', 'Miranda', 'Wang', 'Saunders', 'Tate', 'Mack', 'Hammond', 'Carrillo', 'Townsend', 'Wise', 'Ingram', 'Barton', 'Mejia', 'Ayala', 'Schroeder', 'Hampton', 'Rowe', 'Parsons', 'Frank', 'Waters', 'Strickland', 'Osborne', 'Maxwell', 'Chan', 'Deleon', 'Norman', 'Harrington', 'Casey', 'Patton', 'Logan', 'Bowers', 'Mueller', 'Glover', 'Floyd', 'Hartman', 'Buchanan', 'Cobb', 'French', 'Kramer', 'Mccormick', 'Clarke', 'Tyler', 'Gibbs', 'Moody', 'Conner', 'Sparks', 'Mcguire', 'Leon', 'Bauer', 'Norton', 'Pope', 'Flynn', 'Hogan', 'Robles', 'Salinas', 'Yates', 'Lindsey', 'Lloyd', 'Marsh', 'Mcbride', 'Owen', 'Solis', 'Pham', 'Lang', 'Pratt', 'Lara', 'Brock', 'Ballard', 'Trujillo', 'Shaffer', 'Drake', 'Roman', 'Aguirre', 'Morton', 'Stokes', 'Lamb', 'Pacheco', 'Patrick', 'Cochran', 'Shepherd', 'Cain', 'Burnett', 'Hess', 'Li', 'Cervantes', 'Olsen', 'Briggs', 'Ochoa', 'Cabrera', 'Velasquez', 'Montoya', 'Roth', 'Meyers', 'Cardenas', 'Fuentes', 'Weiss', 'Hoover', 'Wilkins', 'Nicholson', 'Underwood', 'Short', 'Carson', 'Morrow', 'Colon', 'Holloway', 'Summers', 'Bryan', 'Petersen', 'Mckenzie', 'Serrano', 'Wilcox', 'Carey', 'Clayton', 'Poole', 'Calderon', 'Gallegos', 'Greer', 'Rivas', 'Guerra', 'Decker', 'Collier', 'Wall', 'Whitaker', 'Bass', 'Flowers', 'Davenport', 'Conley', 'Houston', 'Huff', 'Copeland', 'Hood', 'Monroe', 'Massey', 'Roberson', 'Combs', 'Franco', 'Larsen', 'Pittman', 'Randall', 'Skinner', 'Wilkinson', 'Kirby', 'Cameron', 'Bridges', 'Anthony', 'Richard']

phone_numbers = ['(415) 255-1100','(415) 928-4631','(510) 540-5454','(866) 932-5588','(510) 886-0616','(415) 307-1871','(510) 865-1139','(415) 777-4850','(510) 222-8623','(415) 403-2247','(415) 474-5494','(650) 592-3139','(415) 864-3333','(510) 887-8185','(415) 284-3000','(415) 992-7215','(415) 615-9200','(415) 777-4100','(415) 673-7545','(415) 345-4400','(415) 861-9981','(510) 841-2760','(925) 934-1117','(650) 345-5406','(415) 921-1969','(707) 745-3000','(855) 802-6683','(415) 405-4600','(415) 234-7084','(415) 474-0333','(415) 474-1750','(925) 283-9912','(510) 215-2850','(415) 885-3333','(602) 427-2752','(415) 230-1996','(415) 864-7368','(888) 270-6855','(415) 354-4506','(866) 270-9902','(510) 865-2875','(415) 781-9000','(415) 956-8858','(650) 359-1757','(925) 284-1915','(415) 981-5780','(888) 586-1355','(415) 474-8052','(415) 738-8121','(415) 922-0111','(415) 400-5295','(415) 931-6300','(415) 885-0333','(650) 997-0400','(415) 981-2605','(415) 921-5733','(415) 626-3100','(650) 344-2510','(925) 686-1761','(650) 755-8133','(408) 946-2955','(408) 246-1226','(877) 268-2574','(510) 793-2535','(408) 737-2900','(650) 854-3900','(408) 736-4963','(510) 240-9405','(408) 565-9960','(510) 886-1055','(408) 241-1445','(408) 733-4733','(925) 228-0760','(510) 582-5240','(408) 866-1005','(650) 425-3914','(925) 452-7910','(510) 352-5900','(415) 404-7453','(650) 341-9900','(408) 502-5305','(415) 334-1880','(650) 321-1701','(650) 589-2909','(415) 688-2085','(866) 849-2126','(408) 255-6750','(925) 284-2586','(408) 257-1060','(650) 557-4116','(650) 372-8336','(650) 991-0777','(650) 588-0220','(408) 988-7500','(650) 282-3083','(650) 591-8906','(925) 735-3047','(866) 451-2806','(650) 440-7285','(650) 591-6666','(650) 349-3200','(650) 288-4227','(877) 271-1549','(650) 341-6700','(650) 264-9696','(650) 591-1143','(650) 348-6130','(650) 342-2301','(844) 325-4744','(408) 733-3049','(650) 241-1641','(650) 321-1000','(619) 280-5383','(858) 453-7368','(619) 463-1116','(855) 365-1913','(619) 583-8084','(619) 270-5895','(619) 443-1720','(858) 587-9997','(888) 704-5204','(619) 479-6565','(858) 565-0311','(619) 284-5285','(858) 271-4151','(866) 835-1449','(877) 713-3968','(619) 293-3888','(619) 216-8884','(760) 291-8098','(619) 561-2320','(877) 713-3956','(760) 489-9272','(619) 610-0954','(619) 460-5241','(858) 279-7410','(619) 281-4006','(619) 463-5393','(858) 560-5720','(619) 255-4000','(877) 713-4583','(619) 448-8282','(619) 443-6702','(858) 565-9081','(858) 457-5161','(858) 571-0104','(858) 578-1632','(760) 798-2632','(858) 666-2423','(888) 271-6704','(619) 582-4074','(858) 530-2100','(858) 678-0550','(866) 671-1752','(858) 748-4774','(858) 693-1175','(619) 670-6400','(866) 894-6343','(619) 447-3000','(619) 427-0190','(760) 598-9000','(619) 280-4988','(619) 233-4787','(760) 434-6161','(619) 651-7000','(619) 286-7600','(619) 595-7801','(760) 208-2785','(888) 830-9456','(619) 231-9600','(619) 334-6948','(858) 486-4834','(408) 456-0700','(408) 377-2331','(650) 352-3601','(877) 745-9314','(650) 528-2129','(408) 733-2306','(408) 980-0502','(650) 381-9788','(408) 618-0044','(408) 570-5040','(877) 516-8284','(408) 512-2708','(408) 733-9095','(408) 586-9001','(650) 216-6886','(408) 359-8979','(877) 396-9296','(408) 549-1209','(408) 735-9780','(650) 968-8384','(408) 245-6710','(650) 854-2651','(888) 482-3584','(650) 528-2128','(408) 437-1900','(844) 328-9442','(408) 732-9450','(408) 873-9090','(510) 494-9500','(707) 544-1400','(415) 883-9600','(707) 584-0655','(415) 459-2900','(707) 778-1221','(415) 453-6204','(415) 578-4349','(707) 823-0730','(707) 653-5931','(888) 284-2778','(707) 766-6881','(415) 924-1196','(510) 223-2000','(707) 579-5605','(707) 538-1516','(415) 459-3577','(415) 223-0828','(707) 648-1900','(707) 559-9571','(415) 492-2180','(707) 823-1361','(707) 361-4060','(925) 943-7977','(707) 762-5126','(415) 492-9660','(510) 236-2860','(707) 766-9500','(415) 491-1125','(866) 837-6172','(707) 644-3322','(707) 645-8888','(707) 781-1993','(510) 758-6874','(408) 384-8887','(650) 389-9367','(408) 354-7317','(866) 575-9826','(408) 502-5355','(408) 214-1714','(408) 496-6300','(408) 736-8658','(408) 720-8566','(650) 265-2120','(408) 996-1006','(408) 244-0900','(408) 664-2724','(408) 216-8947','(888) 492-9765','(408) 216-8945','(408) 441-7600','(408) 263-6040','(408) 247-1900','(408) 984-4767','(408) 570-5010','(408) 287-3444','(408) 445-5211','(408) 266-1474','(831) 426-6855','(408) 295-1360','(408) 599-5321','(408) 998-2012','(408) 288-7368','(408) 971-9397','(408) 294-5333','(408) 271-2600','(408) 297-4675','(408) 227-3700','(408) 298-9988','(408) 647-5909','(408) 923-3200','(831) 469-3620','(408) 354-8910','(408) 600-1431','(408) 378-7188','(408) 214-1685','(408) 728-9514','(831) 384-7159','(408) 779-8986','(831) 475-6342','(831) 449-1800','(408) 778-3237','(408) 225-8648','(866) 251-7152','(408) 723-2370','(831) 427-1991','(844) 250-7147','(831) 373-1025','(831) 585-1628','(831) 240-0330','(831) 240-0589','(831) 476-8897','(831) 458-5042','(408) 848-3474','(408) 842-4457','(415) 658-6604','(415) 241-0100','(415) 957-5887','(415) 749-0101','(415) 989-1111','(415) 749-0101','(603) 571-6274','(415) 673-1232','(415) 491-1125','(415) 440-0550','(415) 495-4119','(415) 567-0683','(415) 881-5059','(415) 421-4333','(415) 359-1333','(415) 580-6272','(415) 861-3333','(415) 921-3469','(415) 745-3716','(415) 440-1155','(415) 354-4507','(415) 563-6333','(415) 487-1218','(415) 445-6530','(415) 474-5333','(415) 354-4501','(415) 626-6900','(415) 345-1970','(415) 787-4485','(415) 701-8366','(415) 505-2504','(415) 923-6900','(415) 552-9443','(855) 254-9912','(855) 641-0159','(877) 902-0832','(866) 678-3468','(415) 978-9619','(415) 664-2822','(415) 255-2288','(650) 488-4047','(415) 584-4800','(650) 758-4888','(415) 648-1910','(415) 587-5815','(415) 821-7280','(415) 648-5349','(415) 282-1686','(415) 330-9252','(415) 642-8440','(415) 333-9956','(415) 284-9080','(415) 308-7225','(415) 334-2698','(650) 997-0670','(415) 586-8940','(650) 755-3872','(650) 992-3500','(650) 991-0827','(415) 647-6922','(855) 646-0468','(650) 994-2247','(650) 756-4588','(415) 285-1231','(415) 641-8003','(415) 642-1877','(650) 583-9275','(650) 952-3727','(415) 285-5966','(415) 513-0086','(650) 756-1405']
zip_codes = ['94110','94109','94704','94117','94542','94114','94501','94107','94803','94105','94109','94002','94103','94545','94107','94105','94105','94105','94109','94109','94103','94704','94596','94404','94115','94510','94806','94132','94102','94123','94109','94549','94801','94109','94043','94158','94103','94086','94107','94111','94501','94104','94108','94066','94549','94108','94806','94109','94114','94102','94133','94115','94133','94015','94107','94115','94107','94402','94520','94015','95035','95051','95050','94536','94085','94025','94085','94538','95054','94544','95050','94086','94553','94544','95008','94403','94553','94578','94112','94403','94087','94132','94304','94080','94404','94404','95014','94549','95014','94044','94404','94014','94080','95054','94040','94065','94582','95054','94401','94065','94404','94403','94404','94404','94002','94002','94401','94010','94404','94086','94061','94301','92108','92122','91942','92122','92115','91910','92040','92122','92115','92139','92123','92115','92126','92122','92071','92108','91913','92029','92040','92119','92027','92101','91942','92111','92120','91941','92123','92101','92120','92071','92040','92123','92122','92117','92126','92078','92109','92122','92115','92126','92122','92128','92064','92126','91978','91977','92021','91910','92081','92108','92101','92008','91914','92120','92101','92056','92122','92101','92021','92064','95134','95008','94301','94040','94041','94086','95054','94062','95134','95134','94043','95054','94086','95035','94063','94086','94086','95051','94086','94043','94087','94025','94304','94041','95112','94089','94087','95014','94538','95404','94949','94928','94930','94954','94901','94903','95472','94590','94954','94954','94939','94806','95403','95409','94901','94903','94590','94954','94903','95472','95409','94597','94952','94903','94530','94928','94903','95401','94590','94503','94954','94806','94087','94040','95030','95112','95051','95051','95054','94087','94086','94086','95014','95050','94085','95126','95050','95126','95131','95035','95129','95128','95134','95112','95125','95125','95060','95113','95125','95126','95126','95112','95126','95126','95126','95136','95111','95136','95127','95060','95030','95123','95008','95020','95138','93933','95037','95010','93906','95037','95123','95123','95136','95060','93940','93940','93906','93906','93906','95062','95060','95020','95020','94115','94117','94107','94102','94108','94109','94102','94109','94103','94109','94107','94109','94103','94133','94109','94158','94103','94115','94122','94109','94109','94115','94102','94105','94109','94131','94102','94109','94109','94102','94109','94123','94110','94107','94103','94111','94158','94107','94131','94102','94134','94134','94014','94124','94131','94124','94124','94110','94005','94124','94134','94112','94134','94131','94014','94112','94014','94014','94014','94124','94014','94014','94014','94131','94110','94110','94080','94080','94110','94110','94015']
addresses = ['3469 18th St','952 Sutter St','2020 Kittredge St','783 Buena Vista Ave W','25200 Carlos Bee Blvd','3904 17th St','564 Central Ave','3 Bayside Village Pl','3535 El Portal Dr','680 Mission St','1100 Gough St','2515 Carlmont Dr','1188 Mission St','25800 Industrial Blvd.','1 St Francis Pl','388 Beale Street','88 Howard St','121 Spear St B18','1609 Franklin St','1388 Sutter St 11','44 Gough St 202','2230 Durant Ave  103','1200 Newell Hill Pl','808 Comet Dr','1475 Fillmore St','801 Southampton Rd','2490 Lancaster Dr','3711 19th Ave','1 Polk St','1550 Bay St','1560 Van Ness Ave','949 East St','400 Harbour Way','888 OFarrell St','555 W Middlefield Rd','355 Berry St','1045 Mission St','1035 Aster Ave','255 King St','460 Davis Ct','550 Central Ave  301','690 Market St','706 Kearny St','3815 Susan Dr','3520 Brook St','47 Kearny St','2300 Lancaster Dr','400 Hyde St  101','4058 17th St','835 Turk St','2211 Stockton St','1489 Webster St  101','2140 Taylor St','862 Campus Dr','574 3rd St 101','2799 California St','2235 3rd St','10 De Sabla Rd','1491 Detroit Ave','333 Park Plaza Dr','440 Dixon Landing Rd','101 Saratoga Ave','1599 Warburton Ave','38660 Hastings St  109','330 N Mathilda Ave','350 Sharon Park Dr','355 N Wolfe Rd','39600 Fremont Blvd','1600 Nantucket Cir','605 Orchard Ave','444 Saratoga Ave','201 W California Ave','486 Morello Ave','575 Berry Ave','1630 W Campbell Ave','203 Laurie Meadows Dr','900 Roanoke Dr','4170 Springlake Dr','1200 Ocean Ave','3055 La Selva','1032 W Remington Dr','2633 Ocean Ave','1600 Sand Hill Rd','852 Antoinette Ln','900 E Hillsdale Blvd','777 Shell Blvd','5608 Stevens Creek Blvd','1076 Carol Ln','20800 Homestead Rd','380 Esplanade Ave','700 Marlin Ave','415 A St 101','101 McLellan Drive','4500 Carlyle Ct','575 S Rengstorff Ave','850 Davit Ln','2000 Shoreline Cir','550 Moreland Way','250 Baldwin Ave','950 Redwood Shores Pkwy','1060 Foster City Blvd','3204 Casa De Campo Way','1987 Bridgepointe Cir','1200 E Hillsdale Blvd','200 Davey Glen Rd','1060 Continentals Way','338 S Fremont St','1080 Carolan Ave','703 Catamaran St','180 Pasito Terrace','707 Leahy St','459 Hamilton Ave','6304 Rancho Mission Rd','5280 Fiore Terrace','5679 Amaya Dr','5305 Toscana Way','6595 Montezuma Rd','67 E Flower St','10112 Ashwood St','3417 Lebon Dr','4424 44th St','7844 Paradise Valley Rd','2420 Cardinal Dr','4850 Talmadge Park Row','9505 Gold Coast Dr','7681 Palmilla Dr','10445 Mast Blvd','8685 Rio San Diego Dr','1250 Santa Cora Ave','910 Del Dios Hwy','12001 Woodside Ave','6575 Jaffe Ct','1501 E Grand Ave','1007 5th Ave','7576 Parkway Dr','7575 Linda Vista Rd','4555 Vandever Ave','4300 Echo Ct','3455 Kearny Villa Rd','1670 Kettner Blvd Ste 2','5320 Adobe Falls Rd','10122 Buena Vista Ave','12002 Wintercrest Dr','9072 Gramercy Dr','7039 Charmant Dr','5150 Balboa Arms Dr','10201 Camino Ruiz','601 S Twin Oaks Valley Rd','3883 Ingraham St','3950 Mahaila Ave','5504 Montezuma Rd','11102 Caminito Alvarez','8465 Regents Rd','11820 Paseo Lucido','12556 Oak Knoll Rd','7194 Schilling Ave','3115 Sweetwater Springs Blvd','3903 Conrad Dr','532 Broadway','561 Mc Intosh St','1982 Wellington Ln','2265 River Run Dr','900 F St','2715 Carlsbad Blvd','861 Anchorage Pl','6398 Del Cerro Blvd 8','1455 Kettner Blvd','3500 Windrift Way','8720 Costa Verde Blvd','600 Front St','989 Peach Ave','12330 9th St','345 Village Center Dr','2275 S Bascom Ave','501 Forest Ave','234 Escuela Ave','151 Calderon Ave','825 E Evelyn Ave','502 Mansion Park Dr','1212 Whipple Ave','4343 Renaissance Dr','150 Alicante Dr','100 N Whisman Rd','730 Agnew Rd','243 Buena Vista Ave','755 E Capitol Ave','1553 El Camino Real','355 E Evelyn Ave','555 E Washington Ave','3500 Granada Ave','655 S Fair Oaks Ave','505 Central Ave','575 E Remington Dr','600 Sharon Park Dr','700 Clark Way','1600 Villa St','1700 N 1st St','1235 Wildwood Ave','1575 Tenaka Pl','19608 Pruneridge Ave']
cities = ['San Francisco','San Francisco','Berkeley','San Francisco','Hayward','San Francisco','Alameda','San Francisco','El Sobrante','San Francisco','San Francisco','Belmont','San Francisco','Hayward','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','Berkeley','Walnut Creek','Foster City','San Francisco','Benicia','Richmond','San Francisco','San Francisco','San Francisco','San Francisco','Lafayette','Richmond','San Francisco','Mountain View','San Francisco','San Francisco','Sunnyvale','San Francisco','San Francisco','Alameda','San Francisco','San Francisco','San Bruno','Lafayette','San Francisco','Richmond','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','Daly City','San Francisco','San Francisco','San Francisco','San Mateo','Concord','Daly City','Milpitas','Santa Clara','Santa Clara','Fremont','Sunnyvale','Menlo Park','Sunnyvale','Fremont','Santa Clara','Hayward','Santa Clara','Sunnyvale','Martinez','Hayward','Campbell','San Mateo','Martinez','San Leandro','San Francisco','San Mateo','Sunnyvale','San Francisco','Palo Alto','South San Francisco','Foster City','Foster City','Cupertino','Lafayette','Cupertino','Pacifica','Foster City','Daly City','South San Francisco','Santa Clara','Mountain View','Redwood City','San Ramon','Santa Clara','San Mateo','Redwood City','Foster City','San Mateo','San Mateo','Foster City','Belmont','Belmont','San Mateo','Burlingame','Foster City','Sunnyvale','Redwood City','Palo Alto','San Diego','San Diego','La Mesa','San Diego','San Diego','Chula Vista','Lakeside','San Diego','San Diego','San Diego','San Diego','San Diego','San Diego','San Diego','Santee','San Diego','Chula Vista','Escondido','Lakeside','San Diego','Escondido','San Diego','La Mesa','San Diego','San Diego','La Mesa','San Diego','San Diego','San Diego','Santee','Lakeside','San Diego','San Diego','San Diego','San Diego','San Marcos','San Diego','San Diego','San Diego','San Diego','San Diego','San Diego','Poway','San Diego','Spring Valley','Spring Valley','El Cajon','Chula Vista','Vista','San Diego','San Diego','Carlsbad','Chula Vista','San Diego','San Diego','Oceanside','San Diego','San Diego','El Cajon','Poway','San Jose','Campbell','Palo Alto','Mountain View','Mountain View','Sunnyvale','Santa Clara','Redwood City','San Jose','San Jose','Mountain View','Santa Clara','Sunnyvale','Milpitas','Redwood City','Sunnyvale','Sunnyvale','Santa Clara','Sunnyvale','Mountain View','Sunnyvale','Menlo Park','Palo Alto','Mountain View','San Jose','Sunnyvale','Sunnyvale','Cupertino','Fremont','Santa Rosa','Novato','Rohnert Park','Fairfax','Petaluma','San Rafael','San Rafael','Sebastopol','Vallejo','Petaluma','Petaluma','Larkspur','Richmond','Santa Rosa','Santa Rosa','San Rafael','San Rafael','Vallejo','Petaluma','San Rafael','Sebastopol','Santa Rosa','Walnut Creek','Petaluma','San Rafael','El Cerrito','Rohnert Park','San Rafael','Santa Rosa','Vallejo','American Canyon','Petaluma','Richmond','Sunnyvale','Mountain View','Los Gatos','San Jose','Santa Clara','Santa Clara','Santa Clara','Sunnyvale','Sunnyvale','Sunnyvale','Cupertino','Santa Clara','Sunnyvale','San Jose','Santa Clara','San Jose','San Jose','Milpitas','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','Santa Cruz','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','Santa Cruz','Los Gatos','San Jose','Campbell','Gilroy','San Jose','Marina','Morgan Hill','Capitola','Salinas','Morgan Hill','San Jose','San Jose','San Jose','Santa Cruz','Monterey','Monterey','Salinas','Salinas','Salinas','Santa Cruz','Santa Cruz','Gilroy','Gilroy','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','Daly City','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','Brisbane','San Francisco','San Francisco','San Francisco','San Francisco','San Francisco','Daly City','San Francisco','Daly City','Colma','Daly City','San Francisco','Daly City','Daly City','Daly City','San Francisco','San Francisco','San Francisco','South San Francisco','South San Francisco','San Francisco','San Francisco','Daly City']

# Two zip codes that are in the same area. 94043, 94040, 94044, 94041
rnd_addresses = ['555 W Middlefield Rd','1035 Aster Ave','440 Dixon Landing Rd','101 Saratoga Ave','1599 Warburton Ave','330 N Mathilda Ave','355 N Wolfe Rd','1600 Nantucket Cir','444 Saratoga Ave','201 W California Ave','1630 W Campbell Ave','1032 W Remington Dr','1600 Sand Hill Rd','5608 Stevens Creek Blvd','20800 Homestead Rd','4500 Carlyle Ct','575 S Rengstorff Ave','550 Moreland Way','180 Pasito Terrace','459 Hamilton Ave','345 Village Center Dr','2275 S Bascom Ave','501 Forest Ave','234 Escuela Ave','151 Calderon Ave','825 E Evelyn Ave','502 Mansion Park Dr','4343 Renaissance Dr','150 Alicante Dr','100 N Whisman Rd','730 Agnew Rd','243 Buena Vista Ave','755 E Capitol Ave','355 E Evelyn Ave','555 E Washington Ave','3500 Granada Ave','655 S Fair Oaks Ave','505 Central Ave','575 E Remington Dr','700 Clark Way','1600 Villa St','1700 N 1st St','1235 Wildwood Ave','1575 Tenaka Pl','19608 Pruneridge Ave','745 S Bernardo Ave','1200 Dale Ave','347 Massol Ave','760 N 7th St','1901 Halford Ave','100 Buckingham Dr','1500 Vista Club Cir','902 W Remington Dr','732 E Evelyn Ave','718 Old San Francisco Rd','7375 Rollingdell Dr','2200 Monroe St','1257 Lakeside Dr','1300 The Alameda','431 El Camino Real','754 The Alameda','1600 Whitewood Dr','555 S Park Victoria Dr','355 Kiely Blvd','500 S Winchester Blvd','70 Descanso Dr','101 E San Fernando St 100','1776 Almaden Rd','2118 Canoas Garden Ave','360 S Market St','3200 Rubino Dr','950 Meridian Ave','1590 Southwest Expy','524 S 9th St','850 Meridian Way','1201 Parkmoor Ave','2050 Southwest Expy 126','4300 The Woods Dr','2600 Corde Terra Cir','3601 Copperfield Dr','2601 Nuestra Castillo Ct','10 Jackson St 107','1045 Coleman Rd','200 Hollis Ave','8200 Kern Ave','6100 Monterey Hwy','16945 Del Monte Ave','15400 Vineyard Blvd','6184 Cottle Rd','150 Palm Valley Blvd','5230 Terner Way','7397 Monterey St','500 Ioof Ave']
rnd_zip_codes = ['94043','94086','95035','95051','95050','94085','94085','95054','95050','94086','95008','94087','94304','95014','95014','95054','94040','95054','94086','94301','95134','95008','94301','94040','94041','94086','95054','95134','95134','94043','95054','94086','95035','94086','94086','95051','94086','94043','94087','94304','94041','95112','94089','94087','95014','94087','94040','95030','95112','95051','95051','95054','94087','94086','94086','95014','95050','94085','95126','95050','95126','95131','95035','95129','95128','95134','95112','95125','95125','95113','95125','95126','95126','95112','95126','95126','95126','95136','95111','95136','95127','95030','95123','95008','95020','95138','95037','95037','95123','95123','95136','95020','95020']
rnd_cities = ['Mountain View','Sunnyvale','Milpitas','Santa Clara','Santa Clara','Sunnyvale','Sunnyvale','Santa Clara','Santa Clara','Sunnyvale','Campbell','Sunnyvale','Palo Alto','Cupertino','Cupertino','Santa Clara','Mountain View','Santa Clara','Sunnyvale','Palo Alto','San Jose','Campbell','Palo Alto','Mountain View','Mountain View','Sunnyvale','Santa Clara','San Jose','San Jose','Mountain View','Santa Clara','Sunnyvale','Milpitas','Sunnyvale','Sunnyvale','Santa Clara','Sunnyvale','Mountain View','Sunnyvale','Palo Alto','Mountain View','San Jose','Sunnyvale','Sunnyvale','Cupertino','Sunnyvale','Mountain View','Los Gatos','San Jose','Santa Clara','Santa Clara','Santa Clara','Sunnyvale','Sunnyvale','Sunnyvale','Cupertino','Santa Clara','Sunnyvale','San Jose','Santa Clara','San Jose','San Jose','Milpitas','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','San Jose','Los Gatos','San Jose','Campbell','Gilroy','San Jose','Morgan Hill','Morgan Hill','San Jose','San Jose','San Jose','Gilroy','Gilroy']

email_services = ['gmail', 'outlook', 'aol']
def email_with_first_name(first_name, last_names):
    return "{}@{}.com".format(first_name, random.choice(email_services))

def email_with_first_dot_last_name(first_name, last_names):
    return "{}.{}@{}.com".format(first_name, last_names, random.choice(email_services))

def generate_email_address(first_name, last_name):
    #if len(first_name) < 8:
    #    return email_with_first_dot_last_name(first_name.lower(), last_name.lower())

    #return random.choice([email_with_first_name, email_with_first_dot_last_name])(first_name.lower(), last_name.lower())
    return email_with_first_dot_last_name(first_name.lower(), last_name.lower())

def get_rnd_first_name():
    return random.choice(first_names)

def get_rnd_last_name():
    return random.choice(last_names)

def generate_name():
    return "%s %s" % (random.choice(first_names), random.choice(last_names))

emails = []
def generate_identity():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email = generate_email_address(first_name, last_name)
    emails.append(email)
    return first_name, last_name, email

for i in range(10):
    generate_identity()

synonyms = {
  '01/10/1990': ['03/08/1990', '04/05/1990', '11/12/1990', '05/06/1989', '02/04/1989', '07/31/1988', '11/18/1989', '12/1/1988', '06/06/1986', '03/27/1987' ,'03/03/1988'],
  '3/2/1994': ['03/08/1994', '04/05/1994', '11/12/1994', '05/06/1994', '02/04/1994', '07/31/1993', '11/18/1993', '12/1/1993', '06/06/1994', '03/27/1994' ,'03/03/1993'],
  '8/8/1940': ['03/08/1940', '04/05/1941', '11/12/1942', '05/06/1950', '02/04/1961', '07/31/1966', '11/18/1970', '12/1/1973', '06/06/1967', '03/27/1954' ,'03/03/1967'],
}

dobs = ['01/10/1990', '3/2/1994', '8/8/1940']
property_worth = ['4000', '8000', '12000', '16000',
                  '20000','24000', '28000', '32000',
                  '35000', '40000', '50000', '60000', '70000', '80000', '90000', '100000']
medical_payments = ['1000', '2000']
personal_liability = ['100000', '300000', '500000']
deductible = ['100', '100 / 250', '250', '500', '750', '1000', '1500', '2500', '5000']

use_synonyms_cols = set(['Date of birth'])

# Fixed columns which actually have a list longer than 1 we need to find the values for even though we are not doing
# cross products.
# no_cross_products =

d = OrderedDict([
  # header0
  ('Insurance Type', (['Renters'], 'fixed')),
  ('Zip code', (zip_codes, 'fixed')),
  ('First name', (first_names, 'random')),
  ('Last name', (last_names, 'random')),
  ('Date of birth', (dobs, 'iterate')),
  ('Gender', (['m', 'f'], 'random')),
  ('Address', (addresses, 'fixed')),
  ('City', (cities, 'fixed')),
  ('State', (['CA'], 'fixed')),
  ('Zip code', (zip_codes, 'fixed')),
  ('Auto insurance coverage?', (['N', 'Y'], 'fixed')), # Y / N
  # header1
  ('Property Type', (['RENTED HOUSE - SINGLE FAMILY'], 'fixed')),
  ('# units', (['1', '2 to 4', '5+'], 'iterate')),
  #('# unrelated roommates', (['0', '1', '2', '3 or more'], 'fixed')),
  ('# unrelated roommates', (['0', '1', '2'], 'fixed')),
  ('roommate names', (('david', 'lee'), 'random')),
  #('# property losses in last 3 years', (['0', '1', '2', '3', '4', '5 or more'], 'fixed')), # '0', '1', '2', '3', '4', '5 or more'
  ('# property losses in last 3 years', (['0', '1', '2', '3', '4'], 'fixed')), # '0', '1', '2', '3', '4', '5 or more'
  ('Phone number', (phone_numbers, 'random')),
  ('Email address', (emails, 'random')),
  # Security systems.
  ('Fire Sprinkler System?', (['N', 'Y'], 'fixed')), # Y / N
  ('Central Fire & Burglar Alarm?', (['N', 'Y'], 'fixed')), # Y / N
  ('Local Fire / Smoke Alarm?', (['N', 'Y'], 'fixed')), # Y / N
  ('Home Security?', (['N', 'Y'], 'fixed')), # Y / N
  ('Non Smoking Household?', (['Y', 'N'], 'fixed')), # Y / N
  ('Local Burglar Alarm?', (['N', 'Y'], 'fixed')), # Y / N
  ('Unusual hazards?', (['NONE'], 'fixed')),
  ('Dogs that bite?', (['N', 'Y'], 'fixed')), # Y / N
  ('Run a business from home?', (['N'], 'fixed')),
  ('Start date', (['Keep default.'], 'fixed')),
  ('Personal property worth', (property_worth, 'iterate')),
  ('Loss of use', (['Keep default'], 'iterate')),
  ('Medical payments', (medical_payments, 'iterate')),
  ('Personal liability', (personal_liability, 'iterate')),
  ('Farmers Identity Protection', (['N', 'Y'], 'fixed')), # Y / N
  ('Deductible', (deductible, 'iterate'))
])

special_cross_cfgs = [
  (['Auto insurance coverage?', 'Fire Sprinkler System?', 'Central Fire & Burglar Alarm?',
    'Local Fire / Smoke Alarm?', 'Home Security?', 'Non Smoking Household?', 'Local Burglar Alarm?']),
  (['# property losses in last 3 years', '# units', 'Farmers Identity Protection'])
]

### Constants for model building.
from ml import model_cfg
model_configs = [
  model_cfg.ModelConfig(
    name='v1', learned_model_loc='renters-price-learn-v1.csv',
    memorized_model_loc = 'renters-price-v1.csv', cols_cfg=model_cfg.ColsCfg(
      cols_for_learning=['gender', 'dob'],
      cols_for_memorizing=['gender'],
    ),
    feature_map_loc = 'feature_map_v0.csv', feature_map2_loc = 'feature_map2_v0.pickle')
]
learned_config = model_cfg.LearnedConfig(
  raw_filenames = ['data/tdg_v0.csv'],
  model_configs=model_configs)

"""
    ('has_bite_dog', 'N'),
    ('age_group', 'middle-age'),

    ('insurance_type', 'renters'),
    ('full_address', '1599 Warburton Ave, Santa Clara, CA, 95050'),
    ('has_auto_insurance_coverage', 'Y'),

    ('has_fire_sprinkler_system', 'N'),
    ('has_center_fire_burglar_alarm', 'N'),
    ('has_local_fire_smoke_alarm', 'Y'),
    ('has_home_security', 'N'),
    ('is_non_smoking_household', 'Y'),
    ('has_local_burglar_alarm', 'N'),
    #
    ('farmers_identity_protection', 'Y'),
    ],
    cfs=[
    ('dob', 26.0), 

    ('unit_count', 2),
    ('property_losses_count', 3),

    ('personal_property_worth', 4000),
    ('medical_payments', 2000),
    ('personal_liability', 100000),
    ('deductible', 150.0)
"""
model_configs2 = [
  model_cfg.ModelConfig(
    name='v2', learned_model_loc='tmp/renters-price-learn-v2.csv',
    memorized_model_loc = 'tmp/renters-price-memorized-v2.csv', 
    cols_cfg=model_cfg.ColsCfg(
      # maybe include: 'medical_payments', 
      cols_for_learning=[
      'age_group', 'property_losses_count', 
      'unit_count',

      #'is_non_smoking_household',

      'personal_property_worth', 'deductible',
      'personal_property_value', 'personal_liability',

      #'has_bite_dog',
      #'has_fire_sprinkler_system', 'has_center_fire_burglar_alarm', 'has_local_fire_smoke_alarm',
      #'has_home_security', 'is_non_smoking_household', 'has_local_burglar_alarm', 
      ],
      cols_for_memorizing=[
      'has_bite_dog', 'age_group', 'insurance_type', 'full_address', 'has_auto_insurance_coverage',
      'has_fire_sprinkler_system', 'has_center_fire_burglar_alarm', 'has_local_fire_smoke_alarm',
      'has_home_security', 'is_non_smoking_household', 'has_local_burglar_alarm', 
      'farmers_identity_protection', 'unit_count', 'property_losses_count',
      'personal_property_worth', 'medical_payments', 'personal_liability', 'deductible'
      ],
    ),
    feature_map_loc = 'tmp/feature_map_v2.csv', feature_map2_loc = 'tmp/feature_map2_v2.pickle')
]
learned_config2 = model_cfg.LearnedConfig(
  raw_filenames = ['data/elance_v2/*.csv'],
  model_configs=model_configs2)

if __name__ == '__main__':
    name = generate_name()
    print(name)
