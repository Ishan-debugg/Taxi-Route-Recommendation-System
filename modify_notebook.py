import json

notebook_path = "notebooks/Taxi_Route_Recommendation_System_RealData (2).ipynb"

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# 1. Modify Cell 2 (index 2): Safe device and version prints
cell_2_source = [
    "import torch\n",
    "\n",
    "print(\"PyTorch Version:\", torch.__version__)\n",
    "print(\"CUDA Available:\", torch.cuda.is_available())\n",
    "if torch.cuda.is_available():\n",
    "    print(\"GPU Device:\", torch.cuda.get_device_name(0))\n",
    "else:\n",
    "    print(\"Running on CPU\")\n"
]
nb["cells"][2]["source"] = cell_2_source

# 2. Extract and split Cell 5 (imports & installer)
# We will create a new installation cell and place it at index 5.
# Then the GATConv imports cell will be at index 6.

# Let's check what is in Cell 5 currently
current_cell_5 = nb["cells"][5]
print("Current cell 5 metadata id:", current_cell_5.get("id"))

# Let's create the new installation cell
installer_cell = {
    "cell_type": "code",
    "execution_count": None,
    "id": "install-pyg-dynamic",
    "metadata": {},
    "outputs": [],
    "source": [
        "# Install torch-geometric dynamically if not already present\n",
        "try:\n",
        "    import torch_geometric\n",
        "except ImportError:\n",
        "    print(\"Installing torch-geometric...\")\n",
        "    !pip install -q torch-geometric\n"
    ]
}

# The imports cell should now contain only imports
imports_cell_source = [
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "import time\n",
    "from collections import defaultdict\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "import torch\n",
    "import torch.nn as nn\n",
    "import torch.nn.functional as F\n",
    "from torch_geometric.nn import GATConv\n",
    "\n",
    "from scipy.spatial import cKDTree\n",
    "from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score\n",
    "\n",
    "import folium\n",
    "from folium.plugins import HeatMap\n",
    "\n",
    "import lightgbm as lgb\n",
    "import shap\n",
    "import optuna\n",
    "optuna.logging.set_verbosity(optuna.logging.WARNING)\n",
    "\n",
    "import ipywidgets as widgets\n",
    "from IPython.display import display, clear_output\n",
    "\n",
    "SEED = 42\n",
    "np.random.seed(SEED)\n",
    "torch.manual_seed(SEED)\n",
    "\n",
    "DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')\n",
    "print(f\"Using device: {DEVICE}\")\n"
]

# Insert the installer cell at index 5, and set imports cell source at the next index
nb["cells"].insert(5, installer_cell)
# Note: Since we inserted a cell, the old Cell 5 is now Cell 6.
nb["cells"][6]["source"] = imports_cell_source

# Save the updated notebook
with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print("Notebook updated successfully with safe Cell 2 and separate installer cell.")
