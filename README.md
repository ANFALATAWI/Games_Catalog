# Games_Catalog
Project 4 for Udacity's full stack nano degree
This project is a website that is developed using the [Flask](http://flask.pocoo.org) framework, It’s a menu for available games a store has, categorized  by studios that developed those games.
A user can log in using the third party Google authentication system, and add their own studios and games, other users cannot modify a given user’s added data.

## Built With
* [Flask](http://flask.pocoo.org)  - The web framework used
*  [PostgresSQL](https://www.postgresql.org)  - Database management
*  [Google Oauth](https://developers.google.com/identity/protocols/OAuth2)  - Authentication used

## Getting Started
### Install the virtual machine
Here Virtual Box + vagrant were used.
* [Install Virtual Box](https://www.virtualbox.org/wiki/Downloads)
* [Install Vagrant](https://www.vagrantup.com/downloads.html)
* [Download the VM configuration](https://github.com/udacity/fullstack-nanodegree-vm)

run `$ vagrant up`  to set up vagrant then `$ vagrant ssh`  to log in to the Linux VM.

### Set up the files
Download the Games Catalog folder in your vagrant directory, run vagrant ssh, cd to /vagrant, where your .py files should exist:
Run `$ python database_setup.py` to configure the database.

This should creat a *studios.db* file in your directory, and you should see a message
`Database has been setup succesfully`

Run `$ python populate_database.py` to populate the database with initial dummy data.

This should print a message
`**Data added succsesfully**`

## Running this program
To run this program, type `$ python games_catalog.py`  to run.
Now to view this website, navigate to http://localhost:5000/ on your favorite web browser, you should see the landing page.

## JSON endpoints
there are three endpoints for this website
* Extracting a spesefic studio's data at http://localhost:5000/studios/studio_id/games/JSON will show
```
{
  "Games": [
    {
      "description": "foo", 
      "id": 1, 
      "name": "Pitfall", 
      "price": "10$", 
      "quantity": 7, 
      "release_date": "1982"
    }, 
    {
      "description": "bar", 
      "id": 2, 
      "name": "Destiny", 
      "price": "75$", 
      "quantity": 130, 
      "release_date": "2014"
    }
  ]
}
```
* Extracting a spesefic game's data at http://localhost:5000/studios/studio_id/games/game_id>JSON will show
```
{
  "Game": {
    "description": "foo", 
    "id": 1, 
    "name": "Pitfall", 
    "price": "10$", 
    "quantity": 7, 
    "release_date": "1982"
  }
}
```
* Extracting all studio data at http://localhost:5000/studios/JSON will show
```
{
  "Studios": [
    {
      "founded_date": "1979", 
      "founder": "David Crane", 
      "id": 1, 
      "name": "Activision"
    }, 
    {
      "founded_date": "1984", 
      "founder": "Andy Gavin", 
      "id": 2, 
      "name": "Naughty Dog"
    }, 
    {
      "founded_date": "1989", 
      "founder": "Paul Richie III", 
      "id": 3, 
      "name": "Toys For Bob"
    }
  ]
}
```

### Reference:
Udacity’s [Restaurant Menu website](https://github.com/udacity/Full-Stack-Foundations/tree/master/Lesson-4/Final-Project)

