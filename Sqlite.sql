SELECT g.id,
    g.game_type_id,
    g.title,
    g.maker,
    g.gamer_id,
    g.number_of_players,
    g.skill_level
FROM levelupapi_game g;

SELECT g.id,
    g.game_type_id,
    g.title,
    g.maker,
    g.gamer_id,
    g.number_of_players,
    g.skill_level
FROM levelupapi_game g
WHERE g.id = 2;

SELECT g.id,
    g.game_type_id,
    g.title,
    g.maker,
    g.gamer_id,
    g.number_of_players,
    g.skill_level,
    t.label game_type
FROM levelupapi_game g
LEFT JOIN levelupapi_gametype t
    ON g.game_type_id = t.id
WHERE t.id = 2;

SELECT e.id,
       e.description
FROM levelupapi_event e
LEFT JOIN levelupapi_gamer g
    ON e.gamer_id = g.id
LEFT JOIN auth_user u
    ON g.user_id= u.id
LEFT JOIN authtoken_token t
    ON t.user_id = u.id
WHERE t.key = `fa2eba9be8282d595c997ee5cd49f2ed31f65bed`;

DELETE FROM levelupapi_events WHERE id = 5;