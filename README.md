# ChatQL
GraphQL based chat engine

## Dependencies
This module depend following system environment.

- python >= 3.6
- mongodb >= 4.0

Following dependency python modules are installed when `pip install`.

- graphene >= 2.1
- mongoengine >= 0.16.3

## Demo
You clone this repository and run following commands.

After, you can access GraphQL interface `POST localhost:8080/graphql`.

Please check response by GraphQL tool (ex: [GraphiQL](https://electronjs.org/apps/graphiql)).
```
docker build ./demo -t chatql --force-rm=true
docker run -p 8080:5000 -it chatql
```

## TODO
- Application Function
    - [ ] Response Generator with Template Engine
    - [ ] Extract Entity with Template Matching
    - [ ] Non Text Query
    - [ ] Intent Estimator with Machine Learning
    - [ ] Extract Entity with Machine Learning
- Document
    - [ ] API Docs 
    - [ ] Conditions Pattern Docs
    - [ ] Response Docs

## License
MIT License.