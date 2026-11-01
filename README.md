# Basic Voice Agent (LiveKit Agents)

A real-time conversational voice agent built on [LiveKit Agents](https://docs.livekit.io/agents/).
It plays a compliance-aware medical sales representative for a fictional company ("Acme Health"):
it greets the caller, asks about their needs, shares product information, and refuses to give medical
advice or discuss off-label use.

## Pipeline

```
caller audio ──► STT (AssemblyAI universal-streaming)
              ──► LLM (Moonshot Kimi K2 Instruct)
              ──► TTS (Cartesia Sonic-2) ──► caller
                  ▲
   Silero VAD ────┘  barge-in: the caller can interrupt the agent mid-sentence
```

All three models are called through LiveKit Inference (`livekit.agents.inference`), so the only
credentials needed are your LiveKit project keys.

## Features

- Streaming STT → LLM → TTS voice loop inside a LiveKit room
- Barge-in / interruptions via Silero VAD and `allow_interruptions=True`
- Proactive greeting before the user speaks (`session.generate_reply`)
- System prompt with explicit compliance rules (no diagnosis, no off-label claims)
- Swap any model by changing one string in `AgentSession(...)`

## Run locally

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
cp .env.example .env      # fill in your LiveKit Cloud project URL / key / secret
uv sync
uv run python livekit_basic_agent.py dev
```

Then join the room from the [LiveKit Agents Playground](https://agents-playground.livekit.io/).

## Project structure

```
├── livekit_basic_agent.py   # agent prompt, AgentSession (STT/LLM/TTS/VAD), worker entrypoint
├── main.py                  # placeholder script
├── docs/barge-in-notes.md   # notes on how LiveKit's interruption handling works
├── pyproject.toml / uv.lock
└── .env.example
```

## License

MIT
