SELECT movies.title
FROM ratings
INNER JOIN movies ON ratings.movie_id=movies.id
WHERE movies.id IN (SELECT movie_id FROM stars WHERE person_id IN (SELECT id FROM people WHERE name = "Chadwick Boseman"))
ORDER BY ratings.rating DESC LIMIT 5;