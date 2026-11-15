import unittest

from pyspark.sql import functions as F

from batch.bronze_to_silver import clean_text_udf
from batch.common import athlete_bio, average_stats, joined_results, spark_session
from streaming.streaming_pipeline import EVENT_SCHEMA


class OlympicTransformsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = spark_session("Olympic transform tests")

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_non_numeric_or_missing_measurements_are_excluded(self):
        bio = self.spark.createDataFrame(
            [
                ("1", "Female", "170", "60"), ("2", "Female", " 190 ", "80"),
                ("2", "Female", "190", "80"), ("3", "Female", "", "100"),
                ("4", "Female", "170", "heavy"), ("5", "Female", "NaN", "100"),
                ("6", "Female", "170", "Infinity"), ("7", "Female", None, "50"),
            ],
            "athlete_id string, sex string, height string, weight string",
        )
        events = self.spark.createDataFrame(
            [("1", "Swimming ", None, "usa"), ("2", "Swimming", " N/A ", "USA"),
             ("3", "Swimming", None, "USA"), ("4", "Swimming", None, "USA"),
             ("5", "Swimming", None, "USA"), ("6", "Swimming", None, "USA"),
             ("7", "Swimming", None, "USA"), ("1", "Swimming", "Gold", "USA")],
            "athlete_id string, sport string, medal string, country_noc string",
        )
        rows = {r.medal: r for r in average_stats(joined_results(events, athlete_bio(bio))).collect()}
        self.assertEqual(set(rows), {"No medal", "Gold"})
        self.assertEqual((rows["No medal"].avg_height, rows["No medal"].avg_weight), (180.0, 70.0))
        self.assertEqual((rows["Gold"].avg_height, rows["Gold"].avg_weight), (170.0, 60.0))

    def test_text_udf_preserves_spaces_punctuation_and_accents(self):
        source = self.spark.createDataFrame([("  Pétanque\u200b\t—  Women’s  ",), (None,)], "value string")
        self.assertEqual(
            {row.value for row in source.select(clean_text_udf("value").alias("value")).collect()},
            {"Pétanque — Women’s", None},
        )

    def test_json_schema_unpacks_one_column_per_event_field(self):
        source = self.spark.createDataFrame(
            [('{"athlete_id":42,"country_noc":"UKR","isTeamSport":false,"medal":null}',)],
            ["value"],
        )
        parsed = source.select(F.from_json("value", EVENT_SCHEMA).alias("record")).select("record.*")
        row = parsed.first()
        self.assertEqual(len(parsed.columns), 11)
        self.assertEqual((row.athlete_id, row.country_noc, row.isTeamSport, row.medal), ("42", "UKR", "false", None))
