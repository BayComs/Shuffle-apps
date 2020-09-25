import asyncio
import time
import json

from walkoff_app_sdk.app_base import AppBase

class TheHiveTools(AppBase):
    """
    An example of a Walkoff App.
    Inherit from the AppBase class to have Redis, logging, and console logging set up behind the scenes.
    """
    __version__ = "1.0.0"
    app_name = "TheHive Tools"  # this needs to match "name" in api.yaml for WALKOFF to work

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    async def compute_similar_case(self, field_type, thehive_input):
        try:
            data = json.loads(thehive_input)
        except json.decoder.JSONDecodeError as e:
            print("Parse error: %s" % e) 
            return thehive_input
        if field_type.lower() == "alert":
            artifactCount = len(data["artifacts"])
            data["hasSimilarCase"] = True if len(data["similarCases"]) else False
            for index, case in enumerate(data["similarCases"]):
                data["similarCases"][index]["similarPercentage"] = round((artifactCount / case["similarArtifactCount"]) * 100,2)
        elif field_type.lower() == "case":
            pass
        return json.dumps(data)


if __name__ == "__main__":
    asyncio.run(TheHiveTools.run(), debug=True)