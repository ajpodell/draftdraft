from dataclasses import dataclass


@dataclass
class RowData:
    num_teams: int
    starting_row: int

ROWS = [
    RowData(
        num_teams=8,
        starting_row=4,
    ),
    RowData(
        num_teams=9,
        starting_row=13,
    )
]
TOTAL_TEAMS = 17
PICKS_PER_TEAM = 6
STARTING_COLUMN = 'A'
ENDING_COLUMN = 'Y'
SPACE_BETWEEN_TEAMS = 3

ROW_1_NUM_TEAMS = 8
ROW_2_NUM_TEAMS = 9

class CellPrinter:
    def __init__(self, pick_num):
        self.pick_num = pick_num

    def get_team_starting_row(self):
        ''' return 0 if its one of the first 8 teams in a forward round or first 9 in reversed round, else the other '''
        # forward rounds
        if not self.is_reversed_round:
            if self.pick_within_round < ROW_1_NUM_TEAMS:
                return ROWS[0].starting_row
            else:
                return ROWS[1].starting_row
        # reversed rounds
        else:
            if self.pick_within_round < ROW_2_NUM_TEAMS:
                return ROWS[1].starting_row
            else:
                return ROWS[0].starting_row
                    
    def get_cell_row(self):
        return self.get_team_starting_row() + self.round_num

    def get_column(self):
        # forward rounds
        team_in_row = self.pick_within_round
        if not self.is_reversed_round:
            if team_in_row >= ROW_1_NUM_TEAMS:
                team_in_row -= ROWS[0].num_teams

            return chr(ord(STARTING_COLUMN) + (team_in_row * SPACE_BETWEEN_TEAMS))

        # reversed rounds
        # remember there is an extra box in the second row
        else:
            if team_in_row >= ROW_2_NUM_TEAMS:
                # were in first row
                # doing 1 less than 9 so that we have an extra row considered -- this ends up just being the first row
                # TODO: can actually make padding configurable
                team_in_row -= ROWS[0].num_teams

            return chr( ord(ENDING_COLUMN) - (team_in_row * SPACE_BETWEEN_TEAMS) )

    @property
    def pick_within_round(self):
        return self.pick_num % TOTAL_TEAMS

    @property
    def is_reversed_round(self):
        return self.round_num % 2 == 1

    @property
    def round_num(self):
        return int(self.pick_num / TOTAL_TEAMS)

    def print_data(self):
        cell_format = f'={self.get_column()}{self.get_cell_row()}'
        print(cell_format)


for i in range(TOTAL_TEAMS * PICKS_PER_TEAM):
    CellPrinter(i).print_data()
