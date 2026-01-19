#!/usr/bin/env python3
"""
Tests for the Telegram Weather & News Bot
"""

import unittest
from unittest.mock import patch, MagicMock

# Import functions from main module
from main import (
    fetch_meduza_news,
    fetch_weather,
    format_daily_message,
    get_weather_emoji,
    WEATHER_CONDITIONS,
)


class TestWeatherEmoji(unittest.TestCase):
    """Test weather emoji function."""

    def test_clear_sky(self):
        self.assertEqual(get_weather_emoji("clear sky"), "☀️")

    def test_sunny(self):
        self.assertEqual(get_weather_emoji("sunny"), "☀️")

    def test_cloudy(self):
        self.assertEqual(get_weather_emoji("cloudy"), "☁️")

    def test_rain(self):
        self.assertEqual(get_weather_emoji("rain"), "🌧️")

    def test_thunderstorm(self):
        self.assertEqual(get_weather_emoji("thunderstorm"), "⛈️")

    def test_snow(self):
        self.assertEqual(get_weather_emoji("snow"), "❄️")

    def test_mist(self):
        self.assertEqual(get_weather_emoji("mist"), "🌫️")

    def test_default(self):
        self.assertEqual(get_weather_emoji("unknown"), "🌤️")


class TestMeduzaNews(unittest.TestCase):
    """Test Meduza news fetch function."""

    def test_fetch_meduza_news_returns_list(self):
        """Test that fetch_meduza_news returns a list."""
        result = fetch_meduza_news()
        self.assertIsInstance(result, list)

    def test_fetch_meduza_news_returns_10_items(self):
        """Test that fetch_meduza_news returns 10 items."""
        result = fetch_meduza_news()
        self.assertEqual(len(result), 10)

    def test_fetch_meduza_news_item_structure(self):
        """Test that each news item has required fields."""
        result = fetch_meduza_news()
        for item in result:
            self.assertIn("title", item)
            self.assertIn("link", item)
            self.assertIsInstance(item["title"], str)
            self.assertIsInstance(item["link"], str)


class TestWeatherConditions(unittest.TestCase):
    """Test weather conditions mapping."""

    def test_weather_conditions_dict_exists(self):
        """Test that WEATHER_CONDITIONS dict exists and has entries."""
        self.assertIsInstance(WEATHER_CONDITIONS, dict)
        self.assertGreater(len(WEATHER_CONDITIONS), 0)

    def test_clear_sky_mapping(self):
        """Test clear sky condition mapping."""
        self.assertEqual(WEATHER_CONDITIONS.get("clear sky"), "Clear")

    def test_rain_mapping(self):
        """Test rain condition mapping."""
        self.assertEqual(WEATHER_CONDITIONS.get("light rain"), "Light Rain")


class TestFormatDailyMessage(unittest.TestCase):
    """Test daily message formatting."""

    @patch("main.fetch_weather")
    @patch("main.fetch_meduza_news")
    def test_format_message_with_data(self, mock_news, mock_weather):
        """Test message formatting with mock data."""
        mock_weather.return_value = {
            "feels_like": 15,
            "high": 20,
            "low": 10,
            "precipitation": 25,
            "condition": "Clear",
            "emoji": "☀️",
        }
        mock_news.return_value = [
            {"title": "Test headline", "link": "https://example.com"}
        ]

        message = format_daily_message()

        self.assertIn("Weather in Lisbon", message)
        self.assertIn("Feels like: 15°C", message)
        self.assertIn("High: 20°C", message)
        self.assertIn("Low: 10°C", message)
        self.assertIn("Precipitation: 25%", message)
        self.assertIn("Meduza", message)
        self.assertIn("Test headline", message)

    @patch("main.fetch_weather")
    @patch("main.fetch_meduza_news")
    def test_format_message_with_failed_weather(self, mock_news, mock_weather):
        """Test message formatting when weather fails."""
        mock_weather.return_value = None
        mock_news.return_value = [
            {"title": "Test headline", "link": "https://example.com"}
        ]

        message = format_daily_message()

        self.assertIn("Weather data temporarily unavailable", message)

    @patch("main.fetch_weather")
    @patch("main.fetch_meduza_news")
    def test_format_message_with_failed_news(self, mock_news, mock_weather):
        """Test message formatting when news fails."""
        mock_weather.return_value = {
            "feels_like": 15,
            "high": 20,
            "low": 10,
            "precipitation": 25,
            "condition": "Clear",
            "emoji": "☀️",
        }
        mock_news.return_value = None

        message = format_daily_message()

        self.assertIn("News data temporarily unavailable", message)


if __name__ == "__main__":
    unittest.main()
