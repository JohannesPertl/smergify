--SELECT all user ids to the given group name
SELECT user_id FROM user_group AS g
JOIN group_has_user AS ghu ON g.group_id = ghu.group_id
WHERE g.group_name = "GroupOne"

--SELECT all artists which have the given users
SELECT uha1.artist_id FROM user_has_artist as uha1
JOIN user_has_artist as uha2 ON uha1.artist_id = uha2.artist_id
JOIN user_has_artist as uha3 ON uha2.artist_id = uha3.artist_id
WHERE (uha1.user_id = "userid1" AND uha2.user_id = "userid2" AND uha3.user_id = "userid3") AND uha1.timerange = 1