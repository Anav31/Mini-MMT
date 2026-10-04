import json
import os
from datetime import datetime


class HealingLogger:

    FILE_PATH = (
        "healing_logs/"
        "healing_history.json"
    )

    def load_history(self):

        if not os.path.exists(
            self.FILE_PATH
        ):

            return []

        with open(
            self.FILE_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def save_cycle(
        self,
        cycle_data
    ):

        history = (
            self.load_history()
        )

        history.append(
            cycle_data
        )

        with open(
            self.FILE_PATH,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(

                history,

                file,

                indent=4
            )

    def generate_cycle_id(self):

        history = (
            self.load_history()
        )

        return (
            len(history)
            + 1
        )

    def current_timestamp(self):

        return datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"
        )