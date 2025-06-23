import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

# Define folder and file paths
folder_path = "Overlap_data"
gold_standard_files = [
    os.path.join(folder_path, "Gold_standard_from_Table_2.xlsx"),
    os.path.join(folder_path, "Gold_standard_from_Uniprot.xlsx"),
    os.path.join(folder_path, "Gold_standard_from_Genecard.xlsx")
]
output_excel_file = "histograms_raw_data.xlsx"  # Save in the same folder as the script

# List of prediction files to process
prediction_files = [
    os.path.join(folder_path, "Targets_from_top_24_predictions.xlsx"),
    os.path.join(folder_path, "Targets_from_random_24_predictions.xlsx"),
    os.path.join(folder_path, "Bottom_24_predictions_filtered_n_geq4.xlsx")
]

# Hard-coded sheet names
sheet_names = [
    "table 2 x top 24",
    "table 2 x random 24",
    "table 2 x bottom 24 filtered",
    "uniprot x top 24",
    "uniprot x random 24",
    "uniprot x bottom 24 filtered",
    "genecards x top 24",
    "genecards x random 24",
    "genecards x bottom 24 filtered"
]

# Initialize histogram bins
bins = [1, 21, 41, 61, 81, 101]  # 1-20, 21-40, 41-60, 61-80, 81-100
bin_labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins) - 1)]

# Bar settings
bar_width = 0.2  # Total bar width within each bin
x_positions = np.arange(len(bin_labels))  # Center positions for each bin group

# Create a writer for the Excel file
with pd.ExcelWriter(output_excel_file) as writer:
    # Create a figure for all graphs
    fig, axes = plt.subplots(1, len(gold_standard_files), figsize=(18, 6), sharey=False)

    sheet_index = 0  # Track sheet index for assigning correct names

    for idx, (gold_standard_file, gold_standard_title) in enumerate(zip(gold_standard_files, ["Gold standard from Table 2", "Gold standard from UniProt", "Gold standard from GeneCards"])):
        gold_standard_df = pd.read_excel(gold_standard_file)
        gold_standard_df.columns = ["ID"]

        ax = axes[idx] if len(gold_standard_files) > 1 else axes

        for prediction_file, legend_label, offset in zip(prediction_files, ["targets from top 24 predictions", "targets from random 24 predictions", "targets from bottom 24 predictions(filtered)"], [-1.5 * bar_width, -0.5 * bar_width, 0.5 * bar_width]):
            # Load prediction data
            predictions_df = pd.read_excel(prediction_file)
            predictions_df = predictions_df.iloc[:, :3]  # Select the first 3 columns (rank, score, ID)
            predictions_df.columns = ["rank", "score", "ID"]

            # Initialize histogram counts
            histogram_counts = {label: 0 for label in bin_labels}
            protein_ranks = {}

            # Process each ID in the gold standard file
            for gs_id in gold_standard_df["ID"]:
                matching_rows = predictions_df[predictions_df["ID"] == gs_id]
                ranks = matching_rows["rank"].tolist()

                # Update histogram counts based on ranks
                for rank in ranks:
                    for i in range(len(bins) - 1):
                        if bins[i] <= rank < bins[i + 1]:
                            bin_label = f"{bins[i]}-{bins[i+1]-1}"
                            histogram_counts[bin_label] += 1
                            break

                # Save matching ranks for the current protein ID
                if gs_id in protein_ranks:
                    protein_ranks[gs_id].extend(ranks)
                else:
                    protein_ranks[gs_id] = ranks

            # Calculate total entries for relative frequency
            total_entries = sum(histogram_counts.values())
            relative_frequencies = {label: count / total_entries if total_entries > 0 else 0 for label, count in histogram_counts.items()}

            # Write protein ranks to a new sheet in the Excel file
            protein_ranks_df = pd.DataFrame.from_dict(protein_ranks, orient="index")
            protein_ranks_df.reset_index(inplace=True)
            protein_ranks_df.columns = ["ID"] + [f"Rank_{i+1}" for i in range(protein_ranks_df.shape[1] - 1)]
            sheet_name = sheet_names[sheet_index]
            protein_ranks_df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Prepare data for plotting
            relative_frequencies_df = pd.DataFrame(list(relative_frequencies.items()), columns=["Bin", "Relative Frequency"])

            # Plot the relative frequencies as adjacent bars
            ax.bar(x_positions + offset, relative_frequencies_df["Relative Frequency"], bar_width, label=legend_label)

            sheet_index += 1  # Increment sheet index

        # Set x-axis with bin labels centered
        ax.set_xticks(x_positions)
        ax.set_xticklabels(bin_labels, fontname="Arial", fontsize=24)
        ax.set_xlabel("Rank bins", fontname="Arial", fontsize=24)
        y_ticks = np.arange(0, 1.1, 0.1)  # Define consistent y-tick range
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([f"{tick:.1f}" for tick in y_ticks], fontname="Arial", fontsize=24)  # Apply y-tick labels to all subplots
        ax.set_title(gold_standard_title, fontname="Arial", fontsize=24)
        ax.set_ylim(0, 1.1)  # Ensure consistent y-axis scale across all subplots
        if idx == 0:
            ax.set_ylabel("Frequency", fontname="Arial", fontsize=24)
            # Add label "A" to the top left corner of the left-most graph
            ax.text(-0.1, 1.05, "A", transform=ax.transAxes, fontsize=24, fontweight="bold", va="top", ha="left", fontname="Arial")

    # Move legend below the figure
    # handles, labels = ax.get_legend_handles_labels()
    # fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False, prop={"size": 20, "family": "Arial"})

    # Finalize the figure layout
    plt.tight_layout()

    # Save the combined bar plot as a PNG file
    combined_plot_file = "combined_relative_frequencies_all.png"
    plt.savefig(combined_plot_file)
    # plt.show()
