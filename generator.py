import random
from datetime import timedelta, datetime


FILENAME = "input.txt"

TITLES = [
    "Life",
    "Kong: Skull Island",
    "Harry Potter and the Goblet of Fire",
    "The Maze Runner",
    "Now You See Me",
    "Shutter Island",
    "Spectre",
    "Logan",
    "The Mother of Tears",
    "Alien",
    "The Hunger Games: Catching Fire",
    "Avatar",
    "Pirates of the Caribbean: Dead Men Tell No Tales",
    "Furious 7",
    "Chappie",
    "Insurgent",
    "The Prestige",
    "John Wick: Chapter 2",
    "Ted 2",
    "Fantastic Beasts and Where to Find Them",
    "Memento",
    "Terminator 2: Judgment Day",
    "Teen Titans: The Judas Contract",
    "Your Name.",
    "Harry Potter and the Deathly Hallows: Part 2",
    "The Magnificent Seven",
    "Ice Age",
    "Minions",
    "The Dark Knight Rises",
    "Harry Potter and the Philosopher's Stone",
    "Nocturnal Animals",
    "Fifty Shades Darker",
    "Spirited Away",
    "Captain America: Civil War",
    "Get Out",
    "Big Hero 6",
    "Django Unchained",
    "Aliens",
    "Tomorrow Everything Starts",
    "The Invisible Guest",
    "Se7en",
    "Aftermath",
    "Smurfs: The Lost Village",
    "The Hateful Eight",
    "Titanic",
    "Dogtooth",
    "Silence",
    "The Hobbit: An Unexpected Journey",
    "Lion",
    "The Revenant"
]

PROVIDERS = [
    "Warner bros",
    "Buena Vista",
    "Paramount",
    "20th Century",
    "Sony Pictures",
    "Miramax",
    "DreamWorks",
    "New Line",
    "MGM",
    "Lionsgate"
]

STB = 10

ENTRIES = 100


def random_time():
    start = datetime.strptime('2017-04-01 12:00', '%Y-%m-%d %H:%M')
    end = datetime.strptime('2017-04-21 12:00', '%Y-%m-%d %H:%M')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

count = 0

while count < ENTRIES:
    with open(FILENAME, 'a') as file:
        box_id = 'stb' + str(random.randint(1, STB))
        title = random.choice(TITLES)
        provider = random.choice(PROVIDERS)
        time = random_time()
        revenue = float(random.randint(1, 10))
        line = box_id + '|' + title + '|' + provider + '|' + datetime.strftime(time, '%Y-%m-%d') \
               + '|' + '{0:.2f}'.format(revenue) + '|' + datetime.strftime(time, '%H:%M') + '\n'
        file.write(line)
        count += 1
