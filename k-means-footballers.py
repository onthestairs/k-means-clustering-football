import csv
import random

all_stats = ("Date","Player ID","Player Surname","Player Forename","Team","Team Id","Opposition","Opposition id","Venue","Position Id","Appearances","Time Played","Starts","Substitute On","Substitute Off","Goals","First Goal","Winning Goal","Shots On Target inc goals","Shots Off Target inc woodwork","Blocked Shots","Penalties Taken","Penalty Goals","Penalties Saved","Penalties Off Target","Penalties Not Scored","Direct Free-kick Goals","Direct Free-kick On Target","Direct Free-kick Off Target","Blocked Direct Free-kick","Goals from Inside Box","Shots On from Inside Box","Shots Off from Inside Box","Blocked Shots from Inside Box","Goals from Outside Box","Shots On Target Outside Box","Shots Off Target Outside Box","Blocked Shots Outside Box","Headed Goals","Headed Shots On Target","Headed Shots Off Target","Headed Blocked Shots","Left Foot Goals","Left Foot Shots On Target","Left Foot Shots Off Target","Left Foot Blocked Shots","Right Foot Goals","Right Foot Shots On Target","Right Foot Shots Off Target","Right Foot Blocked Shots","Other Goals","Other Shots On Target","Other Shots Off Target","Other Blocked Shots","Shots Cleared off Line","Shots Cleared off Line Inside Area","Shots Cleared off Line Outside Area","Goals Open Play","Goals from Corners","Goals from Throws","Goals from Direct Free Kick","Goals from Set Play","Goals from penalties","Attempts Open Play on target","Attempts from Corners on target","Attempts from Throws on target","Attempts from Direct Free Kick on target","Attempts from Set Play on target","Attempts from Penalties on target","Attempts Open Play off target","Attempts from Corners off target","Attempts from Throws off target","Attempts from Direct Free Kick off target","Attempts from Set Play off target","Attempts from Penalties off target","Goals as a substitute","Total Successful Passes All","Total Unsuccessful Passes All","Assists","Key Passes","Total Successful Passes Excl Crosses Corners","Total Unsuccessful Passes Excl Crosses Corners","Successful Passes Own Half","Unsuccessful Passes Own Half","Successful Passes Opposition Half","Unsuccessful Passes Opposition Half","Successful Passes Defensive third","Unsuccessful Passes Defensive third","Successful Passes Middle third","Unsuccessful Passes Middle third","Successful Passes Final third","Unsuccessful Passes Final third","Successful Short Passes","Unsuccessful Short Passes","Successful Long Passes","Unsuccessful Long Passes","Successful Flick-Ons","Unsuccessful Flick-Ons","Successful Crosses Corners","Unsuccessful Crosses Corners","Corners Taken incl short corners","Corners Conceded","Successful Corners into Box","Unsuccessful Corners into Box","Short Corners","Throw Ins to Own Player","Throw Ins to Opposition Player","Successful Dribbles","Unsuccessful Dribbles","Successful Crosses Corners Left","Unsuccessful Crosses Corners Left","Successful Crosses Left","Unsuccessful Crosses Left","Successful Corners Left","Unsuccessful Corners Left","Successful Crosses Corners Right","Unsuccessful Crosses Corners Right","Successful Crosses Right","Unsuccessful Crosses Right","Successful Corners Right","Unsuccessful Corners Right","Successful Long Balls","Unsuccessful Long Balls","Successful Lay-Offs","Unsuccessful Lay-Offs","Through Ball","Successful Crosses Corners in the air","Unsuccessful Crosses Corners in the air","Successful crosses in the air","Unsuccessful crosses in the air","Successful open play crosses","Unsuccessful open play crosses","Touches","Goal Assist Corner","Goal Assist Free Kick","Goal Assist Throw In","Goal Assist Goal Kick","Goal Assist Set Piece","Key Corner","Key Free Kick","Key Throw In","Key Goal Kick","Key Set Pieces","Duels won","Duels lost","Aerial Duels won","Aerial Duels lost","Ground Duels won","Ground Duels lost","Tackles Won","Tackles Lost","Last Man Tackle","Total Clearances","Headed Clearances","Other Clearances","Clearances Off the Line","Blocks","Interceptions","Recoveries","Total Fouls Conceded","Fouls Conceded exc handballs pens","Total Fouls Won","Fouls Won in Danger Area inc pens","Fouls Won not in danger area","Foul Won Penalty","Handballs Conceded","Penalties Conceded","Offsides","Yellow Cards","Red Cards","Goals Conceded","Goals Conceded Inside Box","Goals Conceded Outside Box","Saves Made","Saves Made from Inside Box","Saves Made from Outside Box","Saves from Penalty","Catches","Punches","Drops","Crosses not Claimed","GK Distribution","GK Successful Distribution","GK Unsuccessful Distribution","Clean Sheets","Team Clean sheet","Error leading to Goal","Error leading to Attempt","Challenge Lost","Shots On Conceded","Shots On Conceded Inside Box","Shots On Conceded Outside Box","Team Formation","Position in Formation","Turnovers","Dispossessed","Big Chances","Big Chances Faced","Pass Forward","Pass Backward","Pass Left","Pass Right","Unsuccessful Ball Touch","Successful Ball Touch","Take-Ons Overrun","CompId","SeasId","Touches open play final third","Touches open play opp box","Touches open play opp six yards")
disallowed_stats = ("Date","Player ID","Player Surname","Player Forename","Team","Team Id","Opposition","Opposition id","Venue","Position Id","Appearances","Time Played","Starts","Substitute On","Substitute Off","CompId","SeasId","Turnovers","Goal Assist Goal Kick","Team Clean sheet")
allowed_stats = tuple(set(all_stats)-set(disallowed_stats))
players = {}

with open('stats.csv', 'rU') as csvfile:
	csvFile = csv.DictReader(csvfile, delimiter=',')
	for row in csvFile:
		id = row["Player ID"]
		#If we don't already have the player, set them up in the players dictionary
		if not id in players:
			players[id] = { 'name': row['Player Forename'] + ' ' + row['Player Surname'], 'games': [] }			
		game = {}
		for k,v in row.items():
			if not k in disallowed_stats:
				game[k] = int(v)
		players[id]['games'].append(game)

print "Got Data"

# for k,v in players.items():
# 	print v['name'] + ' (' + k + ')'

#get x per game for each stat x
for id, p in players.items():
	total_games = len(p['games'])
	#if the player has played less than 15 games, sack them off
	if total_games < 15:
		#print "see you later {0}".format(players[id]['name'])
		del players[id]
		continue
	total_stats = {k:0 for k in allowed_stats}
	for game in p['games']:
		for k,v in game.items():
			total_stats[k] += v
	average_stats = {k: (float(v)/total_games) for k,v in total_stats.items()}
	players[id]['stats'] = average_stats

print "CALCULATED STATS"

#print players['17476']['stats']

# we are going to be normalising the data, so things like passes aren't worth tens more than goals, so figure out the max values for each stat
max_stats = {k:0 for k in allowed_stats}
for id in players.keys():
	for k,v in players[id]['stats'].items():
		if v > max_stats[k]:
			max_stats[k] = v

for k,v in max_stats.items():
	if v == 0:
		print "THE PROBLEM IS {0}".format(k)
#print max_stats

print "CALCULATED MAX STATS"

#normalise the data

for id, p in players.items():
	players[id]['normalised_stats'] = {k: (v/max_stats[k]) for k,v in p['stats'].items()}

print "CALCULATED NORMALISED STATS"

#print players['17476']['normalised_stats']

#NOW THE K-MEANS BIT

# pretty much a euclidean metric in loads of variables
def distance(s1, s2):
	sum = 0
	for k in allowed_stats:
		#square these, cant be bothered to include maths library
		sum = sum + (s1[k] - s2[k])*(s1[k] - s2[k])
	return sum


N = 11

means = [players[k]['normalised_stats'] for k in random.sample(players.keys(), N)]

for i in range(20):
	print "Doing the {0}th iteration".format(i)
	total = 0
	clusters = [[] for m in means]
	for id, p in players.items():
		#find which mean this player is closest to
		smallest = len(allowed_stats)
		for m in enumerate(means):
			d = distance(p['normalised_stats'], m[1])
			if d < smallest:
				smallest = d
				closest_mean = m[0]
		#add the id to the cluster
		clusters[closest_mean].append(id)
		total += smallest

	print "total error on is {0}".format(total)
	#recalibrate the means
	for i in range(N):
		new_mean = {k:0 for k in allowed_stats}
		cluster_size = len(clusters[i])
		for id in clusters[i]:
			for k,v in players[id]['normalised_stats'].items():
				new_mean[k] += v
		new_mean = {k: (v/cluster_size) for k,v in new_mean.items()}
		means[i] = new_mean

for c in clusters:
	print "HERE IS A CLUSTER: "
	names = [players[id]['name'] for id in c]
	print ','.join(names)
