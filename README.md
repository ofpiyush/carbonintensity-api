# CarbonIntensity API

API server for pseudo-realtime production carbon intensity data in gCO2eq/kWh for any zone supported by https://github.com/tmrowco/electricitymap-contrib.

## Installation and running

### With Docker

```
docker run -p 80:80 ofpiyush/carbonintensity-api:stable
```

### Local

The code has been teted working on Python `3.7.0`. It should work in compatible versions. You can use [pyenv](https://github.com/pyenv/pyenv#installation) to manage python versions

1. Fork and clone this repository and submodules

   Replace `<username>` with your github username.

   ```
   git clone --recurse-submodules git@github.com:<username>/carbonintensity-api
   ```

1. Install dependencies

   Within your virtualenv

   ```
   pip install -r requirements.txt
   pip install -r electricitymapcontrib/parsers/requirements.txt
   ```

1. Start the server
   ```
   python app.py
   ```

## Usage

Change `http://localhost` to the host and port combo of your environment.

```bash
curl 'http://localhost/carbon-intensity/latest?zone=IN-KA'
{
  "zone": "IN-KA",
  "carbonIntensity": 474,
  "datetime": "2020-11-21T04:30:00Z",
  "updatedAt": "2020-11-21T04:30:00Z"
}
```

## Motivation

This API server is meant to be a self-hosted, free drop-in replacement of https://api.electricitymap.org/v3/carbon-intensity/latest endpoint. ([Documentation](http://static.electricitymap.org/api/docs/index.html#live-carbon-intensity))

While working on https://github.com/thegreenwebfoundation/grid-intensity-go, I needed a test server to check my client implementation of https://api.electricitymap.org.

## Goals

- Be a free, API compatible replacement of https://api.electricitymap.org/v3/carbon-intensity/latest.
- Be capable of testing or light loads (like the ones from a perioidically running kube-scheduler-plugin)

## Non-Goals

- Add sophisticated modeling methods to get more accuracy.
- Be a complete replacement for all endopoints of api.electricitymap.org/v3.

## Contributing

1. Create an issue with the problem you're trying to solve or improvement you'd like to see.
1. Fork and clone the repo.
1. Use the local install guide above.
1. Install dev requirements with:
   ```
   pip install -r dev.requirements.txt
   ```
1. Make your changes
1. Run before committing
   ```
   black --exclude electricitymapcontrib .
   ```
1. Open a PR!

## When should you pay for api.electricitymap.org instead?

### You want more than just the latest carbon intensity data

This project has exactly one endpoint. If you want historical data or forecasts, buy their API key!

### If you need more accurate data

This project relies on `production` data from open source parsers available at https://github.com/tmrowco/electricitymap-contrib.

While production is a decent lens to guess CO2 emissions, api.electricitymap.org uses [better lenses](https://www.sciencedirect.com/science/article/pii/S2211467X19300549).

### If you want to make a lot of requests

Right now, this project doesn't cache or save data from the data sources in any way. Each request you make refetches and parses data from the original source.

If you're going to make a lot of requests, be a nice citizen and either cache the data or buy an API key.

### If you have money to support a company combating climate change with open source

This project is a thin wrapper over the open source parsers that [Tomorrow](https://tmrow.com) maintains.

Go [buy from them](https://api.electricitymap.org/#pricing) so that they can invest in more and better parsers.
