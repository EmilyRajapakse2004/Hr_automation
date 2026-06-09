from app.agents.leave_agent import LeaveAgent
from app.agents.scheduling_agent import SchedulingAgent
from app.agents.compliance_agent import ComplianceAgent
from app.agents.clarification_agent import ClarificationAgent


leave_agent = LeaveAgent()
scheduling_agent = SchedulingAgent()
compliance_agent = ComplianceAgent()
clarification_agent = ClarificationAgent()


def route_agent(intent: str):

    if intent == "leave":
        return leave_agent

    elif intent == "scheduling":
        return scheduling_agent

    elif intent == "compliance":
        return compliance_agent

    return clarification_agent