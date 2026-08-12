import unittest

from job_scraper.services.closed_detector import has_closed_content


class TestClosedDetector(unittest.TestCase):
    def test_general_marker_indonesian(self):
        self.assertTrue(has_closed_content("<html><body>Lowongan telah ditutup oleh perusahaan</body></html>"))

    def test_general_marker_english(self):
        self.assertTrue(has_closed_content("This job is no longer accepting applications"))

    def test_platform_marker_jobstreet(self):
        self.assertTrue(has_closed_content('data-automation="jobClosedHeader"', "jobstreet"))

    def test_open_job_not_detected(self):
        self.assertFalse(has_closed_content("Software Engineer - Jakarta - Full-time - Apply now"))

    def test_case_insensitive(self):
        self.assertTrue(has_closed_content("This position is NO LONGER AVAILABLE"))


if __name__ == "__main__":
    unittest.main()