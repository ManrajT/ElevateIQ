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
I chose Python because it's easy to set up, I've used it recently, and it's simple to accomplish simple glue work like this.  For the API endpoint, I chose to use FastAPI because it's fast to set up and additional functionality of API endpoints like Django REST API are not needed right now. 









Reflection on productionization:
================================
In production, we'd prefer to bundle packages with applications to ease setup and better control what's running in production. We can do this through containers, virtual envs, or python tools like setup tools.  We might also prefer running a more powerful api framework like Django REST framework because after setup, the advanced features may speed development.  Also, we may wish to run the web server separately from the asgi server, for example nginx in front of uvicorn, because we can scale each independently and cache and filter requests. 
