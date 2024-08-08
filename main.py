import pandas as pd

df_anime = pd.read_csv('InputData/anime.csv')
df_anime = df_anime.dropna(subset=['name'])

#Cleaning the episodes column
df_anime['episodes'].str.replace('Unknown', '0')
df_anime['episodes'] = pd.to_numeric(df_anime['episodes'], errors='coerce')

#appending dummies to the dataframe
genre_dummies = df_anime['genre'].str.get_dummies(', ').add_prefix('genre_')
df_anime_with_dummies = pd.concat([df_anime, genre_dummies], axis=1)

#creating list of unique genres
listOfGenres = []
for genreList in df_anime['genre']:
    for genre in str(genreList).split(", "):
        if genre not in listOfGenres:
            listOfGenres.append(genre)

#appending prefix to list of genres
for i in range(len(listOfGenres)):
    listOfGenres[i] = 'genre_' + listOfGenres[i]

#removing nan genres
listOfGenres.remove('genre_nan')

#Calculate the average and sum of rating, episodes and members for each genre
average_ratings = []
average_episodes = []
average_members = []
sum_ratings = []
sum_episodes = []
sum_members = []
for genre in listOfGenres:
    avg_rating = df_anime_with_dummies.loc[df_anime_with_dummies[genre] == 1, 'rating'].mean()
    average_ratings.append([genre, avg_rating])

    sum_rating = df_anime_with_dummies.loc[df_anime_with_dummies[genre] == 1, 'rating'].sum()
    sum_ratings.append([genre, sum_rating])

    avg_episode = df_anime_with_dummies.loc[df_anime_with_dummies[genre] == 1, 'episodes'].mean()
    average_episodes.append([genre, avg_episode])

    sum_episode = df_anime_with_dummies.loc[df_anime_with_dummies[genre] == 1, 'episodes'].sum()
    sum_episodes.append([genre, sum_episode])

    avg_member = df_anime_with_dummies.loc[df_anime_with_dummies[genre] == 1, 'members'].mean()
    average_members.append([genre, avg_member])

    sum_member = df_anime_with_dummies.loc[df_anime_with_dummies[genre] == 1, 'members'].sum()
    sum_members.append([genre, sum_member])

#Create the DataFrames with the results
df_genre_avg_ratings = pd.DataFrame(average_ratings, columns=['Genre', 'Average Rating'])
df_genre_avg_episodes = pd.DataFrame(average_episodes, columns=['Genre', 'Average Number of Episodes'])
df_genre_avg_members = pd.DataFrame(average_members, columns=['Genre', 'Average Number of Members'])

df_genre_sum_ratings = pd.DataFrame(sum_ratings, columns=['Genre', 'Sum Rating'])
df_genre_sum_episodes = pd.DataFrame(sum_episodes, columns=['Genre', 'Sum Number of Episodes'])
df_genre_sum_members = pd.DataFrame(sum_members, columns=['Genre', 'Sum Number of Members'])

#Creating one large DataFrame from the six smaller ones
df_agg_by_genre = df_genre_avg_episodes;

df_agg_by_genre['Average Number of Episodes'] = df_genre_avg_episodes['Average Number of Episodes']
df_agg_by_genre['Sum Number of Episodes'] = df_genre_sum_episodes['Sum Number of Episodes']
df_agg_by_genre['Average Rating'] = df_genre_avg_ratings['Average Rating']
df_agg_by_genre['Sum Rating'] = df_genre_sum_ratings['Sum Rating']
df_agg_by_genre['Average Number of Members'] = df_genre_avg_members['Average Number of Members']
df_agg_by_genre['Sum Number of Members'] = df_genre_sum_members['Sum Number of Members']

df_agg_by_genre.to_csv('PreprocessedData/AggregationsByGenre.csv', index=False)
#print(df_agg_by_genre.to_string())

#Aggregating the data by type
df_avg_by_type = df_anime_with_dummies.groupby('type')[['rating', 'episodes', 'members']].mean().reset_index()
df_avg_by_type.to_csv('PreprocessedData/AggregationsByType.csv', index=False)
#print(df_avg_by_type.to_string())