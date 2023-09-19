CREATE FUNCTION findDistance(lat1 float, lon1 float, lat2 float, lon2 float)
	RETURNS FLOAT 
	language plpgsql
	as
	$$
	DECLARE
		radlat1 float;
		radlat2 float;
		theta float;
		radtheta float;
		del_lat float;
		const_a float;
		const_c float;
		dist float;
	BEGIN
		radlat1 = pi() * lat1 / 180;
		radlat2 = pi() * lat2 / 180;
		del_lat = radlat1 - radlat2;
		theta = lon1 - lon2;
		radtheta = pi() * theta / 180;
		const_a = sin(del_lat/2) * sin(del_lat/2) + cos(radlat1) * cos(radlat2) * sin(radtheta/2)* sin(radtheta/2);
		const_c = 2 * atan(sqrt(const_a)/sqrt(1-const_a));
		dist = 6371* const_c;
	RETURN dist;
END;
$$

Insert into AccidentHospital
SELECT DISTINCT accident_id, hospital_id, distance FROM
(SELECT accident_id, hospital_id, distance, rank() over (partition by accident_id order by (distance)) as distance_rank
FROM(
SELECT accident_id, hospital_id, 
		findDistance(accident_latitude, accident_longitude, hospital_latitude, hospital_longitude) as distance
		FROM (SELECT * FROM accidents NATURAL JOIN zipcodedetails) as A INNER JOIN 
		(SELECT * FROM hospitalLocation NATURAL JOIN hospitaldetails NATURAL JOIN zipcodedetails) as B		
		ON A.city = B.city) as C) as D
WHERE distance_rank = 1;