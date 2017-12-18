import numpy as np


def get_windowed_segments(data, window):
    step = 5
    windowed_segments = []
    segments = sliding_chunker(
        data,
        window_len=len(window),
        slide_len=step
    )
    for segment in segments:
        segment *= window
        windowed_segments.append(segment)
    return windowed_segments


def sliding_chunker(data, window_len, slide_len):
    chunks = []
    for pos in range(0, len(data), slide_len):
        chunk = np.copy(data[pos:pos+window_len])
        if len(chunk) != window_len:
            continue
        chunks.append(chunk)

    return chunks


def reconstruct(data, window, clusterer):
    window_len = window
    slide_len = int(window_len/2)
    segments = sliding_chunker(data, window_len, slide_len)
    # zeros() : float형으로 이루어진 0으로 len만큼 채워줌
    reconstructed_data = np.zeros(len(data))
    for segment_n, segment in enumerate(segments):
        # window the segment so that we can find it in our clusters which were
        # formed from windowed data
        segment *= window
        nearest_match_idx = clusterer.predict(segment)[0]
        nearest_match = np.copy(clusterer.cluster_centers_[nearest_match_idx])

        pos = segment_n * slide_len
        reconstructed_data[pos:pos+window_len] += nearest_match

    return reconstructed_data
