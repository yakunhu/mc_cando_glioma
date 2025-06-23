import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the Excel file
file_name = "JC_comparison_data_rank_leq10.xlsx"
file_path = os.path.join(os.path.dirname(__file__), "Overlap_data", file_name)

# Extract rank information from file name if "rank" appears
if "rank" in file_name:
    start_idx = file_name.find("[rank less") + 1
    end_idx = file_name.find("]", start_idx)
    rank_info = file_name[start_idx:end_idx].replace(" less", "")
    title_suffix = f" {rank_info}".replace("=", "<=")
    output_suffix = f"[{file_name[start_idx:end_idx]}]"
else:
    title_suffix = ""
    output_suffix = ""

# Read all sheets
excel_data = pd.ExcelFile(file_path)
sheets = excel_data.sheet_names

# Initialize data storage for plotting
plot_data = []
sheet_labels = []

# Loop through each sheet
for sheet in sheets:
    # Read the sheet into a DataFrame
    df = excel_data.parse(sheet_name=sheet)

    # Check if necessary columns exist
    if "Top 24 Overlap" in df.columns and "Top 24 Union" in df.columns and "Top 100 Overlap" in df.columns and "Top 100 Union" in df.columns:
        # Count the number of proteins in each column
        top_24_overlap_count = len(df["Top 24 Overlap"].dropna())
        top_24_union_count = len(df["Top 24 Union"].dropna())
        top_100_overlap_count = len(df["Top 100 Overlap"].dropna())
        top_100_union_count = len(df["Top 100 Union"].dropna())

        # Calculate JC for Top 24 and Top 100
        jc_top_24 = top_24_overlap_count / top_24_union_count if top_24_union_count > 0 else 0
        jc_top_100 = top_100_overlap_count / top_100_union_count if top_100_union_count > 0 else 0

        # Append the values for plotting
        plot_data.append((jc_top_24, jc_top_100))
        sheet_labels.append(sheet)

# Prepare the data for plotting
indices = range(len(sheet_labels))
bar_width = 0.35

# Split the data into Top 24 and Top 100
jc_top_24_values = [x[0] for x in plot_data]
jc_top_100_values = [x[1] for x in plot_data]

# Create the plot
fig, ax = plt.subplots(figsize=(18, 10.8))

bars1 = ax.bar([i - bar_width / 2 for i in indices], jc_top_24_values, bar_width, label='Targets from top 24 predictions')
bars2 = ax.bar([i + bar_width / 2 for i in indices], jc_top_100_values, bar_width, label='Targets from top 100 predictions')

# Add labels and title
ax.set_xlabel('Indication', fontsize=24)
ax.set_ylabel('Jaccard coefficient', fontsize=24)
ax.set_title(f'Jaccard Coefficient Comparison{title_suffix.replace("rank", "Rank")}', fontsize=24)
ax.set_xticks(indices)
ax.set_xticklabels(sheet_labels, rotation=45, ha='right', fontsize=24)
ax.tick_params(axis='y', labelsize=24)

ax.legend(fontsize=24)

# Save the plot
plt.tight_layout()
output_file = f"JC_comparison_graph{output_suffix}.png"
plt.savefig(output_file)

# Show the plot
# plt.show()
