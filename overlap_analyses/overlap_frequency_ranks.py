import pandas as pd
import matplotlib.pyplot as plt
import os

# File path
file_path = os.path.join(os.path.dirname(__file__), "Overlap_data", "summary.xlsx")

# Read the data
data = pd.read_excel(file_path)

# Extract unique GS and experiments
data = data[data["Experiment"].str.contains("rank", case=False, na=False)]  # Disregard rows with score cutoffs
data["GS"] = data["Experiment"].str.extract(r"GS from ([^\s]+)")
data["Rank cutoff"] = data["Experiment"].str.extract(r"rank≤([0-9\.]+)").astype(float)
data["Experiment Type"] = data["Experiment"].str.extract(r"targets from (top24|random24|bottom24 filter|bottom24 unfilter)")

# Update the list of unique GS and experiment types
gs_names = data["GS"].dropna().unique()
custom_order = ["top24", "random24", "bottom24 filter"]  # Removed "bottom24 unfilter"

# Map custom titles for the graphs
titles_map = {
    "table2": "Gold standard from Table 2",
    "uniprot": "Gold standard from UniProt",
    "genecard": "Gold standard from GeneCards"
}

# Map experiment types to full legend labels
legend_labels = {
    "top24": "targets from top 24 predictions",
    "random24": "targets from random 24 predictions",
    "bottom24 filter": "targets from bottom 24 predictions (filtered)"
}

# Plot line graphs without binning
fig, axes = plt.subplots(1, len(gs_names), figsize=(18, 6), sharey=False)

for i, gs in enumerate(gs_names):
    ax = axes[i]
    gs_data = data[data["GS"] == gs]  # Filter data by gold standard
    max_y = 0  # Initialize max value for y-axis
    for exp in custom_order:
        exp_data = gs_data[gs_data["Experiment Type"] == exp]  # Filter by experiment type
        overlap_data = exp_data[["Rank cutoff", "Overlap (frequency)"]].dropna()
        if not overlap_data.empty:
            # Save overlap_data to a file
            overlap_data.to_excel(f"overlap_data_{gs}_{exp}.xlsx", index=False)
            x_values = overlap_data["Rank cutoff"].tolist()
            y_values = overlap_data["Overlap (frequency)"].tolist()
            max_y = max(max_y, max(y_values))  # Update max_y
            ax.plot(x_values, y_values, marker="o", label=legend_labels[exp])  # Line graph with markers
    ax.set_xlabel("Rank cutoff", fontsize=24, fontfamily="Arial")
    ax.tick_params(axis='x', labelsize=24, labelrotation=0)
    ax.tick_params(axis='y', labelsize=24, labelrotation=0)
    for label in ax.get_xticklabels():
        label.set_fontname("Arial")
    for label in ax.get_yticklabels():
        label.set_fontname("Arial")
    if i == 0:
        ax.set_ylabel("Overlap percentage %", fontsize=24, fontfamily="Arial")
        # Add label to top left corner of the left-most graph
        ax.text(-0.1, 1.05, "B", transform=ax.transAxes, fontsize=24, fontweight="bold", va="top", ha="left", fontfamily="Arial")

plt.tight_layout()

# Save the line graph
plt.savefig("overlap_line_graphs_direct_fixed.png", bbox_inches="tight")
# plt.show()
