import json

notebook_path = "notebooks/Taxi_Route_Recommendation_System_RealData (2).ipynb"

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

print("Checking cells with errors...")
found_error = False
for idx, cell in enumerate(nb["cells"]):
    cell_type = cell.get("cell_type", "")
    if cell_type == "code":
        outputs = cell.get("outputs", [])
        for out in outputs:
            if out.get("output_type") == "error":
                found_error = True
                print(f"\n--- Error in Cell {idx} ---")
                print(f"Error Name: {out.get('ename')}")
                print(f"Error Value: {out.get('evalue')}")
                print("Traceback (last 10 lines):")
                tb = out.get("traceback", [])
                print("\n".join(tb[-10:]))

if not found_error:
    print("No errors stored in cell outputs.")
