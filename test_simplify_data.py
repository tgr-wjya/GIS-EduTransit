# test_simplify_data.py
import json
import os
import unittest


class TestSimplifyData(unittest.TestCase):
    def test_simplified_geojson_exists_and_valid(self):
        output_path = "data_ready/Kecamatan_ML_Simplified.geojson"
        self.assertTrue(os.path.exists(output_path), "File Kecamatan_ML_Simplified.geojson harus ada")
        
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        self.assertLess(file_size_mb, 1.2, f"Ukuran file harus di bawah 1.2 MB, terdeteksi {file_size_mb:.2f} MB")
        
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.assertEqual(data["type"], "FeatureCollection")
        self.assertGreater(len(data["features"]), 200)
        
        first_props = data["features"][0]["properties"]
        required_keys = ["KODE_KEC", "KECAMATAN", "KAB_KOTA", "dist_ind", "camp_dens", "toll_pct", "sma_grad", "area_km2", "Pred_Reko"]
        for key in required_keys:
            self.assertIn(key, first_props, f"Properti '{key}' tidak ditemukan pada fitur GeoJSON")

    def test_simplified_geojson_latency(self):
        import time
        output_path = "data_ready/Kecamatan_ML_Simplified.geojson"
        start_time = time.perf_counter()
        with open(output_path, "r", encoding="utf-8") as f:
            json.load(f)
        duration_ms = (time.perf_counter() - start_time) * 1000
        self.assertLess(duration_ms, 50.0, f"Latensi pembacaan harus di bawah 50 ms, terdeteksi {duration_ms:.2f} ms")

    def test_get_color_reko(self):
        from simplify_data import get_color_reko
        self.assertEqual(get_color_reko(2), "#10B981")
        self.assertEqual(get_color_reko(1), "#F59E0B")
        self.assertEqual(get_color_reko(0), "#EF4444")
        self.assertEqual(get_color_reko(999), "#EF4444")

if __name__ == "__main__":
    unittest.main()
