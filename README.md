# CarbonIntensity API

API server for pseudo-realtime production carbon intensity data in gCO2eq/kWh for any zone supported by https://github.com/tmrowco/electricitymap-contrib.

```bash
curl 'http://localhost:5000/carbon-intensity/latest?zone=IN-KA'
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
