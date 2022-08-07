-- Keep a log of any SQL queries you execute as you solve the mystery.

-- See crime reports of correct date and street
SELECT * FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = "Humphrey Street";
-- id 295
-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with
-- three witnesses who were present at the time – each of their interview transcripts mentions the bakery.

-- Get interviews that mention the bakery
SELECT * FROM interviews WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%";
-- RUTH: Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
-- If you have security footage from the bakery parking lot,
-- you might want to look for cars that left the parking lot in that time frame.
-- EUGENE: I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
-- I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
-- RAYMOND: As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call,
-- I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- Follow Eugene's information
SELECT * FROM atm_transactions WHERE
atm_location = "Leggett Street" AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw";
-- Get detail of bank accounts in this query
SELECT * FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE
atm_location = "Leggett Street" AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw");
-- Get detail of people in this query
SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE
atm_location = "Leggett Street" AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw"));
-- Nothing I can do with this information yet

-- Follow Raymond's information
SELECT * FROM phone_calls WHERE duration < 60;
-- Make connection
SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE
atm_location = "Leggett Street" AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw"))
AND phone_number IN (SELECT caller FROM phone_calls WHERE duration < 60);

-- Follow Ruth's information
SELECT * FROM bakery_security_logs WHERE
year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 5 AND minute <= 25 AND activity = "exit";

-- Make connection
SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE
atm_location = "Leggett Street" AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw"))
AND phone_number IN (SELECT caller FROM phone_calls WHERE duration < 60)
AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE
year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 5 AND minute <= 25 AND activity = "exit");
-- Returns Diana (id 514354) and Bruce (id 686048). Let's get flight information on these people!
-- I will use their IDs to shorten the code
SELECT * FROM passengers WHERE passport_number IN (SELECT passport_number FROM people WHERE id = 514354 OR id = 686048);
-- They both have flights. Find the earliest flight
SELECT * FROM flights WHERE id IN (
    SELECT flight_id FROM passengers WHERE passport_number IN
    (
        SELECT passport_number FROM people WHERE id = 514354 OR id = 686048
    )
) AND year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute;
-- Earliest flight at 8:20. Let's see which one is on this flight
SELECT * FROM flights WHERE id IN (
    SELECT flight_id FROM passengers WHERE passport_number IN
    (
        SELECT passport_number FROM people WHERE id = 686048
    )
) AND year = 2021 AND month = 7 AND day = 29 AND hour = 8 AND minute = 20;
-- returns the flight, while replacing the id with 514354 does nothing. This means BRUCE IS THE THEIF!
-- Let's see where the flight is going
-- The destination_airport_id is 4
SELECT city FROM airports WHERE id = 4;
-- The flight is going to New York City
-- Let's see who called Bruce earlier
-- His phone number is (367) 555-5533
SELECT receiver FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND caller = "(367) 555-5533" AND duration < 60;
-- The receiver is (375) 555-8161
SELECT name FROM people WHERE phone_number = "(375) 555-8161";
-- Robin is the accompliance. Case closed!