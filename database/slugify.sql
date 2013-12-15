-- Methode python pour slugify une string
CREATE OR REPLACE FUNCTION 
	slugify(texte TEXT) RETURNS TEXT 
AS $$
DECLARE
    result TEXT;
BEGIN
    result := replace(texte , 'æ', 'ae');
    result := replace(result , 'œ', 'oe');
    result := replace(result , '€', 'euros');
    result := replace(result , '$', 'dollars');
    result := replace(result , '£', 'pound');
    result := replace(result , '¥', 'yen');
    result := regexp_replace(translate(lower(result), 
        'áàâãäåāăąÁÂÃÄÅĀĂĄèééêëēĕėęěĒĔĖĘĚìíîïìĩīĭÌÍÎÏÌĨĪĬóôõöōŏőÒÓÔÕÖŌŎŐùúûüũūŭůÙÚÛÜŨŪŬŮçÇÿ&,.ñÑ',
        'aaaaaaaaaaaaaaaaaeeeeeeeeeeeeeeeiiiiiiiiiiiiiiiiooooooooooooooouuuuuuuuuuuuuuuuccy---nn'), E'[^\\w]+', '-', 'g');
    RETURN result;
END;
$$ LANGUAGE PLPGSQL;