Instructions on how to run: 
==========================
- Install dependencies
   - pip3 install fastapi  (api framework) 
   - pip3 install uvicorn  (webserver) 
   - pip3 install requests (http requests)

- Run server: 
   - uvicorn main:app --reload --port 9000

- Run queries by either: 
   
   a) open browser at 127.0.0.1:9000/incidents
   
   b) curl -X 'GET' 'http://127.0.0.1:9000/incidents' -H 'accept: application/js


Reflection on approach:
======================
I chose Python because it's easy to set up, I've used it recently, and it's simple to accomplish simple glue work like this.  For the API endpoint, I chose to use FastAPI because it's fast to set up and additional functionality of API endpoints like Django REST API are not needed right now.  From studying the assignment requirement that we return results, I concluded that we should cache the data and refresh frequently so we're aware of all security events.  Obviously the APIS can fail so I implemented retry logic, and to avoid retrying too much some backoff as well.  For grouping and sorting that data, I just initialized a dict with fields for each customer and inserted fields in correct places.  I wasn't sure if we we're supposed to sort employees by most recent incident time, so I just sorted events inside the priority levels.


Reflection on productionization:
================================
In production, we'd prefer to bundle packages with applications to ease setup and better control what's running in production. We can do this through containers, virtual envs, or python tools like setup tools.  We might also prefer running a more powerful api framework like Django REST framework because after setup, the advanced features may speed development.  Also, we may wish to run the web server separately from the asgi server, for example nginx in front of uvicorn, because we can scale each independently and cache and filter requests. For backoff, we may wish to use exponential backoff and include some jitter as well.  If we're caching lots of data, we should use an external cache like redis or memcache and perhaps shard across multiple.  We would want to double check the rate at which we can call APIs and set them correctly. 
