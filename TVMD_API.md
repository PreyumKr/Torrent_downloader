### To get the season Id, you can use the following API endpoint by searching the name of the series (Search for TV shows by their original, translated and also known as names.):

https://api.themoviedb.org/3/search/tv

#### example:

```
curl --request GET \
     --url 'https://api.themoviedb.org/3/search/tv?query=family%20man&include_adult=false&language=hindi&page=1' \
     --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YjFjNzlkZGQzOTE4OWUyNmM3ZjkwNDE3YmQ4YzIwOSIsIm5iZiI6MTc3NTMxODE1MS41NDcwMDAyLCJzdWIiOiI2OWQxMzQ4NzBkMDg5MDZjZTYyZjgxMDgiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.0lY4C8q4LIm33Do-eiALEf9QvUfWudzAdfNEqQacdr8' \
     --header 'accept: application/json'
```

#### Response:

```
{
  "page": 1,
  "results": [
    {
      "adult": false,
      "backdrop_path": "/eEzKigDI64OomZV6VTJvoPGmVu1.jpg",
      "genre_ids": [
        18,
        10759
      ],
      "id": 93352,
      "origin_country": [
        "IN"
      ],
      "original_language": "hi",
      "original_name": "द फ़ैमिली मैन",
      "overview": "The story of a middle-class man who works for a special cell of the National Investigation Agency. While he tries to protect the nation from terrorists, he also has to protect his family from the impact of his secretive, high-pressure, and low paying job.",
      "popularity": 12.9253,
      "poster_path": "/tE1NUJqw9gV6AVjQ1GTK78LbWJ9.jpg",
      "first_air_date": "2019-09-20",
      "name": "The Family Man",
      "vote_average": 7.673,
      "vote_count": 176
    },
    {
      "adult": false,
      "backdrop_path": "/lbIEd7mRkB6TnGTLN54nFnbQE2y.jpg",
      "genre_ids": [
        18
      ],
      "id": 6349,
      "origin_country": [
        "HK"
      ],
      "original_language": "cn",
      "original_name": "絕世好爸",
      "overview": "Family Man is a 20 episode series aired in October 2002 on TVB. This family drama stars Paul Chun, Flora Chan, Moses Chan, Sonija Kwok, Michael Tong, and Myolie Wu. The series earned Flora Chan her first Best Actress award at the annual TVB Anniversary Awards.",
      "popularity": 4.1809,
      "poster_path": "/5qmuUKj7I7AbUnjlU5cSlyv06ze.jpg",
      "first_air_date": "2002-10-14",
      "name": "Family Man",
      "vote_average": 6,
      "vote_count": 1
    },
    {
      "adult": false,
      "backdrop_path": null,
      "genre_ids": [
        35
      ],
      "id": 24583,
      "origin_country": [
        "US"
      ],
      "original_language": "en",
      "original_name": "Family Man",
      "overview": "A TV-comedy writer and his wife deal with the tribulations of family life with her daughter and son by a previous marriage and their own 3-year-old girl.",
      "popularity": 1.7407,
      "poster_path": null,
      "first_air_date": "1988-03-18",
      "name": "Family Man",
      "vote_average": 5,
      "vote_count": 1
    },
    {
      "adult": false,
      "backdrop_path": null,
      "genre_ids": [],
      "id": 59584,
      "origin_country": [
        "US"
      ],
      "original_language": "en",
      "original_name": "Family Man",
      "overview": "Family Man is an American sitcom which aired on ABC from March 18, 1988 until April 29, 1988. It starred Richard Libertini as a middle-aged comedy writer married to a much younger wife, and focused on the trials and tribulations he faced raising two stepchildren and one biological child. The series was created by Earl Pomerantz.",
      "popularity": 0.3075,
      "poster_path": null,
      "first_air_date": "",
      "name": "Family Man",
      "vote_average": 0,
      "vote_count": 0
    },
    {
      "adult": false,
      "backdrop_path": "/sAzOPtLtqeveLDncierhahMIIpK.jpg",
      "genre_ids": [
        35
      ],
      "id": 15643,
      "origin_country": [
        "US"
      ],
      "original_language": "en",
      "original_name": "The Family Man",
      "overview": "A widowed fire chief tries to raise his four children with help from his father-in-law.",
      "popularity": 4.1096,
      "poster_path": "/vCtEwgPHBjwMgehFyGnIlaUXJx6.jpg",
      "first_air_date": "1990-09-11",
      "name": "The Family Man",
      "vote_average": 6.2,
      "vote_count": 2
    },
    {
      "adult": false,
      "backdrop_path": null,
      "genre_ids": [],
      "id": 26364,
      "origin_country": [
        "GB"
      ],
      "original_language": "en",
      "original_name": "The Family Man",
      "overview": "",
      "popularity": 0.8672,
      "poster_path": null,
      "first_air_date": "2006-03-23",
      "name": "The Family Man",
      "vote_average": 0,
      "vote_count": 0
    },
    {
      "adult": false,
      "backdrop_path": null,
      "genre_ids": [
        35
      ],
      "id": 26801,
      "origin_country": [
        "US"
      ],
      "original_language": "en",
      "original_name": "The Man in the Family",
      "overview": "The Man in the Family is an American sitcom television series that aired from June 19 until July 31, 1991.",
      "popularity": 1.7098,
      "poster_path": null,
      "first_air_date": "1991-06-19",
      "name": "The Man in the Family",
      "vote_average": 6,
      "vote_count": 1
    },
    {
      "adult": false,
      "backdrop_path": "/lne7wXqmeKGzCqE9dypCbztx1SY.jpg",
      "genre_ids": [
        10764,
        10751,
        10762
      ],
      "id": 277935,
      "origin_country": [
        "ES"
      ],
      "original_language": "ca",
      "original_name": "Manduka family",
      "overview": "",
      "popularity": 0.4016,
      "poster_path": "/uVU9Dw9DlUY6PMNrOpk1r4j9moe.jpg",
      "first_air_date": "2023-09-29",
      "name": "Manduka family",
      "vote_average": 0,
      "vote_count": 0
    },
    {
      "adult": false,
      "backdrop_path": "/jvKBKs9EW1dofpZD1IbyJwVZzAb.jpg",
      "genre_ids": [
        18
      ],
      "id": 197254,
      "origin_country": [
        "PH"
      ],
      "original_language": "tl",
      "original_name": "Mano Po Legacy: The Family Fortune",
      "overview": "Mano Po Legacy: The Family Fortune is a 2022 Philippine television drama series broadcast by GMA Network. The series is the first installment of Mano Po Legacy. Directed by Ian Loreños, it stars Barbie Forteza, Sunshine Cruz and Maricel Laxa. It premiered on January 3, 2022 on the network's Telebabad line up. The series concluded on February 25, 2022 with a total of 40 episodes.",
      "popularity": 0.7858,
      "poster_path": "/91hog9OnG6CZMegWY1t7qny6YZ3.jpg",
      "first_air_date": "2022-01-03",
      "name": "Mano Po Legacy: The Family Fortune",
      "vote_average": 0,
      "vote_count": 0
    },
    {
      "adult": false,
      "backdrop_path": null,
      "genre_ids": [],
      "id": 32862,
      "origin_country": [],
      "original_language": "en",
      "original_name": "The Family Man",
      "overview": "The Family Man is a medical drama in three parts, centered on the successful Wishart Fertility Clinic which has recently celebrated its 2000th live birth. The patriarch of the clinic is Dr Patrick Stowe. The drama follows four couples facing a spectrum of fertility problems.",
      "popularity": 0.0311,
      "poster_path": null,
      "first_air_date": "",
      "name": "The Family Man",
      "vote_average": 0,
      "vote_count": 0
    },
    {
      "adult": false,
      "backdrop_path": null,
      "genre_ids": [
        35
      ],
      "id": 250774,
      "origin_country": [
        "US"
      ],
      "original_language": "en",
      "original_name": "Manor House Family",
      "overview": "About a Family in the UK that do random stuff and illegal things.",
      "popularity": 0,
      "poster_path": "/5bDKXnRwqIIM1BcOT3MM2cwuQF6.jpg",
      "first_air_date": "",
      "name": "Manor House Family",
      "vote_average": 0,
      "vote_count": 0
    },
    {
      "adult": false,
      "backdrop_path": null,
      "genre_ids": [],
      "id": 12189,
      "origin_country": [
        "US"
      ],
      "original_language": "en",
      "original_name": "One Man's Family",
      "overview": "One Man's Family, is an American radio soap opera, heard for almost three decades, from 1932 to 1959. Created by Carlton E. Morse, it was the longest-running uninterrupted dramatic serial in the history of American radio. Television versions of the series aired in prime time from 1949 to 1952 and in daytime from 1954 to 1955.",
      "popularity": 0.0214,
      "poster_path": null,
      "first_air_date": "",
      "name": "One Man's Family",
      "vote_average": 0,
      "vote_count": 0
    },
    {
      "adult": false,
      "backdrop_path": "/l7wShoIdIUwaDIbsHno9pO5MZXT.jpg",
      "genre_ids": [
        16,
        35
      ],
      "id": 1434,
      "origin_country": [
        "US"
      ],
      "original_language": "en",
      "original_name": "Family Guy",
      "overview": "Sick, twisted, politically incorrect and Freakin' Sweet animated series featuring the adventures of the dysfunctional Griffin family. Bumbling Peter and long-suffering Lois have three kids. Stewie (a brilliant but sadistic baby bent on killing his mother and taking over the world), Meg (the oldest, and is the most unpopular girl in town) and Chris (the middle kid, he's not very bright but has a passion for movies). The final member of the family is Brian - a talking dog and much more than a pet, he keeps Stewie in check whilst sipping Martinis and sorting through his own life issues.",
      "popularity": 270.2438,
      "poster_path": "/3PFsEuAiyLkWsP4GG6dIV37Q6gu.jpg",
      "first_air_date": "1999-01-31",
      "name": "Family Guy",
      "vote_average": 7.4,
      "vote_count": 4865
    },
    {
      "adult": false,
      "backdrop_path": "/rNozBTiuyygiWtsM4vXB4OkARwo.jpg",
      "genre_ids": [
        16,
        35
      ],
      "id": 1260,
      "origin_country": [
        "US"
      ],
      "original_language": "en",
      "original_name": "Duckman",
      "overview": "Together with Cornfed, his portly, porcine partner in crime solving, this defective detective amazingly manages to solve crimes and be a single parent to his hilariously dysfunctional sons at the same time.",
      "popularity": 24.3657,
      "poster_path": "/tUSieKYAFqgb8x4UZjqOtjkh16y.jpg",
      "first_air_date": "1994-03-05",
      "name": "Duckman",
      "vote_average": 7.1,
      "vote_count": 72
    },
    {
      "adult": false,
      "backdrop_path": "/spbj275EvLvMxnAV9uAMIfl2LRa.jpg",
      "genre_ids": [
        18
      ],
      "id": 21327,
      "origin_country": [
        "KR"
      ],
      "original_language": "ko",
      "original_name": "별난여자 별난남자",
      "overview": "The story follows an extended family's love dilemmas, family arguments and family secrets.",
      "popularity": 6.1777,
      "poster_path": "/tsNqVUQtTaj7Bck1k8cLrbC9fCz.jpg",
      "first_air_date": "2005-09-26",
      "name": "Bizarre Bunch",
      "vote_average": 0,
      "vote_count": 0
    },
    {
      "adult": false,
      "backdrop_path": "/lUred7U3O41usl53TEwj2egjsSH.jpg",
      "genre_ids": [
        18
      ],
      "id": 195305,
      "origin_country": [
        "MX"
      ],
      "original_language": "es",
      "original_name": "Familia de medianoche",
      "overview": "Marigaby is a medical student by day—and by night, she saves lives with her family in Mexico City's high-stakes business of private ambulances. As pressure from both worlds threatens to drag her down, Marigaby will do whatever it takes to stay afloat.",
      "popularity": 5.3626,
      "poster_path": "/3hwZQGHjuy6qhkgshPe7QPRSBVH.jpg",
      "first_air_date": "2024-09-24",
      "name": "Midnight Family",
      "vote_average": 7.8,
      "vote_count": 41
    },
    {
      "adult": false,
      "backdrop_path": "/mgAsmDCaZtquMTogaW4RH7RbsU0.jpg",
      "genre_ids": [
        18
      ],
      "id": 135692,
      "origin_country": [
        "CN"
      ],
      "original_language": "zh",
      "original_name": "海上孟府",
      "overview": "",
      "popularity": 3.4548,
      "poster_path": "/wsf6LBtIJl24lDP86OmFakISK5z.jpg",
      "first_air_date": "2013-12-27",
      "name": "Meng's Palace",
      "vote_average": 0,
      "vote_count": 0
    },
    {
      "adult": false,
      "backdrop_path": "/wk5bZjCtWiaiyG3zQN0aqJOipmS.jpg",
      "genre_ids": [
        99,
        80
      ],
      "id": 249582,
      "origin_country": [
        "US"
      ],
      "original_language": "en",
      "original_name": "CTRL+ALT+DESIRE",
      "overview": "Learn the haunting case of Grant Amato, a 29-year-old Florida man accused of murdering his own family execution style for the love of a cam girl.",
      "popularity": 0.3279,
      "poster_path": "/wALAs5agJcT1PtPVNFNBaCYQKIP.jpg",
      "first_air_date": "2024-04-16",
      "name": "CTRL+ALT+DESIRE",
      "vote_average": 6,
      "vote_count": 9
    },
    {
      "adult": false,
      "backdrop_path": "/uDmDOp2yU63asHFrwwMCwAsoFFQ.jpg",
      "genre_ids": [
        18
      ],
      "id": 292277,
      "origin_country": [
        "CN"
      ],
      "original_language": "zh",
      "original_name": "奇迹",
      "overview": "In Shenzhen, a jobless Lu Da rekindles hope in a 24-hour bookstore; opera star Fan becomes a tech sales whiz in Huaqiangbei; delivery rider Tan earns dignity; drone engineers Zhang Yi and Nuan build love with code; teen Xiao Peng creates a wildlife overpass; planner Wang Pengqian and daughter protect mangroves, with spoonbill Y075 marking eco-change. These stories weave entrepreneurship, innovation, and sustainability, showcasing Shenzhen’s 45-year transformation and future promise.",
      "popularity": 7.9759,
      "poster_path": "/sofXwv1F6yV1CkBmJDkZ7mMgIGl.jpg",
      "first_air_date": "2025-12-22",
      "name": "The Miracles",
      "vote_average": 8,
      "vote_count": 3
    },
    {
      "adult": false,
      "backdrop_path": null,
      "genre_ids": [
        18
      ],
      "id": 316540,
      "origin_country": [
        "SG",
        "CN"
      ],
      "original_language": "zh",
      "original_name": "嫁入高门",
      "overview": "It follows Lu Xiaofan, an ordinary man who enters the elite Bei family through an arranged marriage. Faced with his cold, aristocratic husband Bei Lyuqing and the sharp class divide, Lu survives the schemes of high society with quiet resilience. It’s a story of social disparity, hidden depths, and a humble heart eventually earning respect and love in a world of power.",
      "popularity": 0.4429,
      "poster_path": "/yuP6wDaNlsUbKVlbXIydwfrqHVn.jpg",
      "first_air_date": "2026-06-30",
      "name": "Bittersweet Love",
      "vote_average": 0,
      "vote_count": 0
    }
  ],
  "total_pages": 2,
  "total_results": 21
}
```

Choose the first one from the results and get the season details using the series id.

### To get the season details, you can use the following API endpoint:

https://api.themoviedb.org/3/tv/{series_id}

#### example:

```
curl --request GET \
     --url 'https://api.themoviedb.org/3/tv/95557?language=en-US' \
     --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YjFjNzlkZGQzOTE4OWUyNmM3ZjkwNDE3YmQ4YzIwOSIsIm5iZiI6MTc3NTMxODE1MS41NDcwMDAyLCJzdWIiOiI2OWQxMzQ4NzBkMDg5MDZjZTYyZjgxMDgiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.0lY4C8q4LIm33Do-eiALEf9QvUfWudzAdfNEqQacdr8' \
     --header 'accept: application/json'
```

#### Response:

```
{
  "adult": false,
  "backdrop_path": "/dfmPbyeZZSz3bekeESvMJaH91gS.jpg",
  "created_by": [],
  "episode_run_time": [],
  "first_air_date": "2021-03-25",
  "genres": [
    {
      "id": 16,
      "name": "Animation"
    },
    {
      "id": 18,
      "name": "Drama"
    },
    {
      "id": 10765,
      "name": "Sci-Fi & Fantasy"
    },
    {
      "id": 10759,
      "name": "Action & Adventure"
    }
  ],
  "homepage": "https://www.amazon.com/dp/B08WJP55PR",
  "id": 95557,
  "in_production": true,
  "languages": [
    "en"
  ],
  "last_air_date": "2026-04-01",
  "last_episode_to_air": {
    "id": 6951280,
    "name": "GIVE US A MOMENT",
    "overview": "Mark embarks on a new and dangerous mission, throwing Debbie into a tailspin and plunging Eve into uncertainty.",
    "vote_average": 8.028,
    "vote_count": 18,
    "air_date": "2026-04-01",
    "episode_number": 5,
    "episode_type": "standard",
    "production_code": "",
    "runtime": 51,
    "season_number": 4,
    "show_id": 95557,
    "still_path": "/zbCcDf2fVUlutvArKJtH1yiMZWC.jpg"
  },
  "name": "Invincible",
  "next_episode_to_air": {
    "id": 6951281,
    "name": "YOU LOOK HORRIBLE",
    "overview": "Family bonds are put to the test. Under pressure, Allen makes a new friend.",
    "vote_average": 0,
    "vote_count": 0,
    "air_date": "2026-04-08",
    "episode_number": 6,
    "episode_type": "standard",
    "production_code": "",
    "runtime": null,
    "season_number": 4,
    "show_id": 95557,
    "still_path": "/k7Z18kQXUbVy7Q9M42qOqGhVuTs.jpg"
  },
  "networks": [
    {
      "id": 1024,
      "logo_path": "/w7HfLNm9CWwRmAMU58udl2L7We7.png",
      "name": "Prime Video",
      "origin_country": ""
    }
  ],
  "number_of_episodes": 32,
  "number_of_seasons": 5,
  "origin_country": [
    "US"
  ],
  "original_language": "en",
  "original_name": "Invincible",
  "overview": "Mark Grayson is a normal teenager except for the fact that his father is the most powerful superhero on the planet. Shortly after his seventeenth birthday, Mark begins to develop powers of his own and enters into his father's tutelage.",
  "popularity": 228.4932,
  "poster_path": "/4tblBrslcKSifMVZ3TmtT2ukMor.jpg",
  "production_companies": [
    {
      "id": 20580,
      "logo_path": "/oRR9EXVoKP9szDkVKlze5HVJS7g.png",
      "name": "Amazon Studios",
      "origin_country": "US"
    },
    {
      "id": 151645,
      "logo_path": null,
      "name": "Skybound North",
      "origin_country": "CA"
    },
    {
      "id": 50032,
      "logo_path": "/ojrMksdtR7Bs2vwERU1LCrjv7vx.png",
      "name": "Skybound Entertainment",
      "origin_country": "US"
    },
    {
      "id": 215052,
      "logo_path": null,
      "name": "Skybound Animation",
      "origin_country": ""
    },
    {
      "id": 210099,
      "logo_path": "/g5oRCNCi8kNVb8gEoSoIcqkhjmR.png",
      "name": "Amazon MGM Studios",
      "origin_country": "US"
    }
  ],
  "production_countries": [
    {
      "iso_3166_1": "CA",
      "name": "Canada"
    },
    {
      "iso_3166_1": "US",
      "name": "United States of America"
    }
  ],
  "seasons": [
    {
      "air_date": "2023-07-21",
      "episode_count": 1,
      "id": 349664,
      "name": "Specials",
      "overview": "",
      "poster_path": "/bHZWrwiMtvE7jd8g46Aiqb1VM4Y.jpg",
      "season_number": 0,
      "vote_average": 0
    },
    {
      "air_date": "2021-03-25",
      "episode_count": 8,
      "id": 136020,
      "name": "Season 1",
      "overview": "Nolan Grayson (Omni-Man) is unquestionably the strongest being on our planet; he is also our most spirited protector, having saved the planet from untold calamity. His son Mark, wants nothing more than to follow in his footsteps. But there's something sinister afoot and Omni-man may not be what he appears. Which may prove even too much for the Guardians of the Globe.",
      "poster_path": "/yDWJYRAwMNKbIYT8ZB33qy84uzO.jpg",
      "season_number": 1,
      "vote_average": 7.9
    },
    {
      "air_date": "2023-11-02",
      "episode_count": 8,
      "id": 325266,
      "name": "Season 2",
      "overview": "After an earth-shattering betrayal, Mark fights to rebuild his life. In the face of apocalyptic threats, he discovers new allies and wrestles with his greatest fear - that he might become his father.",
      "poster_path": "/dMOpdkrDC5dQxqNydgKxXjBKyAc.jpg",
      "season_number": 2,
      "vote_average": 7.7
    },
    {
      "air_date": "2025-02-06",
      "episode_count": 8,
      "id": 423637,
      "name": "Season 3",
      "overview": "Everything changes as Mark is forced to face his past and his future, while discovering how much further he'll need to go to protect the people he loves.",
      "poster_path": "/w9XQ7ehwaxqV6WJSAUE0qLTQHgq.jpg",
      "season_number": 3,
      "vote_average": 7.6
    },
    {
      "air_date": "2026-03-18",
      "episode_count": 8,
      "id": 480006,
      "name": "Season 4",
      "overview": "While the world recovers from the global catastrophe of last season, a changed Mark struggles with guilt as he fights to protect his home and the people he loves, setting him on a collision course with a powerful new threat that could alter the fate of humanity forever.",
      "poster_path": "/4tblBrslcKSifMVZ3TmtT2ukMor.jpg",
      "season_number": 4,
      "vote_average": 7.4
    },
    {
      "air_date": null,
      "episode_count": 0,
      "id": 480007,
      "name": "Season 5",
      "overview": "",
      "poster_path": null,
      "season_number": 5,
      "vote_average": 0
    }
  ],
  "spoken_languages": [
    {
      "english_name": "English",
      "iso_639_1": "en",
      "name": "English"
    }
  ],
  "status": "Returning Series",
  "tagline": "Almost there.",
  "type": "Scripted",
  "vote_average": 8.622,
  "vote_count": 5454
}
```

### To get a episode details, you can use the following API endpoint:

https://api.themoviedb.org/3/tv/{series_id}/season/{season_number}

#### example:

```
curl --request GET \
     --url 'https://api.themoviedb.org/3/tv/95557/season/4?language=en-US' \
     --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YjFjNzlkZGQzOTE4OWUyNmM3ZjkwNDE3YmQ4YzIwOSIsIm5iZiI6MTc3NTMxODE1MS41NDcwMDAyLCJzdWIiOiI2OWQxMzQ4NzBkMDg5MDZjZTYyZjgxMDgiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.0lY4C8q4LIm33Do-eiALEf9QvUfWudzAdfNEqQacdr8' \
     --header 'accept: application/json'
```

#### Response:

```
{
  "_id": "68ef34c548f2d47f31f0a0f5",
  "air_date": "2026-03-18",
  "episodes": [
    {
      "air_date": "2026-03-18",
      "episode_number": 1,
      "episode_type": "standard",
      "id": 6876600,
      "name": "MAKING THE WORLD A BETTER PLACE",
      "overview": "Mark battles enemies new and old in his fight to keep Earth safe.",
      "production_code": "INVI 401",
      "runtime": 53,
      "season_number": 4,
      "show_id": 95557,
      "still_path": "/uJXlwnJCp9BuAhW2y8SjbvCcRct.jpg",
      "vote_average": 7.833,
      "vote_count": 24,
      "crew": [
        {
          "job": "Writer",
          "department": "Writing",
          "credit_id": "64bc001baf85de0100193d18",
          "adult": false,
          "gender": 1,
          "id": 1852634,
          "known_for_department": "Writing",
          "name": "Helen Leigh",
          "original_name": "Helen Leigh",
          "popularity": 0.2719,
          "profile_path": null
        },
        {
          "job": "Director",
          "department": "Directing",
          "credit_id": "6544b6156beaea014b66d702",
          "adult": false,
          "gender": 2,
          "id": 1896377,
          "known_for_department": "Directing",
          "name": "Sol Choi",
          "original_name": "Sol Choi",
          "popularity": 0.5399,
          "profile_path": "/n69OtJPQIowcNek8EvRzYPPlhpS.jpg"
        }
      ],
      "guest_stars": [
        {
          "character": "Additional Voices (voice)",
          "credit_id": "6544b7aefd4f80013ce7dbcd",
          "order": 522,
          "adult": false,
          "gender": 1,
          "id": 1226797,
          "known_for_department": "Acting",
          "name": "Nyima Funk",
          "original_name": "Nyima Funk",
          "popularity": 0.509,
          "profile_path": "/rx7rt8E0chx3rwoici36IJPmN7W.jpg"
        },
        {
          "character": "Additional Voices (voice)",
          "credit_id": "6544b7c49d6e3306c88ecb76",
          "order": 523,
          "adult": false,
          "gender": 2,
          "id": 1422233,
          "known_for_department": "Acting",
          "name": "Dan Navarro",
          "original_name": "Dan Navarro",
          "popularity": 0.4967,
          "profile_path": "/8QN7jNDU5PahZ29tH4a7XOyWkWZ.jpg"
        },
        {
          "character": "Additional Voices (voice)",
          "credit_id": "6544b7cc6beaea012c8d4b02",
          "order": 524,
          "adult": false,
          "gender": 1,
          "id": 1171640,
          "known_for_department": "Acting",
          "name": "Ami Shukla",
          "original_name": "Ami Shukla",
          "popularity": 0.2469,
          "profile_path": "/e8HhshT5p9CDeVV6TZVY4YJGpV0.jpg"
        },
        {
          "character": "Paul (voice)",
          "credit_id": "654ddfab29383543f0b60655",
          "order": 528,
          "adult": false,
          "gender": 2,
          "id": 7248,
          "known_for_department": "Acting",
          "name": "Cliff Curtis",
          "original_name": "Cliff Curtis",
          "popularity": 2.7922,
          "profile_path": "/dfaElGoyJWseFWxXwEMLL9WTi7V.jpg"
        },
        {
          "character": "Art (voice)",
          "credit_id": "6552c489fd6fa100e1e43a45",
          "order": 537,
          "adult": false,
          "gender": 2,
          "id": 2,
          "known_for_department": "Acting",
          "name": "Mark Hamill",
          "original_name": "Mark Hamill",
          "popularity": 4.7435,
          "profile_path": "/zMQ93JTLW8KxusKhOlHFZhih3YQ.jpg"
        },
        {
          "character": "Donald (voice)",
          "credit_id": "6552c4b1fd6fa100fee7144d",
          "order": 538,
          "adult": false,
          "gender": 2,
          "id": 1217648,
          "known_for_department": "Acting",
          "name": "Chris Diamantopoulos",
          "original_name": "Chris Diamantopoulos",
          "popularity": 1.6808,
          "profile_path": "/oenBtpk0RTId4wacQKYU4cPcq8Z.jpg"
        },
        {
          "character": "Cecil (voice)",
          "credit_id": "65aeba726af8f8010c96c966",
          "order": 568,
          "adult": false,
          "gender": 2,
          "id": 27740,
          "known_for_department": "Acting",
          "name": "Walton Goggins",
          "original_name": "Walton Goggins",
          "popularity": 5.0205,
          "profile_path": "/5lcVMJbWrNDFiWa1WxK4oR8zwev.jpg"
        },
        {
          "character": "Eve (voice)",
          "credit_id": "65aebaa9aad9c200ca5a13e1",
          "order": 572,
          "adult": false,
          "gender": 1,
          "id": 94098,
          "known_for_department": "Acting",
          "name": "Gillian Jacobs",
          "original_name": "Gillian Jacobs",
          "popularity": 2.1631,
          "profile_path": "/9fGHBU38slGZ6aOdwLgvrVNwCV5.jpg"
        },
        {
          "character": "Oliver (voice)",
          "credit_id": "67a5af42470bb75ff266fd8a",
          "order": 652,
          "adult": false,
          "gender": 2,
          "id": 1721268,
          "known_for_department": "Acting",
          "name": "Christian Convery",
          "original_name": "Christian Convery",
          "popularity": 3.1244,
          "profile_path": "/tOR2tSrvHPVDltE4jBDEva3GNqY.jpg"
        },
        {
          "character": "Brit (voice)",
          "credit_id": "67c95f11ef9a90cdba24a631",
          "order": 707,
          "adult": false,
          "gender": 2,
          "id": 783,
          "known_for_department": "Acting",
          "name": "Jonathan Banks",
          "original_name": "Jonathan Banks",
          "popularity": 4.2179,
          "profile_path": "/bswk26L13PvY4iMTwUTAsepXCLv.jpg"
        },
        {
          "character": "Conquest (voice)",
          "credit_id": "67c96045fb4402dce1034f30",
          "order": 714,
          "adult": false,
          "gender": 2,
          "id": 47296,
          "known_for_department": "Acting",
          "name": "Jeffrey Dean Morgan",
          "original_name": "Jeffrey Dean Morgan",
          "popularity": 6.4051,
          "profile_path": "/m8bdrmh6ExDCGQ64E83mHg002YV.jpg"
        },
        {
          "character": "Amanda / Betsy (voice)",
          "credit_id": "69bb8dc782dccd430c00f1ba",
          "order": 728,
          "adult": false,
          "gender": 1,
          "id": 15761,
          "known_for_department": "Acting",
          "name": "Grey DeLisle",
          "original_name": "Grey DeLisle",
          "popularity": 3.0491,
          "profile_path": "/vrUHaXe1pG56yZkgH7Hs3LGRLTT.jpg"
        },
        {
          "character": "Universa (voice)",
          "credit_id": "69bb8de3d0ff176f112c9878",
          "order": 729,
          "adult": false,
          "gender": 1,
          "id": 82104,
          "known_for_department": "Acting",
          "name": "Danai Gurira",
          "original_name": "Danai Gurira",
          "popularity": 2.4239,
          "profile_path": "/z7H7QeQvr24vskGlANQhG43vozQ.jpg"
        },
        {
          "character": "Burke / Engineer (voice)",
          "credit_id": "69bb8e0c82babb958aa984ce",
          "order": 730,
          "adult": false,
          "gender": 2,
          "id": 1552817,
          "known_for_department": "Acting",
          "name": "Christian Lanz",
          "original_name": "Christian Lanz",
          "popularity": 0.5043,
          "profile_path": "/4GDmhCJvdOQHV0uRuK34XJBMiTr.jpg"
        },
        {
          "character": "Rex / Robot (voice)",
          "credit_id": "69bb8e1559fd3bdf98a9848e",
          "order": 731,
          "adult": false,
          "gender": 2,
          "id": 555249,
          "known_for_department": "Acting",
          "name": "Ross Marquand",
          "original_name": "Ross Marquand",
          "popularity": 1.4799,
          "profile_path": "/2CxkVPimin0c2v7fUK3MGjgEnLt.jpg"
        },
        {
          "character": "Additional Voices (voice)",
          "credit_id": "69bb8e3282babb958aa984d2",
          "order": 732,
          "adult": false,
          "gender": 2,
          "id": 4354816,
          "known_for_department": "Acting",
          "name": "Bobby Kesselman",
          "original_name": "Bobby Kesselman",
          "popularity": 0.243,
          "profile_path": null
        }
      ]
    },
    {
      "air_date": "2026-03-18",
      "episode_number": 2,
      "episode_type": "standard",
      "id": 6951277,
      "name": "I'LL GIVE YOU THE GRAND TOUR",
      "overview": "Loyalties are challenged when an old enemy is revealed.",
      "production_code": "INVI 402",
      "runtime": 51,
      "season_number": 4,
      "show_id": 95557,
      "still_path": "/eZljaDBUuBrKQjm0sRKfKorNFmk.jpg",
      "vote_average": 7.6,
      "vote_count": 14,
      "crew": [
        {
          "job": "Writer",
          "department": "Writing",
          "credit_id": "605d64e3eea34d0052598874",
          "adult": false,
          "gender": 2,
          "id": 1227315,
          "known_for_department": "Writing",
          "name": "Simon Racioppa",
          "original_name": "Simon Racioppa",
          "popularity": 0.3504,
          "profile_path": "/tZUAIEOGGd0ZpxETgXgqRQRGkIy.jpg"
        },
        {
          "job": "Director",
          "department": "Directing",
          "credit_id": "65606e9c3679a1097527f46f",
          "adult": false,
          "gender": 2,
          "id": 3032717,
          "known_for_department": "Art",
          "name": "Jason Zurek",
          "original_name": "Jason Zurek",
          "popularity": 0.2957,
          "profile_path": "/aiLjcLKre1uD5m7YVHxvoxz67yM.jpg"
        }
      ],
      "guest_stars": [
        {
          "character": "Allen (voice)",
          "credit_id": "605d6a277c6de300538cef1c",
          "order": 504,
          "adult": false,
          "gender": 2,
          "id": 19274,
          "known_for_department": "Acting",
          "name": "Seth Rogen",
          "original_name": "Seth Rogen",
          "popularity": 4.8993,
          "profile_path": "/nYl9bvQzaPQLzlf0wf75clLN6Hi.jpg"
        },
        {
          "character": "Thadeus (voice)",
          "credit_id": "65573a777f054018d6f30174",
          "order": 553,
          "adult": false,
          "gender": 2,
          "id": 19540,
          "known_for_department": "Acting",
          "name": "Peter Cullen",
          "original_name": "Peter Cullen",
          "popularity": 2.4116,
          "profile_path": "/9Snf4fBUkk5MrAjqtNtgZRJYJbj.jpg"
        },
        {
          "character": "Telia (voice)",
          "credit_id": "65573b017f054018d6f301b3",
          "order": 556,
          "adult": false,
          "gender": 1,
          "id": 61134,
          "known_for_department": "Acting",
          "name": "Tatiana Maslany",
          "original_name": "Tatiana Maslany",
          "popularity": 2.567,
          "profile_path": "/x8lBkm9CBJbIlLpqjEwkQydZ2or.jpg"
        },
        {
          "character": "General Kregg (voice)",
          "credit_id": "65606f762b113d010cc0bbfb",
          "order": 562,
          "adult": false,
          "gender": 2,
          "id": 6574,
          "known_for_department": "Acting",
          "name": "Clancy Brown",
          "original_name": "Clancy Brown",
          "popularity": 5.0628,
          "profile_path": "/1JeBRNG7VS7r64V9lOvej9bZXW5.jpg"
        },
        {
          "character": "Conquest (voice)",
          "credit_id": "67c96045fb4402dce1034f30",
          "order": 714,
          "adult": false,
          "gender": 2,
          "id": 47296,
          "known_for_department": "Acting",
          "name": "Jeffrey Dean Morgan",
          "original_name": "Jeffrey Dean Morgan",
          "popularity": 6.4051,
          "profile_path": "/m8bdrmh6ExDCGQ64E83mHg002YV.jpg"
        },
        {
          "character": "The Captain (voice)",
          "credit_id": "69bb8f6d1d22ea51f700f1af",
          "order": 733,
          "adult": false,
          "gender": 2,
          "id": 162371,
          "known_for_department": "Acting",
          "name": "Scott Aukerman",
          "original_name": "Scott Aukerman",
          "popularity": 1.1047,
          "profile_path": "/8EzxI2WvFBABaVe7ISrBy8nucp4.jpg"
        },
        {
          "character": "Male Viltrumite / Geldarian Warrior (voice)",
          "credit_id": "69bb8f7c0040fb8b9257d87c",
          "order": 734,
          "adult": false,
          "gender": 2,
          "id": 963818,
          "known_for_department": "Acting",
          "name": "Troy Baker",
          "original_name": "Troy Baker",
          "popularity": 2.0805,
          "profile_path": "/9jeUft7h20HscRCrsVQTgKHXRwJ.jpg"
        },
        {
          "character": "Viltrumite General (voice)",
          "credit_id": "69bb8f85f551a555eba9847f",
          "order": 735,
          "adult": false,
          "gender": 2,
          "id": 2573962,
          "known_for_department": "Acting",
          "name": "Cleveland Berto",
          "original_name": "Cleveland Berto",
          "popularity": 0.5261,
          "profile_path": "/avhpOvkXDn0VSE6cXHneGKGXNrS.jpg"
        },
        {
          "character": "Space Racer (voice)",
          "credit_id": "69bb8fc47d78dcf5362c9837",
          "order": 736,
          "adult": false,
          "gender": 2,
          "id": 1447932,
          "known_for_department": "Acting",
          "name": "Winston Duke",
          "original_name": "Winston Duke",
          "popularity": 2.4303,
          "profile_path": "/MhBiZbryibwuoEtPL9Ns8pYHC1.jpg"
        },
        {
          "character": "Viltrumite Girl / Viltrumite Children (voice)",
          "credit_id": "69bb8fe0d27aba35f72c9976",
          "order": 737,
          "adult": false,
          "gender": 1,
          "id": 3232058,
          "known_for_department": "Acting",
          "name": "Ellie Reine",
          "original_name": "Ellie Reine",
          "popularity": 0.3346,
          "profile_path": "/o0QVIi2VbbzhVXvyBkXSd46eoWZ.jpg"
        },
        {
          "character": "Viltrumite Boy (voice)",
          "credit_id": "69bb8ff6a15bacc1cc3b9a32",
          "order": 738,
          "adult": false,
          "gender": 2,
          "id": 3728806,
          "known_for_department": "Acting",
          "name": "Xander Mateo",
          "original_name": "Xander Mateo",
          "popularity": 0.2149,
          "profile_path": "/4TVtaMDwx6Gz5y3jutfa0PRs0Sb.jpg"
        },
        {
          "character": "Thragg (voice)",
          "credit_id": "69bb90102ce36f900aaafb03",
          "order": 739,
          "adult": false,
          "gender": 2,
          "id": 72095,
          "known_for_department": "Acting",
          "name": "Lee Pace",
          "original_name": "Lee Pace",
          "popularity": 3.2934,
          "profile_path": "/eeTc0d2AX1vFYVxZ6Qw7qZpg4Tz.jpg"
        },
        {
          "character": "Data 1 (voice)",
          "credit_id": "69bb901b4335cdd74e57d6e2",
          "order": 740,
          "adult": false,
          "gender": 2,
          "id": 1099717,
          "known_for_department": "Acting",
          "name": "Jay Pharoah",
          "original_name": "Jay Pharoah",
          "popularity": 1.2414,
          "profile_path": "/qpCc7SshxYXcgZIjhv8xKWuzEp6.jpg"
        },
        {
          "character": "Data 2 / Beast Leader (voice)",
          "credit_id": "69bb9039cd3aeb5ee023d6a4",
          "order": 741,
          "adult": false,
          "gender": 2,
          "id": 60279,
          "known_for_department": "Acting",
          "name": "Fred Tatasciore",
          "original_name": "Fred Tatasciore",
          "popularity": 2.1669,
          "profile_path": "/7pxLvE4l5mQkGzHLIEwYrc9AMFe.jpg"
        },
        {
          "character": "Female Viltrumite / Young Viltrumite Soldier 2 (voice)",
          "credit_id": "69bb905b22a73873730526a7",
          "order": 742,
          "adult": false,
          "gender": 1,
          "id": 76029,
          "known_for_department": "Acting",
          "name": "Courtenay Taylor",
          "original_name": "Courtenay Taylor",
          "popularity": 1.2519,
          "profile_path": "/f58KNRoimAh5Irddrek2mtPEBam.jpg"
        },
        {
          "character": "Young Nolan / Young Viltrumite Soldier (voice)",
          "credit_id": "69bb907276bb957154aafb24",
          "order": 743,
          "adult": false,
          "gender": 2,
          "id": 2837439,
          "known_for_department": "Acting",
          "name": "Talon Warburton",
          "original_name": "Talon Warburton",
          "popularity": 0.4501,
          "profile_path": "/uJCEouwvWxS5aO9FDyMbukfSAUw.jpg"
        }
      ]
    },
    {
      "air_date": "2026-03-18",
      "episode_number": 3,
      "episode_type": "standard",
      "id": 6951278,
      "name": "I GOTTA GET SOME AIR",
      "overview": "Consequences weigh on Mark. Oliver takes on a new job.",
      "production_code": "INVI 403",
      "runtime": 49,
      "season_number": 4,
      "show_id": 95557,
      "still_path": "/feqa4Ct3uOpMvwWfJkvQet6w1yP.jpg",
      "vote_average": 7,
      "vote_count": 15,
      "crew": [
        {
          "job": "Writer",
          "department": "Writing",
          "credit_id": "67c02cbac93271491f359fac",
          "adult": false,
          "gender": 2,
          "id": 4306926,
          "known_for_department": "Production",
          "name": "Ross Stracke",
          "original_name": "Ross Stracke",
          "popularity": 0.2588,
          "profile_path": "/nkSmIq0JyGp6w0yu83v9ZkYVdrE.jpg"
        },
        {
          "job": "Director",
          "department": "Directing",
          "credit_id": "69bb8b24a029aabab100f170",
          "adult": false,
          "gender": 1,
          "id": 3041001,
          "known_for_department": "Directing",
          "name": "Stephanie Gonzaga",
          "original_name": "Stephanie Gonzaga",
          "popularity": 0.2536,
          "profile_path": null
        }
      ],
      "guest_stars": [
        {
          "character": "Additional Voices (voice)",
          "credit_id": "6544b7aefd4f80013ce7dbcd",
          "order": 522,
          "adult": false,
          "gender": 1,
          "id": 1226797,
          "known_for_department": "Acting",
          "name": "Nyima Funk",
          "original_name": "Nyima Funk",
          "popularity": 0.509,
          "profile_path": "/rx7rt8E0chx3rwoici36IJPmN7W.jpg"
        },
        {
          "character": "Additional Voices (voice)",
          "credit_id": "6544b7c49d6e3306c88ecb76",
          "order": 523,
          "adult": false,
          "gender": 2,
          "id": 1422233,
          "known_for_department": "Acting",
          "name": "Dan Navarro",
          "original_name": "Dan Navarro",
          "popularity": 0.4967,
          "profile_path": "/8QN7jNDU5PahZ29tH4a7XOyWkWZ.jpg"
        },
        {
          "character": "Additional Voices (voice)",
          "credit_id": "6544b7cc6beaea012c8d4b02",
          "order": 524,
          "adult": false,
          "gender": 1,
          "id": 1171640,
          "known_for_department": "Acting",
          "name": "Ami Shukla",
          "original_name": "Ami Shukla",
          "popularity": 0.2469,
          "profile_path": "/e8HhshT5p9CDeVV6TZVY4YJGpV0.jpg"
        },
        {
          "character": "Paul (voice)",
          "credit_id": "654ddfab29383543f0b60655",
          "order": 528,
          "adult": false,
          "gender": 2,
          "id": 7248,
          "known_for_department": "Acting",
          "name": "Cliff Curtis",
          "original_name": "Cliff Curtis",
          "popularity": 2.7922,
          "profile_path": "/dfaElGoyJWseFWxXwEMLL9WTi7V.jpg"
        },
        {
          "character": "Black Samson (voice)",
          "credit_id": "6552c643d4fe0400ac35051d",
          "order": 541,
          "adult": false,
          "gender": 2,
          "id": 65640,
          "known_for_department": "Acting",
          "name": "Khary Payton",
          "original_name": "Khary Payton",
          "popularity": 1.3872,
          "profile_path": "/4PgEGuAb2KkaRb7P9PdK40pPeVH.jpg"
        },
        {
          "character": "Donald / Isotope (voice)",
          "credit_id": "6552c73afd6fa1011bc47c12",
          "order": 543,
          "adult": false,
          "gender": 2,
          "id": 1217648,
          "known_for_department": "Acting",
          "name": "Chris Diamantopoulos",
          "original_name": "Chris Diamantopoulos",
          "popularity": 1.6808,
          "profile_path": "/oenBtpk0RTId4wacQKYU4cPcq8Z.jpg"
        },
        {
          "character": "Bulletproof (voice)",
          "credit_id": "6552c9f2ea84c71093ff3ae1",
          "order": 550,
          "adult": false,
          "gender": 2,
          "id": 1099717,
          "known_for_department": "Acting",
          "name": "Jay Pharoah",
          "original_name": "Jay Pharoah",
          "popularity": 1.2414,
          "profile_path": "/qpCc7SshxYXcgZIjhv8xKWuzEp6.jpg"
        },
        {
          "character": "Shapesmith (voice)",
          "credit_id": "65573b4253866e0139e2f3ba",
          "order": 558,
          "adult": false,
          "gender": 2,
          "id": 222121,
          "known_for_department": "Acting",
          "name": "Ben Schwartz",
          "original_name": "Ben Schwartz",
          "popularity": 2.6228,
          "profile_path": "/hWEQe66jXUAGVhbU5dy8s0IrrAQ.jpg"
        },
        {
          "character": "Cecil (voice)",
          "credit_id": "65aeba726af8f8010c96c966",
          "order": 568,
          "adult": false,
          "gender": 2,
          "id": 27740,
          "known_for_department": "Acting",
          "name": "Walton Goggins",
          "original_name": "Walton Goggins",
          "popularity": 5.0205,
          "profile_path": "/5lcVMJbWrNDFiWa1WxK4oR8zwev.jpg"
        },
        {
          "character": "Eve (voice)",
          "credit_id": "65aebaa9aad9c200ca5a13e1",
          "order": 572,
          "adult": false,
          "gender": 1,
          "id": 94098,
          "known_for_department": "Acting",
          "name": "Gillian Jacobs",
          "original_name": "Gillian Jacobs",
          "popularity": 2.1631,
          "profile_path": "/9fGHBU38slGZ6aOdwLgvrVNwCV5.jpg"
        },
        {
          "character": "Machine Head (voice)",
          "credit_id": "65fffca97f6c8d017c71ece4",
          "order": 625,
          "adult": false,
          "gender": 2,
          "id": 52886,
          "known_for_department": "Acting",
          "name": "Jeffrey Donovan",
          "original_name": "Jeffrey Donovan",
          "popularity": 2.7839,
          "profile_path": "/wlDXfXpu6Uz32LUmbFzU8QPDoQH.jpg"
        },
        {
          "character": "Mr. Liu (voice)",
          "credit_id": "67a5de2c5088b945972ff7c6",
          "order": 675,
          "adult": false,
          "gender": 2,
          "id": 21629,
          "known_for_department": "Acting",
          "name": "Tzi Ma",
          "original_name": "Tzi Ma",
          "popularity": 1.9381,
          "profile_path": "/x4fz0LCIiBNGdil3nBYO22W7QJ0.jpg"
        },
        {
          "character": "Titan (voice)",
          "credit_id": "67a5ded74d536cb93266df02",
          "order": 681,
          "adult": false,
          "gender": 2,
          "id": 176762,
          "known_for_department": "Acting",
          "name": "Todd Williams",
          "original_name": "Todd Williams",
          "popularity": 1.1367,
          "profile_path": "/uLdgH4w3wT348vdgUE06kSMizlZ.jpg"
        },
        {
          "character": "Fiona (voice)",
          "credit_id": "67b700a29f7fb2a743656a50",
          "order": 697,
          "adult": false,
          "gender": 1,
          "id": 3412706,
          "known_for_department": "Acting",
          "name": "Somali Rose",
          "original_name": "Somali Rose",
          "popularity": 0.4562,
          "profile_path": "/ocKk7Sbhrhx2zeR2ldTpA20NSvx.jpg"
        },
        {
          "character": "Brit (voice)",
          "credit_id": "67c95f11ef9a90cdba24a631",
          "order": 707,
          "adult": false,
          "gender": 2,
          "id": 783,
          "known_for_department": "Acting",
          "name": "Jonathan Banks",
          "original_name": "Jonathan Banks",
          "popularity": 4.2179,
          "profile_path": "/bswk26L13PvY4iMTwUTAsepXCLv.jpg"
        },
        {
          "character": "Rex / Robot (voice)",
          "credit_id": "69bb8e1559fd3bdf98a9848e",
          "order": 731,
          "adult": false,
          "gender": 2,
          "id": 555249,
          "known_for_department": "Acting",
          "name": "Ross Marquand",
          "original_name": "Ross Marquand",
          "popularity": 1.4799,
          "profile_path": "/2CxkVPimin0c2v7fUK3MGjgEnLt.jpg"
        },
        {
          "character": "Additional Voices (voice)",
          "credit_id": "69bb8e3282babb958aa984d2",
          "order": 732,
          "adult": false,
          "gender": 2,
          "id": 4354816,
          "known_for_department": "Acting",
          "name": "Bobby Kesselman",
          "original_name": "Bobby Kesselman",
          "popularity": 0.243,
          "profile_path": null
        },
        {
          "character": "DA Sinclair / Magnattack / Male Security (voice)",
          "credit_id": "69bb91e2d53b9ae3de3b99e7",
          "order": 744,
          "adult": false,
          "gender": 2,
          "id": 89599,
          "known_for_department": "Acting",
          "name": "Eric Bauza",
          "original_name": "Eric Bauza",
          "popularity": 1.6065,
          "profile_path": "/afOlsVPQxbtkom604MeCemjlwEV.jpg"
        },
        {
          "character": "Vanessa (voice)",
          "credit_id": "69bb91f1aa55d78748aafb24",
          "order": 745,
          "adult": false,
          "gender": 1,
          "id": 1381399,
          "known_for_department": "Acting",
          "name": "Nicole Byer",
          "original_name": "Nicole Byer",
          "popularity": 1.1215,
          "profile_path": "/5eDmmwAumgWzlfT50gf5KpL54E9.jpg"
        },
        {
          "character": "Oliver / Young Omni Man (voice)",
          "credit_id": "69bb91fe65b9ebc1212c8cca",
          "order": 746,
          "adult": false,
          "gender": 2,
          "id": 1721268,
          "known_for_department": "Acting",
          "name": "Christian Convery",
          "original_name": "Christian Convery",
          "popularity": 3.1244,
          "profile_path": "/tOR2tSrvHPVDltE4jBDEva3GNqY.jpg"
        },
        {
          "character": "Amanda / Daphne / Female Security (voice)",
          "credit_id": "69bb9219902d9fdd800526a1",
          "order": 747,
          "adult": false,
          "gender": 1,
          "id": 15761,
          "known_for_department": "Acting",
          "name": "Grey DeLisle",
          "original_name": "Grey DeLisle",
          "popularity": 3.0491,
          "profile_path": "/vrUHaXe1pG56yZkgH7Hs3LGRLTT.jpg"
        },
        {
          "character": "Monster Girl (voice)",
          "credit_id": "69bb926d4335cdd74e57d70d",
          "order": 748,
          "adult": false,
          "gender": 2,
          "id": 24362,
          "known_for_department": "Acting",
          "name": "Kevin Michael Richardson",
          "original_name": "Kevin Michael Richardson",
          "popularity": 2.6524,
          "profile_path": "/xXt9Nh7RAT5bOen66TaXreNYmCl.jpg"
        },
        {
          "character": "Additional Voices (voice)",
          "credit_id": "69bb92971dea1a1c6500f1eb",
          "order": 749,
          "adult": false,
          "gender": 2,
          "id": 23680,
          "known_for_department": "Acting",
          "name": "Dee Bradley Baker",
          "original_name": "Dee Bradley Baker",
          "popularity": 3.7288,
          "profile_path": "/9oFnToDZWp0I484s7Ua1EzNQQ2m.jpg"
        }
      ]
    },
    {
      "air_date": "2026-03-25",
      "episode_number": 4,
      "episode_type": "standard",
      "id": 6951279,
      "name": "HURM",
      "overview": "Hurm.",
      "production_code": "INVI 404",
      "runtime": 56,
      "season_number": 4,
      "show_id": 95557,
      "still_path": "/jAgbFn1AEBxgUksM1mHuaEBDmAS.jpg",
      "vote_average": 6.4,
      "vote_count": 11,
      "crew": [
        {
          "job": "Writer",
          "department": "Writing",
          "credit_id": "605d4bae7c6de3006c5c6715",
          "adult": false,
          "gender": 2,
          "id": 1223867,
          "known_for_department": "Writing",
          "name": "Robert Kirkman",
          "original_name": "Robert Kirkman",
          "popularity": 1.0762,
          "profile_path": "/ulYOkxtk8lUvg4Ltkg2q22ibg4R.jpg"
        },
        {
          "job": "Director",
          "department": "Directing",
          "credit_id": "654de2b729383543f295e83f",
          "adult": false,
          "gender": 2,
          "id": 3907784,
          "known_for_department": "Art",
          "name": "Ian Abando",
          "original_name": "Ian Abando",
          "popularity": 0.2971,
          "profile_path": "/kTl7x51FXs7ab2kTMPjBbPZMPRN.jpg"
        }
      ],
      "guest_stars": [
        {
          "character": "Art (voice)",
          "credit_id": "6552c489fd6fa100e1e43a45",
          "order": 537,
          "adult": false,
          "gender": 2,
          "id": 2,
          "known_for_department": "Acting",
          "name": "Mark Hamill",
          "original_name": "Mark Hamill",
          "popularity": 4.7435,
          "profile_path": "/zMQ93JTLW8KxusKhOlHFZhih3YQ.jpg"
        },
        {
          "character": "Eve (voice)",
          "credit_id": "65aebaa9aad9c200ca5a13e1",
          "order": 572,
          "adult": false,
          "gender": 1,
          "id": 94098,
          "known_for_department": "Acting",
          "name": "Gillian Jacobs",
          "original_name": "Gillian Jacobs",
          "popularity": 2.1631,
          "profile_path": "/9fGHBU38slGZ6aOdwLgvrVNwCV5.jpg"
        },
        {
          "character": "Riley (voice)",
          "credit_id": "660e5f569c97bd0163a548cc",
          "order": 642,
          "adult": false,
          "gender": 1,
          "id": 1181303,
          "known_for_department": "Acting",
          "name": "Chloe Bennet",
          "original_name": "Chloe Bennet",
          "popularity": 2.1151,
          "profile_path": "/4qvbabAnuLBEY1K262pn8sMHtVw.jpg"
        },
        {
          "character": "Oliver (voice)",
          "credit_id": "67a5af42470bb75ff266fd8a",
          "order": 652,
          "adult": false,
          "gender": 2,
          "id": 1721268,
          "known_for_department": "Acting",
          "name": "Christian Convery",
          "original_name": "Christian Convery",
          "popularity": 3.1244,
          "profile_path": "/tOR2tSrvHPVDltE4jBDEva3GNqY.jpg"
        },
        {
          "character": "Damien / Ka-Har (voice)",
          "credit_id": "69c61a22a39c7e86a6ad8ae2",
          "order": 751,
          "adult": false,
          "gender": 2,
          "id": 6574,
          "known_for_department": "Acting",
          "name": "Clancy Brown",
          "original_name": "Clancy Brown",
          "popularity": 5.0628,
          "profile_path": "/1JeBRNG7VS7r64V9lOvej9bZXW5.jpg"
        },
        {
          "character": "Satan (voice)",
          "credit_id": "69c61a293fb01bd49308a862",
          "order": 752,
          "adult": false,
          "gender": 2,
          "id": 11357,
          "known_for_department": "Acting",
          "name": "Bruce Campbell",
          "original_name": "Bruce Campbell",
          "popularity": 2.8911,
          "profile_path": "/p9335ljr7luOWsfwZSOlsIzFJKE.jpg"
        },
        {
          "character": "William (voice)",
          "credit_id": "69c61a4ba39c7e86a6ad8ae6",
          "order": 753,
          "adult": false,
          "gender": 2,
          "id": 1561268,
          "known_for_department": "Acting",
          "name": "Brandon Scott Jones",
          "original_name": "Brandon Scott Jones",
          "popularity": 1.0749,
          "profile_path": "/lgw6q8nuBLDet1VUIEbuS5FX9eJ.jpg"
        },
        {
          "character": "Domina (voice)",
          "credit_id": "69c61a53440b14e48fc62f21",
          "order": 754,
          "adult": false,
          "gender": 1,
          "id": 35317,
          "known_for_department": "Acting",
          "name": "Kate Mulgrew",
          "original_name": "Kate Mulgrew",
          "popularity": 2.2439,
          "profile_path": "/cikUr2PEluEamVsLgrnWWLx9ZsI.jpg"
        },
        {
          "character": "Volcanikka (voice)",
          "credit_id": "69c61a6b2bfa08bf7908a946",
          "order": 755,
          "adult": false,
          "gender": 1,
          "id": 30430,
          "known_for_department": "Acting",
          "name": "Indira Varma",
          "original_name": "Indira Varma",
          "popularity": 4.4877,
          "profile_path": "/yaFCI907dcK2XkzO0HQgtK25kp2.jpg"
        },
        {
          "character": "Additional Voices (voice)",
          "credit_id": "69c61a7707b96f27dd08a885",
          "order": 756,
          "adult": false,
          "gender": 1,
          "id": 81663,
          "known_for_department": "Acting",
          "name": "Vanessa Marshall",
          "original_name": "Vanessa Marshall",
          "popularity": 1.1028,
          "profile_path": "/yZsWfaiOxaN5MZkWIKPbxz1KKS1.jpg"
        },
        {
          "character": "Additional Voices (voice)",
          "credit_id": "69c61a816b3f208aecafd1f2",
          "order": 757,
          "adult": false,
          "gender": 2,
          "id": 80823,
          "known_for_department": "Acting",
          "name": "Andrew Morgado",
          "original_name": "Andrew Morgado",
          "popularity": 0.8801,
          "profile_path": null
        }
      ]
    },
    {
      "air_date": "2026-04-01",
      "episode_number": 5,
      "episode_type": "standard",
      "id": 6951280,
      "name": "GIVE US A MOMENT",
      "overview": "Mark embarks on a new and dangerous mission, throwing Debbie into a tailspin and plunging Eve into uncertainty.",
      "production_code": "",
      "runtime": 51,
      "season_number": 4,
      "show_id": 95557,
      "still_path": "/zbCcDf2fVUlutvArKJtH1yiMZWC.jpg",
      "vote_average": 8.028,
      "vote_count": 18,
      "crew": [
        {
          "job": "Writer",
          "department": "Writing",
          "credit_id": "605d4bae7c6de3006c5c6715",
          "adult": false,
          "gender": 2,
          "id": 1223867,
          "known_for_department": "Writing",
          "name": "Robert Kirkman",
          "original_name": "Robert Kirkman",
          "popularity": 1.0762,
          "profile_path": "/ulYOkxtk8lUvg4Ltkg2q22ibg4R.jpg"
        },
        {
          "job": "Director",
          "department": "Directing",
          "credit_id": "6544b6156beaea014b66d702",
          "adult": false,
          "gender": 2,
          "id": 1896377,
          "known_for_department": "Directing",
          "name": "Sol Choi",
          "original_name": "Sol Choi",
          "popularity": 0.5399,
          "profile_path": "/n69OtJPQIowcNek8EvRzYPPlhpS.jpg"
        }
      ],
      "guest_stars": []
    },
    {
      "air_date": "2026-04-08",
      "episode_number": 6,
      "episode_type": "standard",
      "id": 6951281,
      "name": "YOU LOOK HORRIBLE",
      "overview": "Family bonds are put to the test. Under pressure, Allen makes a new friend.",
      "production_code": "",
      "runtime": null,
      "season_number": 4,
      "show_id": 95557,
      "still_path": "/k7Z18kQXUbVy7Q9M42qOqGhVuTs.jpg",
      "vote_average": 0,
      "vote_count": 0,
      "crew": [],
      "guest_stars": []
    },
    {
      "air_date": "2026-04-15",
      "episode_number": 7,
      "episode_type": "standard",
      "id": 6951282,
      "name": "DON'T DO ANYTHING RASH",
      "overview": "Nothing goes according to plan during a massive confrontation.",
      "production_code": "",
      "runtime": null,
      "season_number": 4,
      "show_id": 95557,
      "still_path": "/vEyYNzrfpLCefYhILeUmdBcLp0M.jpg",
      "vote_average": 0,
      "vote_count": 0,
      "crew": [],
      "guest_stars": []
    },
    {
      "air_date": "2026-04-22",
      "episode_number": 8,
      "episode_type": "finale",
      "id": 6951284,
      "name": "DON'T LEAVE ME HANGING HERE",
      "overview": "Mark confronts his darkest fears as his life changes forever.",
      "production_code": "",
      "runtime": null,
      "season_number": 4,
      "show_id": 95557,
      "still_path": "/a103TuPbdItnmw4d4yDFQngJywu.jpg",
      "vote_average": 0,
      "vote_count": 0,
      "crew": [],
      "guest_stars": []
    }
  ],
  "name": "Season 4",
  "networks": [
    {
      "id": 1024,
      "logo_path": "/w7HfLNm9CWwRmAMU58udl2L7We7.png",
      "name": "Prime Video",
      "origin_country": ""
    }
  ],
  "overview": "While the world recovers from the global catastrophe of last season, a changed Mark struggles with guilt as he fights to protect his home and the people he loves, setting him on a collision course with a powerful new threat that could alter the fate of humanity forever.",
  "id": 480006,
  "poster_path": "/4tblBrslcKSifMVZ3TmtT2ukMor.jpg",
  "season_number": 4,
  "vote_average": 7.4
}
```