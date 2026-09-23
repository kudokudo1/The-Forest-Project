# Bristlecone Pine Newelle Seed 0.0.2

This package plants Bristlecone Pine as an isolated Hermes profile and exposes him on a localhost OpenAI-compatible API that Newelle can use.

## Connection

- Hermes profile: `bristlecone`
- API base URL: `http://127.0.0.1:8643/v1`
- Newelle endpoint: `http://127.0.0.1:8643/v1/`
- Advertised model: `bristlecone`
- Bind address: localhost only
- API key: generated during planting
- CORS: disabled

The package contains no API key. A random key is generated on your computer and written to Bristlecone's private profile `.env` and to a private Newelle connection card.

## What this package does

- Creates or updates a separate Hermes profile named `bristlecone`
- Clones the default profile's model/provider configuration for a faster bootstrap
- Preserves Bristlecone's separate memory, sessions, and state
- Installs Bristlecone's identity and workspace rules
- Configures the Hermes API server on `127.0.0.1:8643`
- Generates a private Bearer API key
- Creates start, stop, status, test, and connection helpers
- Produces a Newelle connection card with the actual local key

## What it does not do

- It does not modify Newelle's internal settings automatically
- It does not expose the API outside the Cherry-AI qube
- It does not enable CORS
- It does not grant unrestricted desktop or cross-qube access
- It does not create a full Newelle tool bridge
- It does not overwrite canonical Forest files

## Planting

Extract the ZIP, open a terminal inside the extracted folder, and run:

```bash
chmod +x plant-bristlecone.sh
./plant-bristlecone.sh
```

Then start Bristlecone's API:

```bash
~/The-Forest/bristlecone/bin/start-bristlecone-api.sh
```

Print the Newelle settings:

```bash
~/The-Forest/bristlecone/bin/show-newelle-connection.sh
```

## Newelle settings

In Newelle, select the OpenAI API provider and enter the values printed by the connection helper.

The expected values are:

- API Endpoint: `http://127.0.0.1:8643/v1/`
- OpenAI Model: `bristlecone`
- API Key: generated locally during planting

## Verification

```bash
~/The-Forest/bristlecone/bin/verify-bristlecone.sh
~/The-Forest/bristlecone/bin/test-bristlecone-api.sh
```

## Stop or disconnect

```bash
~/The-Forest/bristlecone/bin/stop-bristlecone-api.sh
```

Stopping the API is the initial emergency disconnect between Newelle and Bristlecone.
