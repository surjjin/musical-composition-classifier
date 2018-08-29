import os
import h5py
import numpy
import csv

'''
MSD data structure
    analysis / bars_confidence
    analysis / bars_start
    analysis / beats_confidence
    analysis / beats_start
    analysis / sections_confidence
    analysis / sections_start
    analysis / segments_confidence
    analysis / segments_loudness_max
    analysis / segments_loudness_max_time
    analysis / segments_loudness_start
    analysis / segments_pitches           [of interest]
    analysis / segments_start
    analysis / segments_timbre
    analysis / songs
    analysis / tatums_confidence
    analysis / tatums_start
    metadata / artist_terms
    metadata / artist_terms_freq
    metadata / artist_terms_weight
    metadata / similar_artists
    metadata / songs                       [of interest]
    musicbrainz / artist_mbtags
    musicbrainz / artist_mbtags_count
    musicbrainz / songs
'''      
count = 0
# Don't Hardcode this
pth  = 'D:\\study\\major project\\scl\\msd\\data'
pth4 = 'D:\\study\\major project\\scl\\preprocessed\\metadata'
pth5 = 'D:\\study\\major project\\scl\\preprocessed\\pitchdata'
for i1 in range(65, 91):
    pth1 = pth + "\\{}".format(chr(i1))
    if os.path.exists(pth1):
        for i2 in range(65, 91):
            pth2 = pth1 + "\\{}".format(chr(i2))
            if os.path.exists(pth2):
                for i3 in range(65, 91):
                    pth3 = pth2 + "\\{}".format((chr(i3)))
                    if os.path.exists(pth3):
                        for fname in os.listdir(pth3):
                            h5f = h5py.File("{}\\{}".format(pth3,fname), 'r')
                            fname =  fname[:-3]
                            with open("{}\\{}.csv".format(pth4,fname), 'w', newline='') as opf:
                                writer = csv.writer(opf, delimiter=',')
                                writer.writerow(['analyzer_version', 'artist_7digitalid', 'artist_familiarity', 
                                    'artist_hotttnesss', 'artist_id', 'artist_latitude', 'artist_location', 
                                    'artist_longitude', 'artist_mbid', 'artist_name', 'artist_playmeid', 'genre', 
                                    'idx_artist_terms', 'idx_similar_artists', 'release', 'release_7digitalid', 
                                    'song_hotttnesss', 'song_id', 'title', 'track_7digitalid'])
                                writer.writerow([x for x in h5f['metadata']['songs'][0]])
                            with open("{}\\{}.csv".format(pth5,fname), 'w', newline='') as opf:
                                writer = csv.writer(opf, delimiter=',')
                                writer.writerow(['st{}'.format(i) for i in range(12)])
                                for x in h5f['analysis']['segments_pitches']:
                                    writer.writerow( [str(x1) for x1 in x] )
                            count += 1
print("Number of .hdf5 processed : ", count)

            
                