# Template Module for Easytopic New Architecture

## Introduction

This module is a template for a basic module in python made to fit Easytopic's new architecture. By getting started with this template you should be able to develop a module that can connect and work with the whole system in no time.

You are free to reestructure the folders in the project, but make sure to do the right ajustments. Currently the template module contains a trivial piece of code in the processing part that gives every entry back, just so that you can see how it basically works.

## Module Specs

Make sure to edit your module specs in the `module-name-specs.json`. In this `json` file, you can specify the inputs and the outputs that your module will work with. The id of each field will be the key to that info in the dictionary you get when a message is received, so it is important that this is well defined and matching.

## Requirements

In the `requirements.txt` file you can define all python packeges you will need. The `Dockerfile` is configured to install all the requirements with `pip`.

## Dockerfile

The `Dockerfile` is configured to start a basic Docker container, and you can change that file according to your needs. You can define a specific command that needs to be executed in your container, for example.

## Docker Compose

The architecture uses docker compose to start all modules since basically everything is dockerized. Here the `docker-compose.yml` is not really needed, but can be used to help in the development stage and also help to visualize what configurations and environment variables will need to be passed to de module.

## src

Finally, the project itself is found inside the `src` folder. In this template, there is only a `worker.py` file that contains everything, since the connection process until the actual work that needs to be done. The `callback` function is the only function will actually need to change, specifying what will be done with the input (keys need to match the id in the specs) that comes in the `msg` dictionary and giving the output (also the ones specified in the specs) back inside the same dictonary, that will be sent to the output queue.

## General information

The template module uses `pika` library to connect to RabbitMQ, that will handle the messages. The presset configuration made here is basically to simplify the connection process of the module to the rest of the architecture. By following the same pattern, you could use any programming languange to fit the patterns and work with everytinhg as well.