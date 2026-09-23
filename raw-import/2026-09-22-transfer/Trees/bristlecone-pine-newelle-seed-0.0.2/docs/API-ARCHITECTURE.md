# Bristlecone API Architecture

Newelle connects to Bristlecone through Hermes's OpenAI-compatible API.

```text
Newelle desktop interface
        |
        | OpenAI-compatible HTTPS-style request over local HTTP
        | http://127.0.0.1:8643/v1/
        | Authorization: Bearer <generated key>
        v
Hermes profile: bristlecone
        |
        | identity, memory, skills, tools, workspace
        v
Configured model provider
        |
        v
Ollama or another approved inference service
```

The API binds only to `127.0.0.1`. It is not intended for remote access.

The initial integration makes Newelle a front-end for Bristlecone. It does not yet expose Newelle's private GUI API or all Newelle tools to Hermes.
