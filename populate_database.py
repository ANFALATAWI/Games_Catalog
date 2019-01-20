from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Studio, Base, Game

engine = create_engine('sqlite:///studios.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Data:

# Studios
activision_studio = Studio(name='Activision', founded_date='1979', founder='David Crane')
naughtyDog_studio = Studio(name='Naughty Dog', founded_date='1984', founder='Andy Gavin')
toysForBob_studio = Studio(name='Toys For Bob', founded_date='1989', founder='Paul Richie III')
# Committing:
session.add(activision_studio)
session.add(naughtyDog_studio)
session.add(toysForBob_studio)
session.commit()

# Games
pitfall = Game(name='Pitfall', description='Pitfall! is a video game designed by David Crane for the Atari 2600 and released by Activision in 1982. The player controls Pitfall Harry and is tasked with collecting all the treasures in a jungle within 20 minutes while avoiding obstacles and hazards.',
 release_date='1982', quantity='7', price='10$', studio=activision_studio)
destiny = Game(name='Destiny', description='Destiny is an online-only multiplayer first-person shooter video game developed by Bungie and published by Activision. It was released worldwide on September 9, 2014, for the PlayStation 3, PlayStation 4, Xbox 360, and Xbox One consoles. Destiny marked Bungie\'s first new console franchise since the Halo series, and it was the first game in a ten-year agreement between Bungie and Activision. Set in a "mythic science fiction" world, the game features a multiplayer "shared-world" environment with elements of role-playing games.',
 release_date='2014', quantity='130', price='75$', studio=activision_studio)
crashBandicoot = Game(name='Crash Bandicoot', description='The games are mostly set on the fictitious Wumpa Islands, an archipelago situated to the south of Australia where humans and anthropomorphic animals co-exist, although other locations are common. The main games in the series are largely platformers, but several are spin-offs in different genres. The protagonist of the series is an anthropomorphic bandicoot named Crash, whose quiet life on the Wumpa Islands is often interrupted by the games\' main antagonist, Doctor Neo Cortex, who created Crash and wants him dead. In most games, Crash must defeat Cortex and foil his plans for world domination.',
 release_date='1996', quantity='20', price='60$', studio=naughtyDog_studio)
jakAndDaxter = Game(name='Jak and Daxter', description='The games are considered story-based platformers that feature a mixture of action, racing and puzzle solving. The series is set in a fictional universe that incorporates science fantasy elements, and centers on the eponymous characters as they try to uncover the secrets of their world, and unravel the mysteries left behind by an ancient race of Precursors.',
 release_date='2001', quantity='23', price='40$', studio=naughtyDog_studio)
uncharted = Game(name='Uncharted', description='Uncharted is an action-adventure third-person shooter platform video game series developed by Naughty Dog and published by Sony Interactive Entertainment for PlayStation consoles. The series follows protagonist Nathan "Nate" Drake (portrayed by Nolan North through voice and motion capture), a charismatic yet obsessive treasure hunter who journeys across the world to uncover various historical mysteries.',
 release_date='2007', quantity='51', price='60$', studio=naughtyDog_studio)
# Commiting
session.add(pitfall)
session.add(destiny)
session.add(crashBandicoot)
session.add(jakAndDaxter)
session.add(uncharted)
session.commit()

print '**Data added succsesfully**'





