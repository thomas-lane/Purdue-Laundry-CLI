import click
import requests

def get_laundry_dictionary():
    return requests.get('https://laundry-api.sigapp.club/v2/location/all').json()

def get_laundry_status(place=None):
    """Returns a tuple containing place name, available, in use, almost done, end of cycle"""
    in_use = "In use"
    available = "Available"
    almost_done = "Almost done"
    end_of_cycle = "End of cycle"

    laundry_dictionary = get_laundry_dictionary()

    places = list()

    for value in laundry_dictionary:
        if place != None and place not in value:
            continue

        total_washers_in_use = 0
        total_washers_available = 0
        total_washers_almost_done = 0
        total_washers_end_of_cycle = 0

        total_washers = 0

        total_dryers_in_use = 0
        total_dryers_available = 0
        total_dryers_almost_done = 0
        total_dryers_end_of_cycle = 0

        total_dryers = 0

        for dict in laundry_dictionary[value]:
            if dict["status"] == available:
                if dict["type"] == "Washer":
                    total_washers_available += 1
                    total_washers += 1
                elif dict["type"] == "Dryer":
                    total_dryers_available += 1
                    total_dryers += 1
            elif dict["status"] == in_use:
                if dict["type"] == "Washer":
                    total_washers_in_use += 1
                    total_washers += 1
                elif dict["type"] == "Dryer":
                    total_dryers_in_use += 1
                    total_dryers += 1
            elif dict["status"] == almost_done:
                if dict["type"] == "Washer":
                    total_washers_almost_done += 1
                    total_washers += 1
                elif dict["type"] == "Dryer":
                    total_dryers_almost_done += 1
                    total_dryers += 1
            elif dict["status"] == end_of_cycle:
                if dict["type"] == "Washer":
                    total_washers_end_of_cycle += 1
                    total_washers += 1
                elif dict["type"] == "Dryer":
                    total_dryers_end_of_cycle += 1
                    total_dryers += 1
        
        places.append((value, (total_washers_available, total_washers_in_use, total_washers_almost_done, total_washers_end_of_cycle, total_washers), \
            (total_dryers_available, total_dryers_in_use, total_dryers_almost_done, total_dryers_end_of_cycle, total_dryers)))

    return places

def print_width(toPrint, width, color = None):
    click.echo(click.style(toPrint, fg=color), nl=False)

    click.echo(" " * (width - len(toPrint)), nl=False)


@click.command()
@click.option('--room', default=None, help='Room to view available laundry machines from.')
def laundry(room):
    """Displays the status of the laundry machines at Purdue University."""

    click.echo('=======================================================')
    click.echo('    Laundry Machines Available at Purdue University    ')
    click.echo('=======================================================')
    click.echo()

    status = get_laundry_status(room)

    if len(status) == 0:
        click.echo(click.style("No rooms found", fg='red'))
    else:
        click.echo('Room                                    W       D      ')
        click.echo('-------------------------------------------------------')
    
        for place in status:
            print_width(place[0], 40, 'green')
            print_width(str(place[1][0]) + '/' + str(place[1][4]), 8)
            print_width(str(place[2][0]) + '/' + str(place[2][4]), 8)
            click.echo()

if __name__ == "__main__":
    laundry(None)
