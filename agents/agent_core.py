"""Agent core with simple A2A messaging (in-process) and stubs for LangGraph/AutoGen integration.
- Agent: has inbox, memory (vector stub), and simple handle() method which can call an LLM or local reasoner.
- AgentManager: routes messages and simulates runtime. Replace with Pub/Sub or a broker in production.
"""
import queue, time, json
from agents.memory_vector_stub import VectorMemory

class Agent:
    def __init__(self, name, memory_index='default'):
        self.name = name
        self.inbox = queue.Queue()
        self.memory = VectorMemory(memory_index)  # stub to represent vector DB backed memory

    def send(self, target, message):
        # Put a message tuple to be routed by AgentManager
        self.inbox.put({'to': target, 'from': self.name, 'message': message})

    def handle(self, envelope):
        # Basic handler: store payload into memory and optionally produce a reasoning output
        msg = envelope.get('message', {})
        payload = msg.get('payload')
        # Upsert into vector memory as a text embedding stub
        self.memory.upsert(f"{self.name}-{int(time.time()*1000)}", {'text': str(payload)})
        # Simple reasoning: if tariff_summary, produce a note
        if msg.get('type') == 'tariff_summary':
            total = sum(item.get('estimated_additional_cost_usd', 0) for item in payload)
            return {'type':'reasoning_note','from': self.name, 'payload': f'Total estimated additional cost USD {total:,.2f}'}
        return None

class AgentManager:
    def __init__(self):
        self.agents = {}

    def register(self, agent):
        self.agents[agent.name] = agent

    def route_all(self, max_cycles=10):
        # Drain all agent inboxes and route messages to recipients
        for _ in range(max_cycles):
            progressed = False
            for agent in list(self.agents.values()):
                while not agent.inbox.empty():
                    env = agent.inbox.get_nowait()
                    to = env['to']
                    recipient = self.agents.get(to)
                    if recipient:
                        resp = recipient.handle(env)
                        progressed = True
                        if resp and 'from' in resp:
                            sender = self.agents.get(resp['from'])
                            if sender:
                                sender.handle({'message': resp})
                    else:
                        print(f"No recipient {to} registered.")
            if not progressed:
                break
