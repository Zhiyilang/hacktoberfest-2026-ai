#!/usr/bin/env python3
"""GardenPlanner AI — evaluation suite (stdlib unittest, no network).

Covers:
- hemisphere flip maths (_adjust_month) and its inverse property
- build_plan determinism, unknown-city fallback, space/level filters
- plant-DB integrity (schema, month range, enum values)
- every month has a task list
- render() output contract
- Ollama enhancement path: absent binary -> passthrough (monkeypatched)
- CLI end-to-end via real subprocess, incl. invalid-month exit code
"""
from __future__ import annotations

import datetime as _dt
import io
import os
import subprocess
import sys
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import main as GP  # noqa: E402

PY = sys.executable


class TestHemisphere(unittest.TestCase):
    def test_northern_identity(self):
        for m in range(1, 13):
            self.assertEqual(GP._adjust_month(m, False), m)

    def test_southern_is_plus_six(self):
        for m in range(1, 13):
            self.assertEqual(GP._adjust_month(m, True), ((m + 5) % 12) + 1)

    def test_southern_roundtrip(self):
        for m in range(1, 13):
            once = GP._adjust_month(m, True)
            self.assertEqual(GP._adjust_month(once, True), m)


class TestBuildPlan(unittest.TestCase):
    def test_deterministic(self):
        a = GP.build_plan("Shanghai", 10, "balcony", "easy")
        b = GP.build_plan("Shanghai", 10, "balcony", "easy")
        self.assertEqual(a, b)

    def test_unknown_city_falls_back_to_zone8_northern(self):
        plan = GP.build_plan("Atlantis", 10, "any", "any")
        self.assertEqual(plan["zone"], 8)
        self.assertFalse(plan["southern"])
        self.assertEqual(plan["target_month"], 10)

    def test_city_lookup_case_insensitive(self):
        a = GP.build_plan("  Shanghai ", 10, "any", "any")
        b = GP.build_plan("shanghai", 10, "any", "any")
        self.assertEqual(a["picks"], b["picks"])

    def test_southern_city_flips_season(self):
        # Sydney April == northern October (autumn sowing window)
        syd = GP.build_plan("Sydney", 4, "balcony", "easy")
        sha = GP.build_plan("Shanghai", 10, "balcony", "easy")
        self.assertEqual(syd["target_month"], 10)
        self.assertTrue(syd["southern"])
        self.assertEqual([p["name"] for p in syd["picks"]],
                         [p["name"] for p in sha["picks"]])

    def test_balcony_includes_indoor(self):
        # 豆芽 is space=indoor; balcony queries must still surface it
        plan = GP.build_plan("Shanghai", 1, "balcony", "any")
        self.assertIn("豆芽", [p["name"] for p in plan["picks"]])

    def test_garden_excludes_balcony_only(self):
        plan = GP.build_plan("Shanghai", 10, "garden", "any")
        names = [p["name"] for p in plan["picks"]]
        self.assertNotIn("生菜", names)      # balcony-only
        self.assertIn("豌豆", names)         # garden, sows in month 10

    def test_level_easy_excludes_medium_hard(self):
        plan = GP.build_plan("Shanghai", 3, "any", "easy")
        for p in plan["picks"]:
            self.assertEqual(p["level"], "easy")
        names = [p["name"] for p in plan["picks"]]
        self.assertNotIn("番茄", names)      # medium
        self.assertNotIn("南瓜", names)      # medium

    def test_october_balcony_easy_matches_readme_example(self):
        # Locks the README sample output (5 picks) against regressions.
        plan = GP.build_plan("Shanghai", 10, "balcony", "easy")
        self.assertEqual([p["name"] for p in plan["picks"]],
                         ["生菜", "菠菜", "大蒜", "香菜", "豆芽"])

    def test_month_zero_produces_empty_picks_not_crash(self):
        # month 0 has no sowing window; must degrade gracefully
        plan = GP.build_plan("Shanghai", 0, "any", "any")
        self.assertEqual(plan["picks"], [])

    def test_season_label_present(self):
        plan = GP.build_plan("Shanghai", 10, "any", "any")
        self.assertEqual(plan["season"], "中秋")


class TestDataIntegrity(unittest.TestCase):
    def test_every_plant_has_full_schema(self):
        for p in GP.PLANTS:
            for key in ("name", "sow", "space", "level", "friends",
                        "foes", "note", "pests"):
                self.assertIn(key, p, f"{p.get('name')} missing {key}")

    def test_sow_months_within_1_12(self):
        for p in GP.PLANTS:
            for m in p["sow"]:
                self.assertTrue(1 <= m <= 12, f"{p['name']} sow {m} out of range")

    def test_space_and_level_enums(self):
        for p in GP.PLANTS:
            self.assertIn(p["space"], ("balcony", "garden", "indoor"))
            self.assertIn(p["level"], ("easy", "medium", "hard"))

    def test_plant_names_unique(self):
        names = [p["name"] for p in GP.PLANTS]
        self.assertEqual(len(names), len(set(names)))

    def test_every_month_has_tasks(self):
        for m in range(1, 13):
            self.assertTrue(GP.TASKS.get(m), f"month {m} has no task list")

    def test_cities_have_valid_zones(self):
        for city, (zone, southern) in GP.CITIES.items():
            self.assertTrue(1 <= zone <= 12, f"{city} zone {zone}")
            self.assertIsInstance(southern, bool)


class TestRender(unittest.TestCase):
    def test_render_contains_contract_sections(self):
        text = GP.render(GP.build_plan("Shanghai", 10, "balcony", "easy"))
        self.assertIn("Shanghai", text)
        self.assertIn("当月任务清单", text)
        self.assertIn("搭档(伴生)", text)
        self.assertIn("相克(避免相邻)", text)
        self.assertIn("病虫害", text)

    def test_render_empty_picks_message(self):
        text = GP.render(GP.build_plan("Shanghai", 0, "any", "any"))
        self.assertIn("没有特别匹配", text)


class TestOllamaEnhancement(unittest.TestCase):
    def test_absent_binary_passthrough(self):
        with mock.patch("main.shutil.which", return_value=None):
            out = GP.maybe_enhance_with_model("PLAN", "llama3.2")
        self.assertEqual(out, "PLAN")

    def test_present_binary_failure_falls_back(self):
        # binary exists but the model call blows up -> original text survives
        with mock.patch("main.shutil.which", return_value="/usr/bin/ollama"), \
             mock.patch("main.subprocess.run",
                        side_effect=OSError("boom")):
            out = GP.maybe_enhance_with_model("PLAN", "llama3.2")
        self.assertEqual(out, "PLAN")

    def test_present_binary_success_uses_output(self):
        ok = subprocess.CompletedProcess(args=[], returncode=0,
                                         stdout="  friendly text  \n", stderr="")
        with mock.patch("main.shutil.which", return_value="/usr/bin/ollama"), \
             mock.patch("main.subprocess.run", return_value=ok):
            out = GP.maybe_enhance_with_model("PLAN", "llama3.2")
        self.assertEqual(out, "friendly text")

    def test_present_binary_empty_output_falls_back(self):
        ok = subprocess.CompletedProcess(args=[], returncode=0,
                                         stdout="   \n", stderr="")
        with mock.patch("main.shutil.which", return_value="/usr/bin/ollama"), \
             mock.patch("main.subprocess.run", return_value=ok):
            out = GP.maybe_enhance_with_model("PLAN", "llama3.2")
        self.assertEqual(out, "PLAN")


class TestCLI(unittest.TestCase):
    def test_cli_runs_real_subprocess(self):
        proc = subprocess.run(
            [PY, os.path.join(HERE, "main.py"),
             "--city", "Shanghai", "--month", "10",
             "--space", "balcony", "--level", "easy"],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Shanghai", proc.stdout)
        self.assertIn("生菜", proc.stdout)
        self.assertIn("当月任务清单", proc.stdout)

    def test_cli_invalid_month_exits_2(self):
        proc = subprocess.run(
            [PY, os.path.join(HERE, "main.py"), "--month", "13"],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("月份", proc.stderr)

    def test_cli_unknown_city_still_succeeds(self):
        proc = subprocess.run(
            [PY, os.path.join(HERE, "main.py"),
             "--city", "Atlantis", "--month", "5"],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Atlantis", proc.stdout)

    def test_cli_southern_flip(self):
        proc = subprocess.run(
            [PY, os.path.join(HERE, "main.py"),
             "--city", "Sydney", "--month", "4", "--space", "balcony"],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("南半球", proc.stdout)
        self.assertIn("第 10 月", proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
