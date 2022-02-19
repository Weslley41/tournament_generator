def brackets_len(count_teams, len=2):
	"""
	Check len of brackets and add teams 'None' if necessary.
	...
	Parameters:
		(int) count_teams: count of teams

	Returns:
		(int) len: len of brackets
	"""	
	if (count_teams > len):
		return brackets_len(count_teams, len * 2)
	else:
		return len
