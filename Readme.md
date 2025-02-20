# GDriveAuto

CLI application for handling automated tasks for google drive.

## Features

* Create a new folder on google drive (if the folder doesn't exist already)
* Work in progress more features to come later...

## Getting Started
### Prerequisites

1. Create a new Google Cloud project or use an existing one: https://developers.google.com/workspace/guides/create-project
2. Enable Drive API for your project: https://developers.google.com/workspace/guides/enable-apis
3. Configure OAuth and download access credentials json file: https://developers.google.com/workspace/guides/configure-oauth-consent
4. Rename the downloaded file to `credentials.json` and move it to the root of the project.
5. Run `pip install -r requirements.txt`

## Usage
Show available options by running:
`python gdrivecli.py -h`

Create a new folder on Google drive by running:
`python gdrivecli.py -f foldername`
