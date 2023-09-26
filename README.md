# a_foBOT

**Discord Bot app** open for quick extensions with an automated way of testing, and deploying image for the DockerHub.
- [Project Image](https://hub.docker.com/repository/docker/afod3v/afobot/general)

This project can be run with any cloud service that is allowing to handle environment variables.. those variables had to be injected during the process of building container.

- `DISCORD_TOKEN=YOUR_TOKEN_HERE` - this is your discord access token
- `SECRET_KEY=YOUR_KEY_HERE` - this is your key for calling simple user level interface

<br>

In order to launch this project locally (Windows) we can use command:

`docker run -d -e DISCORD_TOKEN=$env:DISCORD_TOKEN -e SECRET_KEY=$env:SECRET_KEY a_fobot:latest`

> Of course before executing anything.. we have have to set those variables in system...

## Secret Menu

`Secret Menu` is allowing us to control some of the bot options from the user level.

**Common way:** 
```
0123456789 - entering your secret key like that is going to call option menu.

0123456789 0 1 - this format is allowing us to set value of the option number 0 to True which is going to enable that feature.
```
**Hidden way:**

Users that are not on the white list are not going to be able to execute any of the command, but anyway we can hide our code in the spoiler tag to prevent them from getting that code before message is going to get deleted...

When typing in the Discord - we can hide our phrase with a use of spoiler tag `||text||`

```
||key_phrase||
||key_phrade option mode||
```
