SELECT vns.id, vns.title, vns.titles, vns.released, vns.image 
FROM vns 
WHERE vns.deleted_at IS NULL AND (vns.id = 'v16459' OR vns.id = 'v28304' OR vns.id = 'v15869' OR vns.id = 'v18458') ORDER BY vns.id ASC
 LIMIT 24 OFFSET 0