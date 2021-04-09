# SimELO

## cl.py

Simulate remaining games of european football leagues using clubs' ELO Rating (obtained from [clubelo.com](http://clubelo.com/), last taken 2021-03-29) 
to calculate probability of win/draw/loss of each game and record teams' final league position, as well as qualification for European competitions
and relegation. This is then used to calculate how probable each team is to qualify directly for the next year's group stage of the Champions League.


For each iteration of the simulation, the following competitions are simulated, and the following spots are awareded according to
[UEFA Access list](https://www.uefa.com/MultimediaFiles/Download/uefaorg/General/02/58/61/42/2586142_DOWNLOAD.pdf):

- Champions League: 1 spot
- Europa League: 1 spot
- La Liga: 4 spots
- Premier League: 4 spots
- Bundesliga: 4 spots
- Serie A: 4 spots
- Ligue 1: 2 spots
- Primeira Liga: 2 spots
- Russian Premier League: 1 spot
- Jupiler Pro League: 1 spot
- Ukrainian Premier League: 1 spot
- Eredivisie: 1 spot

Furthermore, according to [UEFA Champions League regulation](https://documents.uefa.com/r/Regulations-of-the-UEFA-Champions-League-2020/21/Article-3-Entries-for-the-competition-Online), in case the Champions League winner or the Europa League winner have already qualified throught their country,
their spots in the group stage are given as such:

- The Champions League winner spot is given to the winner of the 11th ranked association (Turkey).
- The Europa League winner spot is given to the third-placed team of the 5th ranked association (France).

There is another rule that stops one association from having more than 5 teams in the group stage, which would happen if the winner of CL and EL are from the same country
(which already has 4 spots) and both do not qualify through the league. In that case, the 4rd ranked team is sent to the Europa League instead.
However, I was not able to find how the spot from that team would be awarded, so I did not implement the "no more than 5 clubs from the same country" rule.
For reference, this seems to occur in 1%-2% of the simulations.

You can find the results of 1 million simulation [here](cl_groups.json). Results may vary wildly between simulations.

## pt.py

Simulate remaining games of Liga NOS in the same way, but record teams' final positions, as well as which team qualified for each European competition
and which teams are relegated. Also simulates the Portuguese Cup and the Champions League, to correctly calculated European spots.
Data for Champions League and Liga NOS was last taken at 2021-04-06.