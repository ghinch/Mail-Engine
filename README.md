# Mail Engine for App Engine

## About

Mail Engine is an application which allows you to run your own email service application, with a REST interface and simple administration page, on Google App Engine. It is released under a BSD open source license for you to use in your own appliaction work.

## Installation

First, get the App Engine SDK for Python and install it

### Run locally

Open the SDK, add an application which uses the download directory of Mail Engine, and run it. By navigating to the page and port you chose, you should see the Mail Engine admin page. Note that you will not be able to actually send any email from Mail Engine while running it locally.

### Deploy to AppSpot

Before deploying, you will need to create an application with a unique name on App Engine. Once you've done that, open app.yaml and edit the application name to be that unique name. You may also change the application version to be whatever you like, but note that any settings you configure are keyed to that version, so after deploying and configuring once, do not change the version unless you want to have multiple configurations running. 

Once you've deployed, go to http://{app-name}.appspot.com and you will be brough to the admin configuration panel.

## Configuration

You will need to add a few settings before you can use Mail Engine:

- Auth Key : A unique text key that will be used in combination with other parameters to generate the security token used when making REST requests to Mail Engine. This should be unique (ideally a hash of some kind) and kept secret. You will need the same key stored somewhere in your application that makes requests of Mail Engine.
- Default Sender : An email address to be used as the default From: address in emails sent by Mail Engine. Must be an address that is associated with the App Engine account Mail Engine is deployed to
- Default Subject : The default subject attached to messages sent by Mail Engine
- Allowed IPs : (optional) Comma separated whitelist of IP addresses Mail Engine should screen for and only accept requests from.

## Usage

Requests are send to Mail Engine via HTTP POST, to the url http://{app-name}.appspot.com/post. The following parameters should be sent:

- recipients : Comma separated list of email addresses to receive the message
- subject : The email subject
- body : The email body
- sender : The email address of the sender, which should be associated with the same App Engine account

Additionally, for authentication, a token must be sent in the header of all requests named "Mail-Engine-Auth-Token". It will be a SHA1 hash of the key/values you've posted, in alphabetical order by key and url encoded, with the Auth Key you configured concated to the end. something like:
	> hashlib.sha1(urllib.urlencode(PARAMS.sort()) + SECRET).hexdigest()

##  Future

It's a simple service for now, but hopefully useful, and I'll add more to it as I am able, such as additional functionality to the admin pages, and (maybe) some bounce tracking support.
