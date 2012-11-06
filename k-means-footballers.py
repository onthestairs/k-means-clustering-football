import csv
import random

all_stats = ("Date","Player ID","Player Surname","Player Forename","Team","Team Id","Opposition","Opposition id","Venue","Position Id","Appearances","Time Played","Starts","Substitute On","Substitute Off","Goals","First Goal","Winning Goal","Shots On Target inc goals","Shots Off Target inc woodwork","Blocked Shots","Penalties Taken","Penalty Goals","Penalties Saved","Penalties Off Target","Penalties Not Scored","Direct Free-kick Goals","Direct Free-kick On Target","Direct Free-kick Off Target","Blocked Direct Free-kick","Goals from Inside Box","Shots On from Inside Box","Shots Off from Inside Box","Blocked Shots from Inside Box","Goals from Outside Box","Shots On Target Outside Box","Shots Off Target Outside Box","Blocked Shots Outside Box","Headed Goals","Headed Shots On Target","Headed Shots Off Target","Headed Blocked Shots","Left Foot Goals","Left Foot Shots On Target","Left Foot Shots Off Target","Left Foot Blocked Shots","Right Foot Goals","Right Foot Shots On Target","Right Foot Shots Off Target","Right Foot Blocked Shots","Other Goals","Other Shots On Target","Other Shots Off Target","Other Blocked Shots","Shots Cleared off Line","Shots Cleared off Line Inside Area","Shots Cleared off Line Outside Area","Goals Open Play","Goals from Corners","Goals from Throws","Goals from Direct Free Kick","Goals from Set Play","Goals from penalties","Attempts Open Play on target","Attempts from Corners on target","Attempts from Throws on target","Attempts from Direct Free Kick on target","Attempts from Set Play on target","Attempts from Penalties on target","Attempts Open Play off target","Attempts from Corners off target","Attempts from Throws off target","Attempts from Direct Free Kick off target","Attempts from Set Play off target","Attempts from Penalties off target","Goals as a substitute","Total Successful Passes All","Total Unsuccessful Passes All","Assists","Key Passes","Total Successful Passes Excl Crosses Corners","Total Unsuccessful Passes Excl Crosses Corners","Successful Passes Own Half","Unsuccessful Passes Own Half","Successful Passes Opposition Half","Unsuccessful Passes Opposition Half","Successful Passes Defensive third","Unsuccessful Passes Defensive third","Successful Passes Middle third","Unsuccessful Passes Middle third","Successful Passes Final third","Unsuccessful Passes Final third","Successful Short Passes","Unsuccessful Short Passes","Successful Long Passes","Unsuccessful Long Passes","Successful Flick-Ons","Unsuccessful Flick-Ons","Successful Crosses Corners","Unsuccessful Crosses Corners","Corners Taken incl short corners","Corners Conceded","Successful Corners into Box","Unsuccessful Corners into Box","Short Corners","Throw Ins to Own Player","Throw Ins to Opposition Player","Successful Dribbles","Unsuccessful Dribbles","Successful Crosses Corners Left","Unsuccessful Crosses Corners Left","Successful Crosses Left","Unsuccessful Crosses Left","Successful Corners Left","Unsuccessful Corners Left","Successful Crosses Corners Right","Unsuccessful Crosses Corners Right","Successful Crosses Right","Unsuccessful Crosses Right","Successful Corners Right","Unsuccessful Corners Right","Successful Long Balls","Unsuccessful Long Balls","Successful Lay-Offs","Unsuccessful Lay-Offs","Through Ball","Successful Crosses Corners in the air","Unsuccessful Crosses Corners in the air","Successful crosses in the air","Unsuccessful crosses in the air","Successful open play crosses","Unsuccessful open play crosses","Touches","Goal Assist Corner","Goal Assist Free Kick","Goal Assist Throw In","Goal Assist Goal Kick","Goal Assist Set Piece","Key Corner","Key Free Kick","Key Throw In","Key Goal Kick","Key Set Pieces","Duels won","Duels lost","Aerial Duels won","Aerial Duels lost","Ground Duels won","Ground Duels lost","Tackles Won","Tackles Lost","Last Man Tackle","Total Clearances","Headed Clearances","Other Clearances","Clearances Off the Line","Blocks","Interceptions","Recoveries","Total Fouls Conceded","Fouls Conceded exc handballs pens","Total Fouls Won","Fouls Won in Danger Area inc pens","Fouls Won not in danger area","Foul Won Penalty","Handballs Conceded","Penalties Conceded","Offsides","Yellow Cards","Red Cards","Goals Conceded","Goals Conceded Inside Box","Goals Conceded Outside Box","Saves Made","Saves Made from Inside Box","Saves Made from Outside Box","Saves from Penalty","Catches","Punches","Drops","Crosses not Claimed","GK Distribution","GK Successful Distribution","GK Unsuccessful Distribution","Clean Sheets","Team Clean sheet","Error leading to Goal","Error leading to Attempt","Challenge Lost","Shots On Conceded","Shots On Conceded Inside Box","Shots On Conceded Outside Box","Team Formation","Position in Formation","Turnovers","Dispossessed","Big Chances","Big Chances Faced","Pass Forward","Pass Backward","Pass Left","Pass Right","Unsuccessful Ball Touch","Successful Ball Touch","Take-Ons Overrun","CompId","SeasId","Touches open play final third","Touches open play opp box","Touches open play opp six yards")
meta_stats = ("Date","Player ID","Player Surname","Player Forename","Team","Team Id","Opposition","Opposition id","Venue","Position Id","Appearances","Time Played","Starts","Substitute On","Substitute Off","CompId","SeasId")
keeper_stats = ("Turnovers","Goal Assist Goal Kick","Team Clean sheet","Team Formation","Position in Formation","Goals Conceded Outside Box", "Shots On Conceded","Goals Conceded Inside Box","Crosses not Claimed","Saves Made from Outside Box","Shots On Conceded Inside Box","Saves Made from Inside Box","Shots On Conceded Outside Box","Saves from Penalty","Big Chances Faced","Drops","Key Goal Kick","Goals Conceded","Saves Made","Catches","GK Distribution","GK Successful Distribution","GK Unsuccessful Distribution","Penalties Saved","Goal Assist Goal Kick")
corner_stats = ("Successful Crosses Corners","Unsuccessful Crosses Corners","Corners Taken incl short corners","Corners Conceded","Successful Corners into Box","Unsuccessful Corners into Box","Short Corners","Successful Dribbles","Unsuccessful Dribbles","Successful Crosses Corners Left","Unsuccessful Crosses Corners Left","Successful Crosses Left","Unsuccessful Crosses Left","Successful Corners Left","Unsuccessful Corners Left","Successful Crosses Corners Right","Unsuccessful Crosses Corners Right","Successful Crosses Right","Unsuccessful Crosses Right","Successful Corners Right","Unsuccessful Corners Right","Successful Crosses Corners in the air","Unsuccessful Crosses Corners in the air","Key Corner","Goal Assist Corner")
foot_specific_stats = ("Left Foot Goals","Left Foot Shots On Target","Left Foot Shots Off Target","Left Foot Blocked Shots","Right Foot Goals","Right Foot Shots On Target","Right Foot Shots Off Target","Right Foot Blocked Shots")
penalty_stats = ("Penalties Taken","Penalty Goals","Penalties Saved","Penalties Off Target","Penalties Not Scored","Attempts from Penalties on target","Attempts from Penalties off target","Goals from penalties")
set_piece_stats = ("Direct Free-kick Goals","Direct Free-kick On Target","Direct Free-kick Off Target","Blocked Direct Free-kick", "Key Set Pieces","Key Free Kick","Goal Assist Free Kick","Goal Assist Set Piece")
throw_in_stats = ("Throw Ins to Own Player","Throw Ins to Opposition Player")
disallowed_stats = meta_stats + keeper_stats + corner_stats + foot_specific_stats + penalty_stats + set_piece_stats + throw_in_stats
allowed_stats = tuple(set(all_stats)-set(disallowed_stats))

print "ALLOWED STATS:"
print allowed_stats


class Player():

	def __init__(self, id, name, games):
		self.id = id
		self.name = name
		self.games = games
		self.games_played = len(self.games)
		self.stats = {}
		self.normalised_stats = {}
		self.calculate_stats()

	def calculate_stats(self):
		total_games = self.games_played
		#if the player has played less than 15 games, sack them off
		total_stats = {k:0 for k in self.games[0].keys()}
		for game in self.games:
			for k,v in game.items():
				total_stats[k] += v
		average_stats = {k: (float(v)/total_games) for k,v in total_stats.items()}
		self.stats = average_stats

	def calculate_normalised_stats(self, max_stats, min_stats):
		self.normalised_stats = {k: (v-min_stats[k])/(max_stats[k]-min_stats[k]) for k,v in self.stats.items() if max_stats[k] != 0}

def parse(file='stats.csv', allowed = lambda x: True):
	players = {}
	with open(file, 'rU') as csvfile:
		csvFile = csv.DictReader(csvfile, delimiter=',')
		for row in csvFile:
			if not allowed(row):
				continue
			id = row["Player ID"]
			#If we don't already have the player, set them up in the players dictionary
			if not id in players:
				players[id] = { 'name': row['Player Forename'] + ' ' + row['Player Surname'], 'games': [] }			
			game = {}
			for k,v in row.items():
				if not k in disallowed_stats:
					game[k] = int(v)
			players[id]['games'].append(game)
	player_list = []
	for id, p in players.items():
		player_object = Player(id, p['name'], p['games'])
		player_list.append(player_object)
	return player_list

def get_max_stats(players):
	max_stats = {k:0 for k in players[0].stats.keys()}
	for p in players:
		for k,v in p.stats.items():
			if v > max_stats[k]:
				max_stats[k] = v
	return max_stats

def get_min_stats(players):
	min_stats = {k:0 for k in players[0].stats.keys()}
	for p in players:
		for k,v in p.stats.items():
			if v < min_stats[k]:
				min_stats[k] = v
	return min_stats

class kmeans():

	def __init__(self, N, players, distance_function, threshold=0.01):
		self.N = N
		self.players = players
		self.distance_function = distance_function
		self.features = players[0].stats.keys()
		self.threshold = threshold
		self.calculate()

	def init_means(self):
		self.means = [p.normalised_stats for p in random.sample(self.players, self.N)]

	def calculate(self):
		self.init_means()
		old_total_distance = 10000
		new_total_distance = old_total_distance - self.threshold - 10
		count = 0
		while (old_total_distance - new_total_distance) > self.threshold:
			total = 0
			self.clusters = [[] for m in self.means]
			for p in self.players:
				#find which mean this player is closest to
				smallest = len(self.features)
				for m in enumerate(self.means):
					d = self.distance_function(p.normalised_stats, m[1])
					if d < smallest:
						smallest = d
						closest_mean = m[0]
				#add the id to the cluster
				self.clusters[closest_mean].append(p)
				total += smallest
			old_total_distance, new_total_distance = new_total_distance, total
			count = count + 1
			print "Done iteration {0}. New distance is {1}.".format(count, new_total_distance, old_total_distance)
			self.recalculate_means()
		self.final_error = new_total_distance
		self.mean_features()

	def recalculate_means(self):
		for i in range(self.N):
			new_mean = {k:0 for k in self.features}
			cluster_size = len(self.clusters[i])
			for p in self.clusters[i]:
				for k,v in p.normalised_stats.items():
					new_mean[k] += v
			new_mean = {k: (v/cluster_size) for k,v in new_mean.items()}
			self.means[i] = new_mean

	def mean_features(self):
		self.mean_features = [None for i in range(self.N)]
		for i in range(self.N):
			distances = {k: sum([(self.means[i][k] - self.means[j][k]) for j in range(self.N) if not j == i]) for k in self.features}
			self.mean_features[i] = sorted(distances.items(), key = lambda x: abs(x[1]), reverse=True)

def conjunct(props):
	if len(props) == 2:
		f, g = props
		return lambda x: (f(x)) and (g(x))
	else:
		f = props.pop()
		g = conjunct(props)
		return lambda x: (f(x)) and (g(x))

def disjunct(props):
	if len(props) == 2:
		f, g = props
		return lambda x: (f(x)) or (g(x))
	else:
		f = props.pop()
		g = disjunct(props)
		return lambda x: (f(x)) or (g(x))

#team filters
only_man_u = lambda x: (x["Team Id"] == '1')
only_man_city = lambda x: (x["Team Id"] == '43')
only_arsenal = lambda x: (x["Team Id"] == '3')
only_tottenham = lambda x: (x["Team Id"] == '6')
only_chelsea = lambda x: (x["Team Id"] == '8')
only_newcastle = lambda x: (x["Team Id"] == '4')
only_top_6 = disjunct([only_man_u, only_man_city, only_arsenal, only_chelsea, only_tottenham, only_newcastle])

#substitutes
no_substitutes = lambda x: (x["Substitute On"] == '0' and x["Substitute Off"] == '0')

#positional filters
no_keepers = lambda x: (x["Position Id"] != '1')
only_2_midfielders = lambda x: (x['Team Formation'] in ('2','3') and x['Position in Formation'] in ('4','8'))
only_3_midfielders = lambda x: (x['Team Formation'] in ('4','9') and x['Position in Formation'] in ('4','8','7')) or (x['Team Formation'] in ('5','6','7','8') and x['Position in Formation'] in ('4','8','10'))
only_midfielders = disjunct([only_2_midfielders,only_3_midfielders])
only_1_strikers = lambda x: (x['Team Formation'] in ('2','3','6') and x['Position in Formation'] in ('9','10'))
only_2_strikers = lambda x: (x['Team Formation'] in ('4','5','7','8','9') and x['Position in Formation'] in ('9'))
only_strikers = disjunct([only_1_strikers,only_2_strikers])
only_2_defenders = lambda x: (x['Team Formation'] in ('2','3','4','5','6','7','8','9') and x['Position in Formation'] in ('5','6'))

#combos
only_strikers_no_substitutes = conjunct([no_substitutes,only_strikers])
no_keepers_no_substitutes = conjunct([no_keepers, no_substitutes])
only_man_u = conjunct([only_man_u,no_keepers_no_substitutes])
only_top_6_midfielders = conjunct([only_top_6,only_midfielders,no_substitutes])


players = parse(allowed=only_top_6_midfielders)
print "parsed"

a = len(players)
players = [p for p in players if p.games_played > 5]
b = len(players)

print "Got rid of {0} players.".format(a-b)

max_stats = get_max_stats(players)
min_stats = get_min_stats(players)
print "got max, min stats"

print "poor stats"
print [k for k,v in max_stats.items() if v == 0]

for p in players:
	p.calculate_normalised_stats(max_stats, min_stats)
print "normalised the stats"


distance = lambda x,y: sum([(x[k]-y[k])**2 for k in list( set( x.keys() ).intersection( set(y.keys()) ) )])


ks = [kmeans(4,players,distance) for i in range (10)]

ks = sorted(ks, key= lambda x: x.final_error)

kmeans = ks[0]

def p_q():
	print "<h4>Salient Features</h4>"

def p_co():
	print "<h4>Comments</h4>"
	print "<p></p>"

def p_m():
	print "<h4>Players</h4>"

for i in range(len(kmeans.clusters)):
	c = kmeans.clusters[i]
	cluster_names = [p.name for p in c]
	cluster_attrs = kmeans.mean_features[i][:10]
	p_q()
	print "<p>{0}</p>".format(", ".join(['<span style="color:{1};">{0}</span>'.format(k[0],'red' if (k[1]<0) else 'green') for k in cluster_attrs]))
	p_m()
	print "<p>{0}</p>".format(", ".join(cluster_names))
	p_co()
	print "<hr />"
