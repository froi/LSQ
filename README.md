# Morsel

## Purpose

During our day to day we create and run one time code snippets to solve a number of problems. Sometimes these problems come back with a vengeance. It's not always easy to find the scripts that were used for the problem, if they're found at all. Also many times there's not an easy way to comment on the solutions.

With this tool we can save our snippets and let us comment and collaborate on them

## Requirements

- MongoDB (2.4+)
- Python (2.7)
- Virtualenv / Virtualenv Wrapper

## Installation 

- Start the MongoDB daemon 

        $ mongod 

- Clone HL Snippet

        $ git clone git@github.com:froi/morsel.git

- Change to the directory

        $ cd morsel

- Set up a virtual environment and activate it

        $ virtualenv env
        $ source env/bin/activate

- Install Python requirements

        $ pip install -r requirements.txt

- Copy the `config.py.sample` to `config.py` and change as required

        $ cp config.py.sample config.py
        $ vim config.py

- Run the app

        $ python app.py

Point your browser to `http://localhost:<port>` and you're good
to go.

## Screenshots

![Login page](http://i.imgur.com/7qtVk7p.png)

---

![Landing page](http://i.imgur.com/BdA1Kbk.png)

---

![Add Snippet](http://i.imgur.com/4FabXwI.png)

---

![Edit Snippet](http://i.imgur.com/FoyCQw2.png)

---

![View Snippet](http://i.imgur.com/ViYebIg.png)

---

![Delete Snippet](http://i.imgur.com/HcGHqhH.png)

---

## Roadmap

* Full Text Search
* Version Control (big maybe)

