-- Viewing the winning score from each game with the gwt_games table
WITH winning_scr AS (
 SELECT 
 	game_id,
 	MAX(total_scr) AS 'score'
 FROM gwt_game_results
 GROUP BY game_id
)
SELECT gwt_games.*, winning_scr.score
FROM gwt_games
LEFT JOIN winning_scr
ON winning_scr.game_id = gwt_games.game_id;

-- wanting to view the player table with a win tally column,

-- Creating a column noting which id's won their game
WITH winning_index AS (
	SELECT id, MAX(total_scr)
	FROM gwt_game_results
	GROUP BY game_id
)
SELECT id FROM winning_index;

-- Each row with a determined win or lose
SELECT 
	id, 
	total_scr,
	CASE
		WHEN id IN (
			SELECT id
			FROM gwt_game_results
			GROUP BY game_id
			HAVING MAX(total_scr)
			) THEN 1
			ELSE 0
		END AS winner
FROM gwt_game_results ggr;

-- The tally
SELECT 
	player_id, 
	COUNT(1) AS games_played,
	SUM(
		CASE
			WHEN id IN (
				SELECT id
				FROM gwt_game_results
				GROUP BY game_id
				HAVING MAX(total_scr)
				) THEN 1
			ELSE 0
		END
	) AS wins,
	100.0*(wins / games_played)
FROM gwt_game_results
GROUP BY 1;

-- including a winrate and kicking the case to a subquery
WITH win_bool AS (
	SELECT 
		player_id,
		CASE
			WHEN id IN (
				SELECT id
				FROM gwt_game_results
				GROUP BY game_id
				HAVING MAX(total_scr)
				) THEN 1
			ELSE 0
		END AS win
	FROM gwt_game_results
	)
SELECT 
	player_id, 
	COUNT(1) AS games_played,
	SUM(win) AS wins,
	ROUND(100.0 * SUM(win) / COUNT(1),1) AS winrate
FROM win_bool
GROUP BY 1;
