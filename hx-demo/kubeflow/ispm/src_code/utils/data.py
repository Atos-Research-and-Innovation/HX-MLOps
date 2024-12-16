import numpy as np  


def preprocess_data(df, status_or_gt: str):
    """
    Preprocess data to have a single input in a single row
    ready to be ingested in the DNN. It preprocess the input data
    and also the ground truth data.
    Args:
        df(Pandas Dataframe): Input dataframe to be preprocessed.
        status_or_gt(Str): Indicates to do the preprocessing of the 
        ingestion data or the ground truth data.
    """

    if status_or_gt == 'status':
        pivot_df = df.pivot(index=['timestamp', 'day_time'], columns='container_id', values=status_or_gt)
    else:
        pivot_df = df.pivot(index=['timestamp'], columns='container_id', values=status_or_gt)

    pivot_df.columns = [f'cnt{col}' for col in pivot_df.columns]
    pivot_df.reset_index(inplace=True)
    if status_or_gt == 'status':
        # pivot_df['day_time'] = pivot_df['day_time'] / 86400
        # Use sckit learn class to perform the min max data scalation instead to 
        # perform it without previously calculate the maximum value
        # scaler = MinMaxScaler()
        # pivot_df[['day_time']] = scaler.fit_transform(pivot_df[['day_time']])

        # Use the sin operation instead of min max to help
        # the model understand the cyclic nature of the feature.
        # Normalize 'day_time' to the range [0, 2π]
        pivot_df['day_time_normalized'] = (pivot_df['day_time'] / pivot_df['day_time'].max()) * 2 * np.pi

        # Apply sine and cosine transformations
        pivot_df['day_time_sin'] = np.sin(pivot_df['day_time_normalized'])
        pivot_df['day_time_cos'] = np.cos(pivot_df['day_time_normalized'])

        # Drop the 'day_time_normalized' column as it's no more needed
        pivot_df = pivot_df.drop(columns=['day_time_normalized', 'day_time'])
    else:
        # No preprocessing is needed for ground truth data regarding time.
        pass

    pivot_df.set_index('timestamp', inplace=True)

    return pivot_df