# Changelog

## [v2.0.0] - unreleased

* Remove deploy module
* Add rest.controller module
* Rename client module to microservices

## [v1.3.0]

* Ability to deploy ioFog microservices, and connections through SDK are now available.
    * This can be imported through iofog_python_sdk.deploy options.
    * Previous standard iofog_python_sdk can be imported through iofog_python_sdk.microservices
* Added standards for rest calls made to ioFog under deploy.create_rest_call
* Fixed issue with python3 object handling
