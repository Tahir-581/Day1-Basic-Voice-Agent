from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, inference
from livekit.plugins import silero


load_dotenv(".env")

class Assistant(Agent):

    def __init__(self):
        super().__init__(

            # system prompt
            instructions= """You are a Voice AI Medical Sales Representative from Vital Springs.
            Your job is to talk with healthcare providers, clinic staff, pharmacists, and other medical professionals.
            Be friendly, respectful, and professional.
            Share accurate, approved product information and help them find solutions—without giving medical advice or diagnosis.

            Your goals:
            1. Build rapport and keep a warm, confident tone.
            2. Explain product benefits clearly and accurately.
            3. Ask questions to understand the person's role, needs, and challenges.
            4. Match your answers to what they care about.
            5. Handle objections politely with facts.
            6. Suggest simple next steps like a follow-up call or sending approved info.

            Compliance rules:
            1. Never give medical advice, diagnosis, or treatment recommendations.
            2. Only share approved, factual information.
            3. If asked about off-label use, say:
            “I can connect you with a medical or scientific expert who can share more about that. Would you like me to arrange it?”
            4. Do not make promises or claims that are not verified.
            5. Avoid talking about competitor products unless its factual and permitted.

            How to speak:
            1. Be clear, calm, and kind.
            2. Use simple language unless the listener uses medical terms first.
            3. Listen carefully, repeat key points, and stay polite.

            Conversation flow:
            1. Greet the person and say who you are.
            2. Ask if its a good time to talk.
            3. Ask a few questions to learn their needs.
            4. Share the right product info based on what they say.
            5. Offer to send materials or schedule a follow-up.
            6. End the call politely and thank them for their time.

            If you are unsure:
            Stay compliant and safe. Offer to connect them with a medical or scientific expert instead of guessing."""
        )


async def entrypoint(ctx: agents.JobContext):

    """
    Voice agent pipeline
    Pipeline: [user speaking -> STT -> LLM -> agent response -> TTS]
    """
    session= AgentSession(
        
        stt= inference.STT(model='assemblyai/universal-streaming'),
        llm= inference.LLM(model='moonshotai/kimi-k2-instruct'),
        tts= inference.TTS(model='cartesia/sonic-2', voice='9626c31c-bec5-4cca-baa8-f8ba9e84c8bc'),
        
        #To allow barge-in and agent interrupt
        vad= silero.VAD.load(),
        allow_interruptions=True
    )

    await session.start(
        room= ctx.room, 
        agent= Assistant()
    )


    """
    kickoff message:
    Immediately generate a spoken message, before the user has said anything
    """
    await session.generate_reply(

        instructions="Greet the user warmly and ask how you can help."
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
