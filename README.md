# ProgImage
a coding challenge, not real, just for fun.

It's a [Flask](http://flask.pocoo.org/) app for RESTFul API image storage transformation. It's just a demo, the [decision log](DecisionLog.md) details the differences between real world and demo as well as why it's structured as it is.

## Overview

* No database
* Meta data is stored alongside images in a object store.
* Filesystem can be used as the object store
* Image transforms (make thumbnail etc.) are cached in the object store

## Example Deployment on AWS

App running in gunicorn on EC2 instance within auto scaling group behind load balancer (either type). Shared filesystem for object store is EFS.


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

For the examples below I'll assume it's running as `http://127.0.0.1:5070/`. And I'm using curl but you might want to use httpie or wget etc...

Send an image
```Shell
curl -v -F "image=@IMG_1780.JPG" localhost:5070
```

You should see 'Location' in the returned http header. This is the URL for the stored image to be retrieved.

Transforms of the image can retrieved with a url of the format `http://localhost:5070/images/<ident>/<transform>/`.

Worked example, some lines have been removed for readability.

```Shell
curl -v -F "image=@14590987878890.jpg" localhost:5070
> POST / HTTP/1.1
> Host: localhost:5070
> User-Agent: curl/7.54.0
> Accept: */*
> Content-Length: 280866
> Expect: 100-continue
> Content-Type: multipart/form-data; boundary=------------------------9050b98ac18a3548
> 
< HTTP/1.1 100 Continue
* HTTP 1.0, assume close after body
< HTTP/1.0 201 CREATED
< Content-Type: application/json
< Content-Length: 71
< Location: http://localhost:5070/images/89387845b87c8aa70ab5f433b84148c193286d22/
< Server: Werkzeug/0.14.1 Python/3.6.5
< Date: Fri, 09 Nov 2018 15:32:32 GMT
< 
{
  "id": "89387845b87c8aa70ab5f433b84148c193286d22", 
  "msg": "ok"
}

curl http://localhost:5070/images/89387845b87c8aa70ab5f433b84148c193286d22/ > image_copy.jpeg

curl http://localhost:5070/images/89387845b87c8aa70ab5f433b84148c193286d22/thumbnail/ > image_copy_thumbnail.jpeg
```


### On demand images

The source image is POSTed to a transform. In this case a thumnail. The response returns the thumbnail which is being saved to `file.jpeg`.

```Shell
curl -v -F "image=@14590987878890.jpg" localhost:5070/on_demand/thumbnail/ > file.jpeg
```


## Missing parts

Development is time boxed, here is what I'd add next

* proper MIME detection and responses
* HAL or JSON-LD or something more discoverable. Would be useful to know which transforms are available.
* The `ImageAnvil()` transform shouldn't be called within the web request, it should be sent to a queue and should wait for the response.
* Retrieving the image from URL is part of the spec. this is missing.
* Finish user passing arguments to the transform - e.g. image size for the thumbnail
* Swagger doc.
