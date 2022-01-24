# kinopoisk unofficial API

This is simple python package for getting data from [unofficial kinopoisk API](https://kinopoiskapiunofficial.tech).

## Installing

**pip**

```bash
pip install kinopoisk-unofficial-api
```

**poetry**

```bash
poetry add kinopoisk-unofficial-api
```

## Getting token

Why this not work. What the token and why this require it from me?
For interact to [API](https://kinopoiskapiunofficial.tech) you should getting api token. That get it you need sign up to [their site](https://kinopoiskapiunofficial.tech/signup). After register go to profile and save your token somewhere.

## How to use

For begin you should create the **KPClient** instance.

```python
from kinopoisk import KPClient

client = KPClient(<your token>)
```

When you have client you can used all functional this library.

### Getting movie

```python
matrix = await client.get_movie_data(301)
print(matrix)
```

You can get e.g. name, release date, raiting, length of this movie and more.

```python
matrix.name.en
'The Matrix'
matrix.year
1999
matrix.length
136
```

If you not know movie id (that to be often) may use another method named ***search_movie***

```python
answer = await client.search_movie('Mr. Robot')
mr_robot = answer[0] # If you search popular movie, that usually this movie should be to first
```

### Getting data of movie
In previous example we got tv series. By default it take without it seasons. That load it you should get it id and call to method of client  ***get_seasons_data***

```python
seasons = await client.get_seasons_data(mr_robot.id.kinopoisk)
for season in seasons:
	print(season.episodes)
```

Yet this not exactly conveniently. Store seasons and it tv series between it may be not good idea. So that, you may not splitting data, for it need call tv series method ***load_seasons***.

```python
await mr_robot.load_seasons(client)
for season in mr_robot.seasons:
    print(season.episodes)
# Or just
for season in mr_robot:
    print(season.episodes)
```

Season have a episodes (Seriously?) that may be get it same way.

```python
for season in mr_robot:
    for episode in season:
        print(episode.name.en)
		# First episode named 'eps1.0_hellofriend.mov'
```

### Getting facts and bloopers of movie

```python
for fact in await client.get_facts(mr_robot.id.kinopoisk):
	print(fact.text)
```

### Getting persons

```python
bc = (await client.search_person('Benedict Cumberbatch'))[0]
await bc.get_all_data(client)
print(bc.birthday.strftime("%d %B, %Y"))
# Output 19 July, 1976
```

Or you can get persons of some movie

```python
persons = await mr_robot.get_persons(client)
actors = []
for person in persons:
    if person.is_actor:
        actors.append(person)
for actor in actors[:10]: print(f'{actor.name.en}: {actor.character}')
```

### Getting reviews

```python
reviews = await mr_robot.get_reviews(client)
for review in reviews: print(f'{review.author} - {review.title}:\n{review.text}')
```

