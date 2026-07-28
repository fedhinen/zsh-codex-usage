import datetime as dt
import importlib.machinery
import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).parents[1] / "bin" / "codex-usage"
LOADER = importlib.machinery.SourceFileLoader("codex_usage", str(MODULE_PATH))
SPEC = importlib.util.spec_from_loader("codex_usage", LOADER)
assert SPEC and SPEC.loader
codex_usage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(codex_usage)


class CodexUsageTests(unittest.TestCase):
    def test_rate_limit_windows_prefers_default_rate_limits(self):
        result = {
            "rateLimits": {
                "primary": {"usedPercent": 37.5, "resetsAt": 0, "windowDurationMins": 300},
                "secondary": {"usedPercent": 11, "resetsAt": 3600, "windowDurationMins": 10080},
            },
            "rateLimitsByLimitId": {
                "other": {"primary": {"usedPercent": 99, "windowDurationMins": 300}}
            },
        }

        windows = codex_usage.rate_limit_windows(result)

        self.assertEqual(windows["primary"]["remainingPercent"], 62)
        self.assertEqual(windows["secondary"]["remainingPercent"], 89)
        self.assertEqual(windows["primary"]["windowMinutes"], 300)

    def test_failed_refresh_does_not_make_cache_fresh(self):
        previous = {
            "schemaVersion": 2,
            "loggedIn": True,
            "remainingPercent": 62,
            "lastSuccessfulRefreshAt": (dt.datetime.now().astimezone() - dt.timedelta(hours=1)).isoformat(),
            "updatedAt": (dt.datetime.now().astimezone() - dt.timedelta(hours=1)).isoformat(),
            "stale": False,
        }

        failed = codex_usage.error_payload(previous, "network error", True)

        self.assertTrue(failed["stale"])
        self.assertFalse(codex_usage.cache_is_fresh(failed))
        self.assertFalse(codex_usage.retry_is_due(failed))

    def test_prompt_can_show_both_windows(self):
        data = {
            "loggedIn": True,
            "stale": False,
            "windows": {
                "primary": {"remainingPercent": 62, "resetsAt": None},
                "secondary": {"remainingPercent": 89, "resetsAt": None},
            },
        }

        self.assertEqual(codex_usage.prompt_text(data, "both"), "󰚩 P: 62% · S: 89%")

    def test_future_cache_timestamp_is_not_fresh(self):
        data = {
            "stale": False,
            "lastSuccessfulRefreshAt": (dt.datetime.now().astimezone() + dt.timedelta(minutes=5)).isoformat(),
        }

        self.assertFalse(codex_usage.cache_is_fresh(data))


if __name__ == "__main__":
    unittest.main()
