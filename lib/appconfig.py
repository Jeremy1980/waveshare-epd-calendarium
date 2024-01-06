#!/usr/bin/env python3
# -*- coding:utf-8 -*-

months = ["stycznia","lutego","marca","kwietnia","maja","czerwca","lipca","sierpnia","wrzesnia","pazdziernika","listopada","grudnia"]

# (start(day, month), end(day, month))
sign_dates = (
    ((20, 3), (19, 4)),  # Aries
    ((20, 4), (20, 5)),
    ((21, 5), (20, 6)),
    ((21, 6), (22, 7)),
    ((23, 7), (22, 8)),
    ((23, 8), (22, 9)),
    ((23, 9), (22, 10)),
    ((23, 10), (21, 11)),
    ((22, 11), (21, 12)),
    ((22, 12), (19, 1)),
    ((20, 1), (17, 2)),
    ((18, 2), (19, 3)),  # Pisces
)

# English
en_sign_dict = (
    (0, "Aries"),
    (1, "Taurus"),
    (2, "Gemini"),
    (3, "Cancer"),
    (4, "Leo"),
    (5, "Virgo"),
    (6, "Libra"),
    (7, "Scorpio"),
    (8, "Sagittarius"),
    (9, "Capricorn"),
    (10, "Aquarius"),
    (11, "Pisces"),
)

pl_sign_dict =  (
    (0, "Baran"),
    (1, "Byk"),
    (2, "Bliźnięta"),
    (3, "Rak"),
    (4, "Lew"),
    (5, "Panna"),
    (6, "Waga"),
    (7, "Skorpion"),
    (8, "Strzelec"),
    (9, "Koziorożec"),
    (10, "Wodnik"),
    (11, "Ryby"),
)
