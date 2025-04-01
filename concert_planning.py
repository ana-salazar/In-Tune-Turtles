import pandas as pd

# Load Excel file with all sheets
file_path = "Spotify_Daily_Top_50.xlsx"
xls = pd.ExcelFile(file_path)

# Combine all sheets that start with "page_"
data_sheets = [s for s in xls.sheet_names if s.startswith("page_")]
combined_df = pd.concat([xls.parse(sheet) for sheet in data_sheets], ignore_index=True)

# Clean artist names
combined_df['artists'] = combined_df['artists'].astype(str).str.strip()

# Count how often each artist appears
top_artists = combined_df['artists'].value_counts().head(20)
print("\n🎤 Most Frequent Artists in Top 50:")
print(top_artists)

# Optional: Filter artists by known DMV popularity
dmv_relevant_artists = [
    "Drake", "SZA", "Bad Bunny", "21 Savage", "Ice Spice", 
    "Brent Faiyaz", "Megan Thee Stallion", "Burna Boy", 
    "Peso Pluma", "Kali Uchis", "Karol G", "J Balvin"
]

# Filter DataFrame to only those artists
filtered_df = combined_df[combined_df['artists'].isin(dmv_relevant_artists)]

# Show most popular songs by these artists
top_songs = (
    filtered_df.groupby(['artists', 'name'])
    .size()
    .reset_index(name='appearances')
    .sort_values(by='appearances', ascending=False)
    .groupby('artists')
    .head(1)
)

print("\n🎵 Suggested Songs for DMV Lineup:")
print(top_songs)

# Estimate concert time (4 songs per artist, 4 mins each)
artists_selected = top_songs['artists'].unique()
minutes = len(artists_selected) * 4 * 4
print(f"\n⏱️ Total estimated runtime: {minutes} mins ({minutes / 60:.2f} hrs)")
