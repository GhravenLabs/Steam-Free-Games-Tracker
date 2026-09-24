import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import steam_free


class BrowserOutputTests(unittest.TestCase):
    def run_tracker(self, directory, args, games):
        output = Path(directory) / "games #1 % report.html"
        with (
            patch.object(steam_free, "OUT", str(output)),
            patch.object(steam_free, "collect", return_value=games),
            patch.object(steam_free.webbrowser, "open") as browser,
            contextlib.redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(steam_free.main(args), 0)
        self.assertIn("Free Steam Games", output.read_text(encoding="utf-8"))
        return output, browser

    def test_browser_uses_escaped_file_uri(self):
        with tempfile.TemporaryDirectory(prefix="tracker # ") as directory:
            output, browser = self.run_tracker(directory, [], [])
            browser.assert_called_once_with(output.resolve().as_uri())

    def test_no_open_and_empty_scheduled_run_still_write_page(self):
        with tempfile.TemporaryDirectory() as directory:
            for args in (["--no-open"], ["--open-if-any"]):
                with self.subTest(args=args):
                    _, browser = self.run_tracker(directory, args, [])
                    browser.assert_not_called()

    def test_scheduled_run_opens_when_games_exist_unless_no_open(self):
        games = [{"title": "Demo", "worth": "Free", "ends": "Unknown",
                  "url": "https://example.com/game", "img": "", "source": "Fixture"}]
        with tempfile.TemporaryDirectory() as directory:
            output, browser = self.run_tracker(directory, ["--open-if-any"], games)
            browser.assert_called_once_with(output.resolve().as_uri())
            _, browser = self.run_tracker(directory, ["--open-if-any", "--no-open"], games)
            browser.assert_not_called()


if __name__ == "__main__":
    unittest.main()
