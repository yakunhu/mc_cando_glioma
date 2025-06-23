import pandas as pd
import matplotlib.pyplot as plt
import os

# File path
file_path = os.path.join(os.path.dirname(__file__), "Overlap_data", "summary.xlsx")

# Read the data
data = pd.read_excel(file_path)

# Extract only rows with rank information
rank_data = data[data["Experiment"].str.contains("rank", case=False, na=False)]
rank_data["GS"] = rank_data["Experiment"].str.extract(r"GS from ([^\s]+)")
rank_data["Rank cutoff"] = rank_data["Experiment"].str.extract(r"rank≤([0-9\.]+)").astype(float)
rank_data["Experiment Type"] = rank_data["Experiment"].str.extract(r"targets from (top24|random24|bottom24 filter)")

# Update the list of unique GS and experiment types
gs_names = rank_data["GS"].dropna().unique()
custom_order = ["top24", "random24", "bottom24 filter"]

# Create a dictionary to store the JC values for output
output_data = []

# Plot Jaccard Coefficient (JC) vs Rank cutoff
fig, axes = plt.subplots(1, len(gs_names), figsize=(18, 6), sharey=False)

for i, gs in enumerate(gs_names):
    ax = axes[i]
    # Determine individual y-axis limits for each subplot
    y_min = rank_data[rank_data["GS"] == gs]["JC"].min()
    y_max = rank_data[rank_data["GS"] == gs]["JC"].max() * 1.05  # Add a 5% increment to y_max

    for exp in custom_order:
        # Filter data for the current gold standard and experiment type
        filtered_data = rank_data[(rank_data["GS"] == gs) & (rank_data["Experiment Type"] == exp)]
        
        # Append data to output
        output_data.append(filtered_data[["Rank cutoff", "JC"]].assign(GS=gs, Experiment=exp))
        
        # Plot JC vs Rank cutoff
        ax.plot(filtered_data["Rank cutoff"], filtered_data["JC"], marker="o", label={
            "top24": "targets from top 24 predictions",
            "random24": "targets from random 24 predictions",
            "bottom24 filter": "targets from bottom 24 predictions (filtered)"
        }[exp])
    
    ax.set_ylim(y_min, y_max)  # Set individual y-axis limits
    ax.set_xlabel("Rank cutoff", fontsize=24)
    if i == 0:
        ax.set_ylabel("Jaccard coefficient", fontsize=24)
        ax.text(-0.13, 1.05, "C", transform=ax.transAxes, fontsize=24, fontweight="bold", va="top", ha="left")
    ax.tick_params(axis='both', labelsize=24)
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname("Arial")
    # ax.set_title({
    #    'table2': 'Gold standard from Table 2',
    #    'uniprot': 'Gold standard from UniProt',
    #    'genecard': 'Gold standard from GeneCards'
    # }.get(gs.lower(), f"Gold standard from {gs}"), fontname="Arial")
    # ax.legend(prop={'family': 'Arial'})

# Combine all output data into a single DataFrame
output_df = pd.concat(output_data, ignore_index=True)

# Save the output data to a file
output_df.to_excel("jc_vs_rank_cutoff.xlsx", index=False)

plt.tight_layout()
plt.savefig("jaccard_coefficient_line_graph.png")
# plt.show()
