# evolution-sim

## Usage
### Docker:
+ Install docker desktop
+ Run `$ docker compose up` or `$ docker compose -d` (run in background)
+ Try the following either with a browser or curl (recommend curl for testing backend):
**Caution**: This will open port 8080 on the machine it is run on.

#### Frontend:
```
# Index route: (home page)
$ curl http://localhost:8080/

# Simulation viewer: (would recommend using browswer to appreciate visuals)
$ curl http://localhost:8080/sim.html
```

#### Backend:
```
# HTTP/1.0 GET / (note the trailing slash...)
$ curl http://localhost:8080/evol/

# HTTP/1.0 GET /run
$ curl http://localhost:8080/evol/run

## Not implemented yet ##
# HTTP/1.0 POST /load
$ curl -X POST -d 'key=value' http://localhost:8080/evol/load
```
