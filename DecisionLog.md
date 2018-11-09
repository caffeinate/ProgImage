# ProgImage Decision Log

why it's been done like this!

* *No Usership* - In real world apps someone owns the data and there is authentication and authorisation around this. There is nothing in the requirements for this.

* space limiting or clearing old cache isn't covered

* without data discovery (via API) it's easy loose uploaded images. Not covered.



## Missing parts

Development is time boxed, here is what I'd add next

* proper MIME detection and responses
* HAL or JSON-LD or something more discoverable. Would be useful to know which transforms are available.
* The `ImageAnvil()` transform shouldn't be called within the web request, it should be sent to a queue and should wait for the response. A pool of workers should process items in the queue. Before an item is processed a check should be made to see if already processed (i.e. whilst the request was in the queue).
* Retrieving the image to process from a URL is part of the spec. this is missing.
* Finish user passing arguments to the transform - e.g. image size for the thumbnail
* Swagger doc.
