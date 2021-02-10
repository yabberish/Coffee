# Coffee
Coffee is a discord moderation bot made by elflanded.

# Links

  [Contributing](docs/CONTRIBUTING.md)
  
  [CODE of CONDUCT](docs/CODE_OF_CONDUCT.md.md)


# Self-hosting.

*Instructions to install the bot for your own personal use*

Start by cloning the repository using the following command:
```sh
git clone https://github.com/elfq/Coffee.git
```

Then rename `.env.example` to `.env` and open it with a text editor, and change the values.

*you may need to check if you can view hidden files on windows to access this file!!!*

```py
DISCORD_TOKEN=your_token
DISCORD_PREFIX=your_prefix
```

Don't include any quotes when setting your values!

**Windows Setup**

Once you're done setting up .env, go to the folder again, and open the `setup.bat` file, then it will setup itself. Alternatively you can run:

```sh
venv\Scripts\activate.bat
py -3 -m pip install -r requirements.txt
```

**MacOS & Linux setup:**

Open up terminal, and locate the folder, once you've located it run the following command.

`pip3 install -r requirements.txt`

Once all modules finish installing, run `python main.py`, and the bot will be setup!

**Important**

You need to have python installed for this, please go [here](https://www.python.org/downloads/) to install the latest version of python!

