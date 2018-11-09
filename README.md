# ProgImage
a coding challenge, not real, just for fun.

It's a [Flask](http://flask.pocoo.org/) app for RESTFul API image storage transformation. It's just a demo, the [decision log](DecisionLog.md) details the differences between real world and demo as well as why it's structured as it is.


## Running it locally

### Setup

Virtual environment is your choice. Instructions here are with one.

```Shell
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

### Unit tests

get `venv` shell as above

```Shell
export PYTHONPATH=`pwd`
python3 prog_image/test/test_all.py 
```

## Running it locally

create your own config by copying the template and editting anything there that needs changing.

```Shell
cd prog_image/settings/
cp local_config_template.py local_config_yourname.py
ln -s local_config_yourname.py local_config.py
cd ../..
```
i.e. `local_config.py` is used in the next bit.

```Shell
export PYTHONPATH=`pwd`
python3 prog_image/app.py
```

You should now see a message saying the port it's running on.


## Using it

For the examples below I'll assume it's running as `http://127.0.0.1:5070/`. And I'm using [HTTPie](https://httpie.org) but you might want to use curl or wget etc...

Send an image
```Shell
http --form POST localhost:5070 image=@IMG_1780.JPG
```
