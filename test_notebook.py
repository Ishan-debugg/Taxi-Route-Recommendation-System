import json
import traceback
import sys

notebook_path = "notebooks/Taxi_Route_Recommendation_System_RealData (2).ipynb"

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Mock google.colab to avoid import errors during test execution
class MockFiles:
    def upload(self):
        return {}

class MockOutput:
    def enable_custom_widget_manager(self):
        pass

sys.modules['google.colab'] = sys.modules[__name__]
files = MockFiles()
output = MockOutput()

namespace = {
    'files': files,
    'output': output,
}

print("Starting notebook execution test...")

has_error = False

for idx, cell in enumerate(nb["cells"]):
    cell_type = cell.get("cell_type", "")
    if cell_type == "code":
        source = "".join(cell.get("source", []))
        
        # Skip magic commands
        source_clean = "\n".join([line for line in source.split("\n") if not line.strip().startswith("!") and not line.strip().startswith("%")])
        
        # Replace local load if needed
        if "pd.read_csv('taxi_route_dataset_sample.csv')" in source_clean:
            source_clean = source_clean.replace("pd.read_csv('taxi_route_dataset_sample.csv')", "pd.read_csv('data/taxi_route_dataset_sample.csv')")
            
        print(f"Executing Cell {idx}...")
        try:
            exec(source_clean, namespace)
        except Exception as e:
            print(f"Error in Cell {idx}: {type(e).__name__}: {e}")
            traceback.print_exc()
            has_error = True
            break

if not has_error:
    print("Notebook executed successfully from start to finish!")
else:
    print("Notebook execution failed.")
