"""
knowledge_base.py
Static sports analytics knowledge base grounded in real expert sources.
Every entry traces to the source listed in its metadata.
"""

KNOWLEDGE_BASE = [

    # ──────────────────────────────────────────────────────────────────────────
    # CATEGORY 1: advanced_metrics
    # Source: Basketball Reference Glossary (basketball-reference.com/about/glossary.html)
    # Source: Dean Oliver "Basketball on Paper" (2004) via public references
    # ──────────────────────────────────────────────────────────────────────────

    {
        "content": (
            "Box Plus/Minus (BPM) is a box score estimate of points per 100 possessions a player "
            "contributed above a league-average player, translated to an average team. It is available "
            "since the 1973-74 NBA season. A BPM of 0.0 represents a league-average player. Elite "
            "players typically post BPM above +4.0, MVP-caliber seasons above +7.0, and historically "
            "great seasons above +10.0. Unlike plus/minus, BPM attempts to isolate individual "
            "contribution using only box score statistics without requiring lineup data."
        ),
        "metadata": {
            "category": "advanced_metrics",
            "topic": "BPM (Box Plus/Minus)",
            "source": "Basketball Reference Glossary",
            "source_url": "https://www.basketball-reference.com/about/glossary.html",
        },
    },

    {
        "content": (
            "True Shooting Percentage (TS%) measures shooting efficiency taking into account field "
            "goals, 3-point field goals, and free throws. The formula is PTS / (2 * TSA) where "
            "TSA = FGA + 0.44 * FTA. The 0.44 multiplier accounts for the fact that not all free "
            "throw trips result in two attempts (technical fouls, and-ones). League average TS% "
            "hovers around 56-58%. A TS% above 60% is considered elite shooting efficiency. It is "
            "superior to FG% because it accounts for the added value of three-pointers and free "
            "throws, making it the preferred shooting efficiency metric for modern analysts."
        ),
        "metadata": {
            "category": "advanced_metrics",
            "topic": "True Shooting Percentage (TS%)",
            "source": "Basketball Reference Glossary",
            "source_url": "https://www.basketball-reference.com/about/glossary.html",
        },
    },

    {
        "content": (
            "Usage Percentage (USG%) estimates the percentage of team plays used by a player while "
            "on the floor. The formula is 100 * ((FGA + 0.44 * FTA + TOV) * (Team MP / 5)) / "
            "(MP * (Team FGA + 0.44 * Team FTA + Team TOV)). A USG% of 20% is roughly league "
            "average. Primary scorers typically post USG% between 25-30%. Players above 30% usage "
            "are carrying an unusually high offensive load. High usage does not guarantee high "
            "efficiency — the relationship between usage and efficiency reveals whether a player "
            "can maintain their shooting quality under increased offensive responsibility."
        ),
        "metadata": {
            "category": "advanced_metrics",
            "topic": "Usage Rate (USG%)",
            "source": "Basketball Reference Glossary",
            "source_url": "https://www.basketball-reference.com/about/glossary.html",
        },
    },

    {
        "content": (
            "Player Efficiency Rating (PER) was developed by ESPN columnist John Hollinger and sums "
            "up all a player's positive accomplishments, subtracts the negative accomplishments, and "
            "returns a per-minute rating of performance. The league average is always set to 15.0 by "
            "definition. A PER above 20.0 represents an All-Star level player. A PER above 25.0 is "
            "MVP territory. A PER above 30.0 has historically only been achieved by the greatest "
            "individual seasons in NBA history. PER is useful for quick comparisons but has known "
            "weaknesses in measuring defensive contributions and can be inflated by high usage even "
            "when inefficient."
        ),
        "metadata": {
            "category": "advanced_metrics",
            "topic": "PER (Player Efficiency Rating)",
            "source": "Basketball Reference Glossary, John Hollinger ESPN",
            "source_url": "https://www.basketball-reference.com/about/glossary.html",
        },
    },

    {
        "content": (
            "Win Shares (WS) is a player statistic that attempts to divvy up credit for team wins "
            "to individual players. It comes in offensive (OWS) and defensive (DWS) components. "
            "A full season of roughly 10+ Win Shares is typically associated with MVP-level "
            "performance. Win Shares credit players for both individual efficiency and their team's "
            "overall performance, meaning a very good player on a bad team may accumulate fewer Win "
            "Shares than their individual talent warrants. It is calculated using the full methodology "
            "described in Basketball on Paper by Dean Oliver."
        ),
        "metadata": {
            "category": "advanced_metrics",
            "topic": "Win Shares (WS)",
            "source": "Basketball Reference Glossary, Dean Oliver Basketball on Paper",
            "source_url": "https://www.basketball-reference.com/about/glossary.html",
        },
    },

    {
        "content": (
            "Value Over Replacement Player (VORP) is a box score estimate of the points per 100 "
            "TEAM possessions that a player contributed above a replacement-level player (-2.0), "
            "translated to an average team and prorated to an 82-game season. A positive VORP "
            "indicates a player better than replacement level. VORP above 3.0 represents a solid "
            "starter. VORP above 6.0 is All-NBA caliber. VORP is available since the 1973-74 season "
            "and is one of the cleaner metrics for comparing players across different eras because "
            "it adjusts for pace and league context."
        ),
        "metadata": {
            "category": "advanced_metrics",
            "topic": "VORP (Value Over Replacement Player)",
            "source": "Basketball Reference Glossary",
            "source_url": "https://www.basketball-reference.com/about/glossary.html",
        },
    },

    {
        "content": (
            "Offensive Rating (ORtg) measures points scored per 100 possessions for teams, and "
            "points produced per 100 possessions for individual players. Defensive Rating (DRtg) "
            "measures points allowed per 100 possessions. Both were developed by Dean Oliver in "
            "Basketball on Paper. For teams, a net rating (ORtg minus DRtg) above +5 is playoff "
            "contender level. A net rating above +8 represents a championship contender. A net "
            "rating above +10 or +11 historically correlates with 60+ win seasons. For individual "
            "players, ORtg and DRtg reflect the team's performance when that player is on the floor."
        ),
        "metadata": {
            "category": "advanced_metrics",
            "topic": "Offensive and Defensive Rating (ORtg / DRtg)",
            "source": "Basketball Reference Glossary, Dean Oliver Basketball on Paper",
            "source_url": "https://www.basketball-reference.com/about/glossary.html",
        },
    },

    {
        "content": (
            "Pace Factor estimates the number of possessions per 48 minutes by a team. The formula "
            "is 48 * ((Team Poss + Opp Poss) / (2 * (Team MP / 5))). The NBA average pace in the "
            "early 2000s was around 90-92 possessions per 48 minutes. The pace-and-space revolution "
            "pushed the average toward 99-102 by the late 2010s. Pace matters for statistical "
            "comparison because players on faster teams accumulate more counting stats simply due "
            "to more possessions. All serious player and team comparisons should use per-possession "
            "or per-100-possession metrics to control for pace differences."
        ),
        "metadata": {
            "category": "advanced_metrics",
            "topic": "Pace Factor",
            "source": "Basketball Reference Glossary",
            "source_url": "https://www.basketball-reference.com/about/glossary.html",
        },
    },

    {
        "content": (
            "Effective Field Goal Percentage (eFG%) adjusts for the fact that a 3-point field goal "
            "is worth one more point than a 2-point field goal. The formula is (FG + 0.5 * 3P) / FGA. "
            "If Player A goes 4-for-10 with 2 threes and Player B goes 5-for-10 with no threes, both "
            "score 10 points from field goals and have the same eFG% of 50% — revealing that "
            "traditional FG% would misleadingly favor Player B. eFG% is one of Dean Oliver's Four "
            "Factors and the single most important determinant of offensive success in the NBA, "
            "carrying approximately 40% of the explanatory weight for team winning percentage."
        ),
        "metadata": {
            "category": "advanced_metrics",
            "topic": "Effective Field Goal Percentage (eFG%)",
            "source": "Basketball Reference Glossary, Dean Oliver Four Factors",
            "source_url": "https://www.basketball-reference.com/about/glossary.html",
        },
    },

    {
        "content": (
            "Assist Percentage (AST%) estimates the percentage of teammate field goals a player "
            "assisted while on the floor. The formula is 100 * AST / (((MP / (Team MP / 5)) * "
            "Team FG) - FG). A true pass-first point guard typically posts AST% above 35%. A "
            "playmaking big man posting AST% above 20% is considered exceptional. AST% is more "
            "meaningful than raw assist totals because it controls for minutes played and team "
            "context — a player on a team with poor shooters will naturally accumulate fewer "
            "assists regardless of their passing ability."
        ),
        "metadata": {
            "category": "advanced_metrics",
            "topic": "Assist Percentage (AST%)",
            "source": "Basketball Reference Glossary",
            "source_url": "https://www.basketball-reference.com/about/glossary.html",
        },
    },

    # ──────────────────────────────────────────────────────────────────────────
    # CATEGORY 2: four_factors_framework
    # Source: Dean Oliver "Basketball on Paper" (2004)
    # Source: Jacobs 2017, Teramoto and Cross 2010
    # Source: nbastuffer.com/analytics101/four-factors
    # Source: athletepath.com/four-factors-calculator
    # ──────────────────────────────────────────────────────────────────────────

    {
        "content": (
            "Dean Oliver's Four Factors framework, introduced in Basketball on Paper (2004), "
            "identifies the four statistical categories most responsible for winning basketball "
            "games: Effective Field Goal Percentage (eFG%), Turnover Percentage (TOV%), Offensive "
            "Rebound Percentage (ORB%), and Free Throw Rate (FTR). Together these four metrics "
            "explain approximately 96% of the variance in team wins, making them arguably the most "
            "powerful predictive framework in basketball analytics. Oliver assigned relative weights: "
            "eFG% carries 40% of importance, TOV% 25%, ORB% 20%, FTR 15%. Modern regression "
            "analyses by Jacobs (2017) suggest updated weights closer to 46% for eFG%, 35% for "
            "TOV%, 12% for ORB%, and 7% for FTR, indicating shooting and ball security are even "
            "more dominant than originally estimated."
        ),
        "metadata": {
            "category": "four_factors_framework",
            "topic": "Four Factors Overview",
            "source": "Dean Oliver Basketball on Paper, athletepath.com, arxiv.org",
            "source_url": "https://www.athletepath.com/four-factors-calculator/",
        },
    },

    {
        "content": (
            "The shooting factor is the single most important determinant of offensive success, "
            "accounting for approximately 40-46% of winning probability. It is measured using "
            "Effective Field Goal Percentage: (FG + 0.5 * 3P) / FGA. The formula weights "
            "three-pointers at 1.5x field goals to reflect their additional value. Teams that rank "
            "in the top 10 in eFG% are nearly always top-10 offenses. The rise of three-point "
            "shooting since 2012 is fundamentally a story about eFG% optimization — teams realized "
            "that a 35% three-point shooter has the same eFG% as a 52.5% two-point shooter, and "
            "began allocating shots accordingly."
        ),
        "metadata": {
            "category": "four_factors_framework",
            "topic": "Shooting Factor (eFG%)",
            "source": "Dean Oliver Basketball on Paper, Basketball Reference",
            "source_url": "https://www.nbastuffer.com/analytics101/four-factors/",
        },
    },

    {
        "content": (
            "Turnover Percentage measures turnovers per 100 possessions: TOV / (FGA + 0.44 * FTA "
            "+ TOV). It accounts for approximately 25-35% of winning probability. Elite offensive "
            "teams typically post TOV% below 13%. A TOV% above 17% is damaging to any offense "
            "regardless of shooting efficiency. Turnovers are doubly costly — they deny the offense "
            "a scoring opportunity AND give the opponent an extra possession. In the Four Factors "
            "framework, each turnover eliminated is worth approximately 1.3 points per game in "
            "terms of net rating impact."
        ),
        "metadata": {
            "category": "four_factors_framework",
            "topic": "Turnover Factor (TOV%)",
            "source": "Dean Oliver Basketball on Paper, multiple regression analyses",
            "source_url": "https://www.nbastuffer.com/analytics101/four-factors/",
        },
    },

    {
        "content": (
            "Offensive Rebound Percentage measures offensive rebounds relative to available "
            "offensive rebounds: ORB / (ORB + Opponent DRB). It carries approximately 12-20% of "
            "winning probability. Elite offensive rebounding teams can generate 3-5 additional "
            "points per game through second-chance opportunities. However, offensive rebounding "
            "involves a significant trade-off: crashing the offensive glass means fewer defenders "
            "back in transition, making teams vulnerable to fast breaks. This is why "
            "analytically-driven teams increasingly accept lower ORB% in exchange for better "
            "transition defense, unless they have exceptional rim-running bigs who create easy "
            "offensive rebound opportunities."
        ),
        "metadata": {
            "category": "four_factors_framework",
            "topic": "Rebounding Factor (ORB%)",
            "source": "Dean Oliver Basketball on Paper",
            "source_url": "https://www.nbastuffer.com/analytics101/four-factors/",
        },
    },

    {
        "content": (
            "Free Throw Rate measures FT / FGA — both how often a team gets to the line and how "
            "often they convert. It carries approximately 7-15% of winning probability. An FTR "
            "above 0.30 indicates a team that actively attacks the basket and earns free throws "
            "regularly. Free throws are one of the most efficient scoring opportunities in "
            "basketball, estimated at roughly 1.1 points per trip to the line. However, the free "
            "throw factor has decreased in predictive importance in the modern NBA as three-point "
            "shooting has become more dominant. Teams now increasingly accept lower free throw "
            "rates in exchange for more three-point attempts."
        ),
        "metadata": {
            "category": "four_factors_framework",
            "topic": "Free Throw Factor (FTR)",
            "source": "Dean Oliver Basketball on Paper, modern regression studies",
            "source_url": "https://www.athletepath.com/four-factors-calculator/",
        },
    },

    # ──────────────────────────────────────────────────────────────────────────
    # CATEGORY 3: defensive_systems
    # Source: Ben Falk, Cleaning the Glass (cleaningtheglass.com)
    # Ben Falk was VP of Basketball Strategy for Philadelphia 76ers and
    # Basketball Analytics Manager for Portland Trail Blazers
    # ──────────────────────────────────────────────────────────────────────────

    {
        "content": (
            "NBA halfcourt defense operates on a simple framework: the offense works to create an "
            "advantage through dribble penetration, screens, or mismatches, and the defense works "
            "to prevent that advantage from forming and to neutralize it when it does. The first "
            "line of individual defense is preventing the ballhandler from gaining an advantage — "
            "if the ballhandler gets past their defender, help must arrive. Help defense opens up "
            "a teammate, requiring further rotation. This chain of advantage-creation and "
            "neutralization defines the entire halfcourt defensive sequence."
        ),
        "metadata": {
            "category": "defensive_systems",
            "topic": "Core Framework of NBA Defense",
            "source": "Ben Falk, Cleaning the Glass",
            "source_url": "https://cleaningtheglass.com/",
        },
    },

    {
        "content": (
            "When a ballhandler beats their defender, a teammate must provide help to prevent a "
            "layup. This help, however, creates an open teammate that the offense can attack. Good "
            "teams then help the helper through a second rotation. NBA defensive systems have "
            "converged on three core principles: help should come from the weak side (not the "
            "strong side), defenders should not help from the strong side corner because corner "
            "threes are too valuable to leave open, and the first line of rim protection should "
            "come from the low man — the weak side defender closest to the basket. These principles "
            "were identified by Ben Falk through his work inside NBA organizations."
        ),
        "metadata": {
            "category": "defensive_systems",
            "topic": "Help Defense Principles",
            "source": "Ben Falk, Cleaning the Glass",
            "source_url": "https://cleaningtheglass.com/",
        },
    },

    {
        "content": (
            "A closeout occurs when a defender rushes to contest a perimeter player who has "
            "received the ball. Against shooters, defenders use hard closeouts — sprinting close "
            "to the shooter's body to prevent any clean look, accepting the risk of being driven "
            "past. Against non-shooters, defenders use short closeouts — stopping further from the "
            "player to prioritize staying in front of any drive. The fly-by closeout (running past "
            "the shooter to force them inside the three-point line) became popular as corner threes "
            "increased in value, but skilled shooters counter with pump fakes. Closeout quality is "
            "one of the most important metrics in evaluating team defensive execution."
        ),
        "metadata": {
            "category": "defensive_systems",
            "topic": "Closeout Philosophy",
            "source": "Ben Falk, Cleaning the Glass",
            "source_url": "https://cleaningtheglass.com/",
        },
    },

    {
        "content": (
            "NBA coaches are reluctant to have players fully help from the strong side corner "
            "because corner threes are the highest-value shot in basketball — they are closer to "
            "the basket than non-corner threes and worth the same three points. Leaving a shooter "
            "in the strong side corner to stop a drive trades a high-difficulty two against a "
            "wide-open three, which is almost always a bad tradeoff. This is a departure from "
            "college and high school basketball where corner threes are not disproportionately "
            "valuable. Understanding this principle explains why modern NBA defenses allow drives "
            "more willingly when the alternative is leaving shooters in corners."
        ),
        "metadata": {
            "category": "defensive_systems",
            "topic": "Strong Side Corner Rule",
            "source": "Ben Falk, Cleaning the Glass",
            "source_url": "https://cleaningtheglass.com/",
        },
    },

    {
        "content": (
            "After help arrives at the rim and the ball is kicked out, a second rotation must "
            "close out on the open player. If the offense passes again, a third rotation is "
            "required. Each successive rotation opens a player further from the ball, and by the "
            "third pass, the defense is typically scrambling. Great offenses — those with multiple "
            "reliable shooters and a skilled passer at the hub — are specifically designed to force "
            "these third and fourth rotations until a breakdown occurs. This is why player spacing "
            "and the ability to make decisions under pressure are the primary offensive skills in "
            "modern NBA design."
        ),
        "metadata": {
            "category": "defensive_systems",
            "topic": "Rotation Chains and Their Limits",
            "source": "Ben Falk, Cleaning the Glass",
            "source_url": "https://cleaningtheglass.com/",
        },
    },

    # ──────────────────────────────────────────────────────────────────────────
    # CATEGORY 4: lineup_construction
    # Source: Ben Falk "Size Matters" — Cleaning the Glass
    # (cleaningtheglass.com/size-matters)
    # ──────────────────────────────────────────────────────────────────────────

    {
        "content": (
            "Ben Falk's analysis of 5 years of NBA lineup data categorized lineups as Big (two "
            "traditional big men), Small (undersized power forward), or Spread (larger PF who "
            "shoots threes). Over this period, Big lineups scored 106.1 points per 100 possessions "
            "while allowing 106.1 on defense. Small lineups scored 107.9 but allowed 108.8. Spread "
            "lineups scored 108.7 while allowing 107.4. This reveals the core tradeoff: bigger "
            "lineups sacrifice offense for defense, while smaller lineups gain offensive efficiency "
            "but give back defensive effectiveness. The sweet spot — spread bigs who can shoot "
            "threes and defend — is the most valuable and rarest roster asset."
        ),
        "metadata": {
            "category": "lineup_construction",
            "topic": "Big vs Small vs Spread Lineup Tradeoffs",
            "source": "Ben Falk, Cleaning the Glass — Size Matters",
            "source_url": "https://cleaningtheglass.com/size-matters/",
        },
    },

    {
        "content": (
            "Teams flee the midrange shot because long twos have lower expected value than either "
            "rim attempts or three-pointers. However, teams that force midrange shots on defense "
            "often play big lineups — the same lineups that tend to take midrange shots on offense. "
            "The Spurs exemplified this paradox: they led the league in midrange shots forced "
            "defensively while also leading the league in midrange shots attempted offensively. "
            "Going analytically pure on offense (eliminating midrange) typically requires a roster "
            "configuration that is defensively vulnerable on the glass. Teams optimize one end at "
            "the expense of the other."
        ),
        "metadata": {
            "category": "lineup_construction",
            "topic": "Midrange Trade-Off in Team Construction",
            "source": "Ben Falk, Cleaning the Glass",
            "source_url": "https://cleaningtheglass.com/size-matters/",
        },
    },

    {
        "content": (
            "Between 2007-2011 and 2012-2017, the percentage of possessions played with Big "
            "lineups dropped by 16 percentage points, all of which shifted to Spread lineups — "
            "not Small lineups. The NBA did not go small so much as it made big men shoot threes. "
            "Big men who previously took 60% of their shots in long midrange were gradually pushed "
            "beyond the arc. A stretch big who can hit threes at league-average efficiency while "
            "maintaining physicality against traditional bigs represents a genuine positional "
            "advantage — providing spacing without sacrificing size. This transformation "
            "fundamentally reshaped NBA roster construction and draft evaluation."
        ),
        "metadata": {
            "category": "lineup_construction",
            "topic": "Rise of the Spread Big",
            "source": "Ben Falk, Cleaning the Glass — Size Matters",
            "source_url": "https://cleaningtheglass.com/size-matters/",
        },
    },

    # ──────────────────────────────────────────────────────────────────────────
    # CATEGORY 5: analytics_history
    # Source: nbastuffer.com analytics movement guide
    # Source: Dean Oliver Basketball on Paper 2004
    # Source: Public documentation of SportVU and Second Spectrum integration
    # ──────────────────────────────────────────────────────────────────────────

    {
        "content": (
            "Dean Oliver is to NBA analytics what Bill James is to baseball. His 2004 book "
            "Basketball on Paper introduced possession-based statistics and the Four Factors "
            "framework to the basketball community. Before this work, NBA analytics departments "
            "were minimal and focused on basic box score data. Oliver introduced the concept that "
            "basketball efficiency should be measured per possession rather than per game, because "
            "teams playing at different paces are not directly comparable using counting stats. "
            "His framework became the foundation for virtually all modern NBA statistical analysis."
        ),
        "metadata": {
            "category": "analytics_history",
            "topic": "Analytics Revolution Origins",
            "source": "nbastuffer.com, Dean Oliver Basketball on Paper",
            "source_url": "https://www.nbastuffer.com/analytics101/",
        },
    },

    {
        "content": (
            "In 2010-11, four NBA teams installed SportVU cameras that captured positioning data "
            "for all 10 players, 3 referees, and the ball 25 times per second. By 2013-14 the NBA "
            "mandated these cameras in every arena, becoming the first major American sports league "
            "to use player tracking in every game. This data explosion shifted team analytics "
            "departments from statisticians to data scientists and machine learning engineers. "
            "Starting in 2017-18 the NBA switched to Second Spectrum, which added computer vision "
            "and NLP to automatically classify plays and generate insights in real time from "
            "broadcast footage."
        ),
        "metadata": {
            "category": "analytics_history",
            "topic": "Video Tracking Era (SportVU and Second Spectrum)",
            "source": "nbastuffer.com analytics movement",
            "source_url": "https://www.nbastuffer.com/analytics101/",
        },
    },

    {
        "content": (
            "The Houston Rockets under Daryl Morey systematically pursued a shot quality "
            "philosophy: take only shots with the highest expected value — layups, dunks, and "
            "three-pointers — while eliminating the low-value long two. This approach, dubbed "
            "Moreyball, was based on the mathematical reality that a 35% three-point shooter is "
            "as efficient as a 52.5% midrange shooter. The Rockets dragged the rest of the NBA "
            "toward this philosophy through competitive pressure. Three-point attempt rates have "
            "risen every season since 2012, fundamentally altering offensive design, defensive "
            "positioning, and the types of players teams prioritize in the draft."
        ),
        "metadata": {
            "category": "analytics_history",
            "topic": "Moreyball and the Three-Point Revolution",
            "source": "nbastuffer.com analytics movement",
            "source_url": "https://www.nbastuffer.com/analytics101/",
        },
    },

    {
        "content": (
            "Pat Riley was utilizing custom analytics metrics as early as 1991, charting Knicks "
            "players on closeouts, boxouts, charges taken, and player efficacy — metrics that the "
            "broader basketball world would not adopt for another decade. This demonstrates that "
            "analytically-minded basketball thinking predates the formal analytics movement. The "
            "difference after 2004 was the democratization of these methods through public "
            "research, open data, and eventually league-wide tracking infrastructure. According to "
            "Chris Herring's analysis, Riley's early work represents one of the earliest examples "
            "of NBA teams building systematic analytical frameworks around individual player "
            "behaviors."
        ),
        "metadata": {
            "category": "analytics_history",
            "topic": "Pat Riley and Early Analytics",
            "source": "nbastuffer.com, Chris Herring ReWind Space",
            "source_url": "https://www.nbastuffer.com/analytics101/",
        },
    },

    # ──────────────────────────────────────────────────────────────────────────
    # CATEGORY 6: scoring_and_shot_quality
    # Source: Shot quality analytics consensus, Basketball Reference
    # Source: Ben Falk, Cleaning the Glass
    # ──────────────────────────────────────────────────────────────────────────

    {
        "content": (
            "Modern NBA shot quality analysis ranks shot types by expected points per attempt. "
            "Dunks and layups at the rim generate approximately 1.3-1.4 points per attempt. "
            "Corner threes generate approximately 1.05-1.15 points per attempt (closer distance "
            "than above-the-break threes). Above-the-break threes generate 1.0-1.05 points per "
            "attempt at league-average rates. Long two-point shots (midrange) generate only "
            "0.75-0.85 points per attempt — the lowest expected value shot in the game. This "
            "hierarchy is why analytically-driven teams systematically eliminate midrange shots "
            "from their offensive systems."
        ),
        "metadata": {
            "category": "scoring_and_shot_quality",
            "topic": "Shot Quality Hierarchy",
            "source": "Shot quality analytics consensus, Basketball Reference",
            "source_url": "https://www.basketball-reference.com/about/glossary.html",
        },
    },

    {
        "content": (
            "Corner three-pointers are worth approximately 5-7% more per attempt than "
            "above-the-break threes because they are 1.75 feet closer to the basket (22 feet vs "
            "23 feet 9 inches), yet both count as three points. This geometric advantage makes the "
            "corner three the most efficient non-layup shot in basketball. Teams specifically "
            "design offensive systems to generate corner threes through drive-and-kick actions. "
            "Defenders are instructed never to fully leave the strong side corner because a "
            "wide-open corner three is a catastrophic defensive mistake — it represents a "
            "high-probability three-point attempt with no defensive pressure."
        ),
        "metadata": {
            "category": "scoring_and_shot_quality",
            "topic": "The Corner Three Advantage",
            "source": "NBA shot analytics, Ben Falk Cleaning the Glass",
            "source_url": "https://cleaningtheglass.com/",
        },
    },

    {
        "content": (
            "There is a well-documented inverse relationship between usage rate and shooting "
            "efficiency: as a player's usage rate increases, their efficiency tends to decline "
            "because they are taking progressively harder shots under tighter defense. Elite "
            "players like LeBron James, Kevin Durant, and Stephen Curry are exceptional precisely "
            "because they maintain high efficiency at extremely high usage rates. A player posting "
            "28%+ usage at 60%+ TS% is performing at an exceptionally rare level. Most players "
            "show significant efficiency decline above 25% usage, which is why distributed "
            "offensive systems that maintain multiple moderate-usage scoring options often "
            "outperform single-star-dominated systems."
        ),
        "metadata": {
            "category": "scoring_and_shot_quality",
            "topic": "Usage-Efficiency Curve",
            "source": "Basketball analytics research consensus",
            "source_url": "https://www.basketball-reference.com/about/glossary.html",
        },
    },
]
