# BucketHoarder

BucketHoarder was built to perform searches via the GrayHat Warfare APIs and then download all files matching the query.

Things may break as the APIs are updated.

Once intsall run BucketHoarder with the help command to understand how to format queries.

```
./buckethoarder.py --help
```

## Requirements

For most *nix machines.

1. **Python 3.10** would be needed as some of the statement values are python 3.10 only
2. Recommendation is to use `virtualenv`

```
git clone https://github.com/Neuvik/BucketHoarder
cd BucketHoarder
python3 -m 'venv' venv
source bin/env/activate
pip3 install -r requirements.txt
```

The files.py which recursively looks at all the directories will require libmagic to be installed.

For MacOS

```
brew install libmagic
```

Create a .env file within the BucketHoarder directory and add your API key in the following format
```
API_KEY=API KEY HERE
```

