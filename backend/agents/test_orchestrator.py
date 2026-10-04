from backend.agents.roar_ai import (
    SelfHealingOrchestrator
)

orchestrator = (
    SelfHealingOrchestrator()
)

report = (
    orchestrator.run()
)

print(
    "\nORCHESTRATOR REPORT\n"
)

print(report)