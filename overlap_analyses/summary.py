import pandas as pd

# Read the Excel file into a DataFrame
table2 = pd.read_excel(r"Overlap_data\Gold_standard_from_Table_2.xlsx")
uniprot = pd.read_excel(r"Overlap_data\Gold_standard_from_Uniprot.xlsx")
genecard = pd.read_excel(r"Overlap_data\Gold_standard_from_Genecard.xlsx")

top24 = pd.read_excel(r"Overlap_data\Targets_from_top_24_predictions.xlsx")
random24 = pd.read_excel(r"Overlap_data\Targets_from_random_24_predictions.xlsx")
bottom24_filter = pd.read_excel(r"Overlap_data\Bottom_24_predictions_filtered_n_geq4.xlsx")
bottom24_unfilter = pd.read_excel(r"Overlap_data\Targets_from_bottom_24_predictions_unfiltered.xlsx")

# Display the first few rows of the DataFrame to ensure it loaded correctly
# print(preds_top24.head())

columns = [
    "Experiment", 
    "Targets in GS", 
    "Targets in actual / control", 
    "Overlap (intersection)", 
    "Overlap (frequency)", 
    "Union", 
    "JC"
]

# Create the DataFrame
df = pd.DataFrame(columns=columns)

def gen_block(pred_df, pred_name, gs_df, gs_name, mode="rank"):
    global df
    results = []  # Store each row as a DataFrame in this list
    if mode == "rank":
        for rank in range(10, 101, 10):
            experiment = f"GS from {gs_name} vs. targets from {pred_name} (rank≤{rank})"
            targets_in_GS = gs_df["id"].nunique()
            targets_in_actual_control = pred_df[pred_df["rank"] <= rank]["id"].nunique()
            overlap_intersection = len(set(gs_df["id"]) & set(pred_df[pred_df["rank"] <= rank]["id"]))
            overlap_frequency = overlap_intersection / targets_in_GS
            union = len(set(gs_df["id"]) | set(pred_df[pred_df["rank"] <= rank]["id"]))
            jc = overlap_intersection / union if union > 0 else 0
            results.append([experiment, targets_in_GS, targets_in_actual_control, overlap_intersection, overlap_frequency, union, jc])
            del experiment; del targets_in_GS; del targets_in_actual_control; del overlap_intersection; del overlap_frequency; del union; del jc
    elif mode == "score":
        for score in (0.1 * x for x in range(1, 11)):
            experiment = f"GS from {gs_name} vs. targets from {pred_name} (score≥{score:.1f})"
            targets_in_GS = gs_df["id"].nunique()
            targets_in_actual_control = pred_df[pred_df["score"] >= score]["id"].nunique()
            overlap_intersection = len(set(gs_df["id"]) & set(pred_df[pred_df["score"] >= score]["id"]))
            overlap_frequency = overlap_intersection / targets_in_GS
            union = len(set(gs_df["id"]) | set(pred_df[pred_df["score"] >= score]["id"]))
            jc = overlap_intersection / union if union > 0 else 0
            results.append([experiment, targets_in_GS, targets_in_actual_control, overlap_intersection, overlap_frequency, union, jc])
            del experiment; del targets_in_GS; del targets_in_actual_control; del overlap_intersection; del overlap_frequency; del union; del jc
    # Create a DataFrame from the collected results
    return pd.DataFrame(results, columns=df.columns)

def concatenate_rows(df_list):
    global df
    for i in range(1, 11):
        df = pd.concat([
            df,
            df_list[0].iloc[[i - 1]],
            df_list[1].iloc[[i - 1]],
            df_list[2].iloc[[i - 1]],
            df_list[3].iloc[[i - 1]]
        ], ignore_index=True)

# Example Usage
top24_table2_rank = gen_block(top24, "top24", table2, "table2", mode="rank")
random24_table2_rank = gen_block(random24, "random24", table2, "table2", mode="rank")
bottom24_unfilter_table2_rank = gen_block(bottom24_unfilter, "bottom24 unfilter", table2, "table2", mode="rank")
bottom24_filter_table2_rank = gen_block(bottom24_filter, "bottom24 filter", table2, "table2", mode="rank")

# Concatenate rank data frames for table2
concatenate_rows([top24_table2_rank, random24_table2_rank, bottom24_unfilter_table2_rank, bottom24_filter_table2_rank])

top24_table2_score = gen_block(top24, "top24", table2, "table2", mode="score")
random24_table2_score = gen_block(random24, "random24", table2, "table2", mode="score")
bottom24_unfilter_table2_score = gen_block(bottom24_unfilter, "bottom24 unfilter", table2, "table2", mode="score")
bottom24_filter_table2_score = gen_block(bottom24_filter, "bottom24 filter", table2, "table2", mode="score")

# Concatenate score data frames for table2
concatenate_rows([top24_table2_score, random24_table2_score, bottom24_unfilter_table2_score, bottom24_filter_table2_score])

top24_uniprot_rank = gen_block(top24, "top24", uniprot, "uniprot", mode="rank")
random24_uniprot_rank = gen_block(random24, "random24", uniprot, "uniprot", mode="rank")
bottom24_unfilter_uniprot_rank = gen_block(bottom24_unfilter, "bottom24 unfilter", uniprot, "uniprot", mode="rank")
bottom24_filter_uniprot_rank = gen_block(bottom24_filter, "bottom24 filter", uniprot, "uniprot", mode="rank")

# Concatenate rank data frames for uniprot
concatenate_rows([top24_uniprot_rank, random24_uniprot_rank, bottom24_unfilter_uniprot_rank, bottom24_filter_uniprot_rank])

top24_uniprot_score = gen_block(top24, "top24", uniprot, "uniprot", mode="score")
random24_uniprot_score = gen_block(random24, "random24", uniprot, "uniprot", mode="score")
bottom24_unfilter_uniprot_score = gen_block(bottom24_unfilter, "bottom24 unfilter", uniprot, "uniprot", mode="score")
bottom24_filter_uniprot_score = gen_block(bottom24_filter, "bottom24 filter", uniprot, "uniprot", mode="score")

# Concatenate score data frames for uniprot
concatenate_rows([top24_uniprot_score, random24_uniprot_score, bottom24_unfilter_uniprot_score, bottom24_filter_uniprot_score])

top24_genecard_rank = gen_block(top24, "top24", genecard, "genecard", mode="rank")
random24_genecard_rank = gen_block(random24, "random24", genecard, "genecard", mode="rank")
bottom24_unfilter_genecard_rank = gen_block(bottom24_unfilter, "bottom24 unfilter", genecard, "genecard", mode="rank")
bottom24_filter_genecard_rank = gen_block(bottom24_filter, "bottom24 filter", genecard, "genecard", mode="rank")

# Concatenate rank data frames for genecard
concatenate_rows([top24_genecard_rank, random24_genecard_rank, bottom24_unfilter_genecard_rank, bottom24_filter_genecard_rank])

top24_genecard_score = gen_block(top24, "top24", genecard, "genecard", mode="score")
random24_genecard_score = gen_block(random24, "random24", genecard, "genecard", mode="score")
bottom24_unfilter_genecard_score = gen_block(bottom24_unfilter, "bottom24 unfilter", genecard, "genecard", mode="score")
bottom24_filter_genecard_score = gen_block(bottom24_filter, "bottom24 filter", genecard, "genecard", mode="score")

# Concatenate score data frames for genecard
concatenate_rows([top24_genecard_score, random24_genecard_score, bottom24_unfilter_genecard_score, bottom24_filter_genecard_score])

print(df.head())

# Write the DataFrame to an Excel file
output_file = "summary.xlsx"
df.to_excel(output_file, index=False)
