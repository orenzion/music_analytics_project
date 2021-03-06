-- find cluster centroid with highest danceability
select *
from `spotify-db`.kmeans_clustering_centroids cs
where cs.danceability_c = (select max(cs1.danceability_c)
						from `spotify-db`.kmeans_clustering_centroids cs1);
          
          
-- find the playlist with the highest danceability avg
select playliat_danceability.playlist_id, max(playliat_danceability.avg_danceability)
from 
	(select pt.playlist_id as playlist_id, avg(af.danceability) as avg_danceability -- playlist and avg tracks danceability
	from playlists_tracks pt join audio_features af
	on pt.track_id = af.track_id
	group by pt.playlist_id) playliat_danceability;
    

-- find the 2 playlists who share the most tracks
select pt1.playlist_id as playlist_id1, pt2.playlist_id as playlist_id1, count(pt1.track_id)
from playlists_tracks pt1 join playlists_tracks pt2
on pt1.track_id = pt2.track_id and pt1.playlist_id != pt2.playlist_id
group by pt1.playlist_id, pt2.playlist_id
having count(pt1.track_id) > 1
order by count(pt1.track_id) desc
limit 1;
-- the result is 'top hits germany' and 'top hits swizerland' playlists share the most tracks


-- find the common tracks of the 2 playlists that share the most tracks
select pt1.track_id
from playlists_tracks pt1 join playlists_tracks pt2
on pt1.track_id = pt2.track_id and pt1.playlist_id != pt2.playlist_id
where pt1.playlist_id = (select pt1.playlist_id
						from playlists_tracks pt1 join playlists_tracks pt2
						on pt1.track_id = pt2.track_id and pt1.playlist_id != pt2.playlist_id
						group by pt1.playlist_id, pt2.playlist_id
						having count(pt1.track_id) > 1
						order by count(pt1.track_id) desc
						limit 1)
and pt2.playlist_id =  (select pt2.playlist_id
						from playlists_tracks pt1 join playlists_tracks pt2
						on pt1.track_id = pt2.track_id and pt1.playlist_id != pt2.playlist_id
						group by pt1.playlist_id, pt2.playlist_id
						having count(pt1.track_id) > 1
						order by count(pt1.track_id) desc
						limit 1);


-- get the tracks audio features for the common tracks in the 2 playlists that share the most tracks ???
select *
from audio_features af join (select pt1.track_id
							from playlists_tracks pt1 join playlists_tracks pt2
							on pt1.track_id = pt2.track_id and pt1.playlist_id != pt2.playlist_id
							where pt1.playlist_id = (select pt1.playlist_id
													from playlists_tracks pt1 join playlists_tracks pt2
													on pt1.track_id = pt2.track_id and pt1.playlist_id != pt2.playlist_id
													group by pt1.playlist_id, pt2.playlist_id
													having count(pt1.track_id) > 1
													order by count(pt1.track_id) desc
													limit 1)
							and pt2.playlist_id =  (select pt2.playlist_id
													from playlists_tracks pt1 join playlists_tracks pt2
													on pt1.track_id = pt2.track_id and pt1.playlist_id != pt2.playlist_id
													group by pt1.playlist_id, pt2.playlist_id
													having count(pt1.track_id) > 1
													order by count(pt1.track_id) desc
													limit 1)) pct
on af.track_id = pct.track_id;


-- top hits by country playlists and track ids
select p.playlist_name, pt.playlist_id, pt.track_id
from playlists p join playlists_tracks pt
on p.playlist_id = pt.playlist_id
where p.playlist_name like 'Top Hits%';



-- top hits by country playlists, track ids and audio features
select p.playlist_name, pt.playlist_id, af.*
from playlists p join playlists_tracks pt join audio_features af
on p.playlist_id = pt.playlist_id and pt.track_id = af.track_id
where p.playlist_name like 'Top Hits%';


-- get distinct genres
select ag.genre, count(*) as total
from artist_genres ag
group by ag.genre
order by total desc;

-- get the tempo of track: Bridges by koresma
select af.tempo
from audio_features af 
where af.track_id = '5GiEgcvmqbD1WgHzICDvOb';


-- get a list of ids of the artists from the db that their top tracks by the given country were not extracted yet
-- the way to do it: all artirst ids minus artist ids that their tracks where extracted from the given country
select a.artist_id
from artists a 
where a.artist_id not in (select att.artist_id
						  from artists_top_tracks att
                          where att.country = 'US');
                          
                          

