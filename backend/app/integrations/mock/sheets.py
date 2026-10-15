from pathlib import Path
import pandas as pd
from app.config import settings


class MockSheets:
    def get_pipeline(self, names: list[str]) -> list[dict]:
        df = pd.read_csv(Path(settings.data_dir) / "sample_sales_data/sales_pipeline.csv")
        keys = [n.lower() for n in names if n]
        rows = []
        for i, r in df.iterrows():
            cust = str(r["Customer"]).lower()
            if any(k in cust or cust in k for k in keys):
                rows.append({"row": int(i) + 2, **r.to_dict()})
        return rows
