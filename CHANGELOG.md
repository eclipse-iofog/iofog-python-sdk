# Changelog

## [v3.0.0-beta] - 13 Auguest 2021

* No changes from alpha4

## [v3.0.0-alpha4] - 20 July 2021

* Add appropriate time delay between retries in REST client

## [v3.0.0-alpha3] - 20 July 2021

* Add retries to REST client for 503 etc

## [v3.0.0-alpha2] - 6 July 2021

* Change rest.controller module to take base_url in constructor

## [v3.0.0-alpha1] - 23 March 2021

* Remove deploy module
* Add rest.controller module
* Rename client module to microservices
* Add microservices.log module

## [v1.3.0]

* Ability to deploy ioFog microservices, and connections through SDK are now available.
    * This can be imported through iofog.deploy options.
    * Previous standard iofog can be imported through iofog.microservices
* Added standards for rest calls made to ioFog under deploy.create_rest_call
* Fixed issue with python3 object handling
