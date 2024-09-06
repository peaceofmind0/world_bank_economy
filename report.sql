--GDP per capital for the past year
SELECT c_g.country_name, 
c_g.year,
gdp_billion_dollar/c_p.population*1000000000 as gdp_dollar_per_capita 
FROM country_gdp c_g INNER JOIN country_population c_p on c_g.country_id = c_p.country_id  and c_g.YEAR = c_p.YEAR 
WHERE c_g.YEAR = YEAR(current_date) - 1
ORDER BY gdp_dollar_per_capita DESC LIMIT 10;

--region total gdp for the past year
SELECT r.region_id,r.region_name, c_g.year, 
SUM(c_g.gdp_billion_dollar) as region_total_gdp_billion_dollar 
FROM country_gdp c_g INNER JOIN country c on c_g.country_id = c.country_id 
INNER JOIN region r ON c.region_id = r.region_id 
WHERE c_g.YEAR = YEAR(current_date) - 1 
GROUP BY c_g.year,r.region_name,r.region_id 
ORDER BY YEAR DESC;

--past 5 year region total gdp
WITH total_gdp_region AS (
    SELECT r.region_id,r.region_name as region, c_g.year, 
    SUM(c_g.gdp_billion_dollar) as region_total_gdp
    FROM country_gdp c_g INNER JOIN country c on c_g.country_id = c.country_id 
    INNER JOIN region r ON c.region_id = r.region_id 
    WHERE c_g.YEAR BETWEEN YEAR(current_date) - 6 AND YEAR(current_date) - 1
    GROUP BY c_g.year,r.region_name,r.region_id 
)
SELECT year,
SUM(CASE WHEN region = 'South Asia' THEN region_total_gdp ELSE 0 END) AS south_asia_gdp,
SUM(CASE WHEN region = 'Middle East & North Africa' THEN region_total_gdp ELSE 0 END) AS middle_east_north_africa_gdp,
SUM(CASE WHEN region = 'Sub-Saharan Africa' THEN region_total_gdp ELSE 0 END) AS subsaharan_africa_gdp,
SUM(CASE WHEN region = 'Latin America & Caribbean' THEN region_total_gdp ELSE 0 END) as latin_american_caribbean_gdp, 
SUM(CASE WHEN region = 'Europe & Central Asia' THEN region_total_gdp ELSE 0 END) as europe_central_asia_gdp,
SUM(CASE WHEN region = 'North America' THEN region_total_gdp ELSE 0 END) as north_america_gdp,
SUM(CASE WHEN region = 'East Asia & Pacific' THEN region_total_gdp ELSE 0 END) as east_asi_pacific_gdp 
FROM total_gdp_region 
GROUP BY year 
ORDER BY year DESC;