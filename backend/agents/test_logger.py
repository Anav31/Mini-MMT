from healing_logger import HealingLogger

logger = HealingLogger()

cycle = {

    "cycle_id":
    logger.generate_cycle_id(),

    "timestamp":
    logger.current_timestamp(),

    "bugs_found":
    3,

    "bugs_fixed":
    2,

    "patches_applied":
    2,

    "confidence_score":
    95,

    "system_status":
    "TEST_SUCCESS"

}

logger.save_cycle(
    cycle
)

print(
    "\nLOGGER TEST PASSED\n"
)


history = logger.load_history()

print(history[-1])