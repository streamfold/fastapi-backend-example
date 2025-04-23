# FastAPI - Rotel Demo

This is a demo of the [Rotel Python](https://github.com/streamfold/pyrotel) integration with the [FastAPI](https://fastapi.tiangolo.com/) project. Using the FastAPI instrumentation, it will emit trace spans that can be sent to any compatible tracing vendor. See the _Enabling Rotel_ section below for how to enable Rotel and OpenTelemetry for your own FastAPI project.

This is the backend component
from the fullstack FastAPI [demo template](https://github.com/fastapi/full-stack-fastapi-template).
For full instructions on how to run the FastAPI backend, see the [FastAPI README](/README-FastAPI.md).

## Usage

Copy the `.env.example` to `.env` and set the appropriate environment variables.

This project uses the [uv](https://github.com/astral-sh/uv) project manager, to install dependencies run:

```shell
uv sync
```

Run a server listening on `http://127.0.0.1:10000`: 

```shell
uv run uvicorn app.main:app --host 0.0.0.0 --port "10000" --workers 2
```

Test that the server is running:
```shell
curl http://127.0.0.1:10000/api/v1/utils/health-check/
```

## Enabling Rotel

See the `initialize_tracing` method in [main.py](/app/main.py) for how we enable OpenTelemetry tracing and Rotel to emit traces to [Axiom](https://axiom.co/).

To start the server with Rotel enabled, set the following environment variables before starting the server:
```shell
export AXIOM_API_KEY=xaat-xxxxxxxx
export AXIOM_DATA_SET=my-data-set

uv run uvicorn app.main:app --host 0.0.0.0 --port "10000" --workers 2
```

## Deploying to Render

This project can also be deployed to [Render](https://render.com/) using the provided build and run scripts. Fork this repo and connect it to Render, setting the following script paths in the app config. Set the environment variables as needed in Render's configuration section.

* Build: [render-build.sh](/scripts/render-build.sh)
* Run: [render-start.sh](/scripts/render-start.sh)

## Questions / Support

Do you have questions about this project or want to share your feedback? Join our [Discord server](https://discord.gg/reUqNWTSGC) where we'd be happy to discuss this integration. See you there! 🚀
