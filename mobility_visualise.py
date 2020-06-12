import datetime
import tkinter
import json
import time

START_DATE = datetime.datetime.strptime('15/02/2020', '%d/%m/%Y')
# Need to update END_DATE if you are updating the mobility.json file with recent data
END_DATE = datetime.datetime.strptime('07/06/2020', '%d/%m/%Y')
N_DAYS = END_DATE - START_DATE + datetime.timedelta(days=1)
MAX_PERC_CHG = 100
MIN_PERC_CHG = -100
DEFINITIONS = json.load(open('definitions.json'))

# related to drawing
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
X_AXIS_OFFSET = 100
Y_AXIS_OFFSET = 100

X_INCREMENT = (CANVAS_WIDTH - 2 * Y_AXIS_OFFSET) / N_DAYS.days
Y_INCREMENT = (CANVAS_HEIGHT - 2 * X_AXIS_OFFSET) / (MAX_PERC_CHG - MIN_PERC_CHG)

"""
Assumes that the mobility.json stores values in the format where each date is a dictionary from 
country name to country data. Example below:
{
    "2020-02-15": 
        {"United Arab Emirates": 
            {"retail_and_recreation_percent_change_from_baseline": "0", 
            "grocery_and_pharmacy_percent_change_from_baseline": "4", 
            "parks_percent_change_from_baseline": "5", 
            "transit_stations_percent_change_from_baseline": "0", 
            "workplaces_percent_change_from_baseline": "2", 
            "residential_percent_change_from_baseline": "1"},
        "Afghanistan": {},
        ...
        },
    "2020-02-16":
        {...
        }
and so on.
"""


def main():
    # get the data from .json file we created using mobility_build.py
    data = json.load(open('mobility.json'))
    # Prompt user to enter a country to show the plots for
    track_country = input("Input country to track: ")

    # Create canvas
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Mobility')
    plot_date = START_DATE
    keys = list(data[str(plot_date.date())][track_country].keys())

    # Iterate over the data fields and plot daily change in visits over baseline for each field
    for key in keys:
        clear_entire_canvas(canvas)
        set_up_canvas_background(canvas, key, track_country)
        # Initiate a dict to store previous coordinate point of a plot to be able to draw a line between plot points
        prev_coord = {}
        plot_date = START_DATE

        while plot_date <= END_DATE:
            # Reset the top right date counter on the canvas
            reset_refresh_tags(canvas)
            # Start the top right date counter on the canvas
            draw_date_text(canvas, plot_date)
            # Pass slice of data that we need to plot and plot the data
            data_slice = data[str(plot_date.date())][track_country][key]
            plot_data(canvas, data_slice, plot_date, prev_coord)
            # Increment the plot date by 1
            plot_date += datetime.timedelta(days=1)

            # animate
            canvas.update()
            time.sleep(1 / 20)
        # pause after one complete plot is done
        time.sleep(1)

    canvas.mainloop()


# Plot the data slice received e.g. data["2020-02-15"]["India"]["retail_and_recreation_percent_change_from_baseline"]
# by drawing an oval at the corresponding x, y coordinate and draw a line connecting it to the previous drawn plot
def plot_data(canvas, data_slice, plot_date, prev_coord):
    # Calculate x and y coordinates for the plots
    x_delta = (plot_date - START_DATE).days
    x = Y_AXIS_OFFSET + x_delta * X_INCREMENT

    y_delta = int(data_slice)

    if y_delta > 0:
        y = max((CANVAS_HEIGHT // 2) - y_delta * Y_INCREMENT, (CANVAS_HEIGHT // 2) - MAX_PERC_CHG * Y_INCREMENT)
    else:
        y = min((CANVAS_HEIGHT // 2) - y_delta * Y_INCREMENT, (CANVAS_HEIGHT // 2) - MIN_PERC_CHG * Y_INCREMENT)

    canvas.create_oval(x, y, x + 1.5, y + 1.5, fill='red', outline='')

    if x_delta == 0:
        prev_coord['x'] = x
        prev_coord['y'] = y
    else:
        canvas.create_line(prev_coord['x'], prev_coord['y'], x, y, fill='red', width=4)
        prev_coord['x'] = x
        prev_coord['y'] = y


# Delete entire canvas
def clear_entire_canvas(canvas):
    canvas.delete('all')


# Delete blocks with to_refresh tag
def reset_refresh_tags(canvas):
    canvas.delete('to_refresh')


# Display date of the data that is being plotted currently on the top right of the graph
def draw_date_text(canvas, date_obj):
    x = CANVAS_WIDTH - Y_AXIS_OFFSET - 50
    y = X_AXIS_OFFSET + 25
    date_txt = str(date_obj.day) + ' ' + str(datetime.datetime.strftime(date_obj, '%b'))
    canvas.create_text(x, y, anchor='c', font='Helvetica 18 bold', text=date_txt, tags='to_refresh')


# Function to set-up the canvas background
def set_up_canvas_background(canvas, key, track_country):
    draw_x_axis(canvas)
    draw_y_axis(canvas)
    draw_gridlines(canvas)
    draw_header(canvas, key, track_country)
    draw_footer(canvas)


# Draw the x axis taking into account the axis offset values
def draw_x_axis(canvas):
    y = CANVAS_HEIGHT - X_AXIS_OFFSET
    x1 = Y_AXIS_OFFSET
    x2 = CANVAS_WIDTH - Y_AXIS_OFFSET
    canvas.create_line(x1, y, x2, y, width=2)

    # Draw the x-axis label
    label_y = y + (X_AXIS_OFFSET / 2)
    x_axis_txt = "Date"
    canvas.create_text(CANVAS_WIDTH / 2, label_y, anchor='c', font='Helvetica 18 bold', text=x_axis_txt)

    draw_x_axis_points(canvas)


# Draw the x-axis start and end point labels
# TODO: This is a mess. Need to convert this into an iterable loop.
def draw_x_axis_points(canvas):
    x_axis_start_txt = str(START_DATE.day) + ' ' + str(datetime.datetime.strftime(START_DATE, '%b'))
    # x_axis_end_txt = str(END_DATE.day) + ' ' + str(datetime.datetime.strftime(END_DATE, '%b'))

    march = datetime.datetime.strptime('01/03/2020', '%d/%m/%Y')
    april = datetime.datetime.strptime('01/04/2020', '%d/%m/%Y')
    may = datetime.datetime.strptime('01/05/2020', '%d/%m/%Y')
    june = datetime.datetime.strptime('01/06/2020', '%d/%m/%Y')

    x_axis_march_txt = str(march.day) + ' ' + str(datetime.datetime.strftime(march, '%b'))
    x_axis_april_txt = str(april.day) + ' ' + str(datetime.datetime.strftime(april, '%b'))
    x_axis_may_txt = str(may.day) + ' ' + str(datetime.datetime.strftime(may, '%b'))
    x_axis_june_txt = str(june.day) + ' ' + str(datetime.datetime.strftime(june, '%b'))

    y = CANVAS_HEIGHT - (X_AXIS_OFFSET * 3 / 4)
    x_feb = Y_AXIS_OFFSET
    x_mar = x_feb + (march - START_DATE).days * X_INCREMENT
    x_apr = x_feb + (april - START_DATE).days * X_INCREMENT
    x_may = x_feb + (may - START_DATE).days * X_INCREMENT
    x_june = x_feb + (june - START_DATE).days * X_INCREMENT
    canvas.create_text(x_feb + 20, y, anchor='c', font='Helvetica 14', text=x_axis_start_txt)
    canvas.create_text(x_mar, y, anchor='c', font='Helvetica 14', text=x_axis_march_txt)
    canvas.create_text(x_apr, y, anchor='c', font='Helvetica 14', text=x_axis_april_txt)
    canvas.create_text(x_may, y, anchor='c', font='Helvetica 14', text=x_axis_may_txt)
    canvas.create_text(x_june, y, anchor='c', font='Helvetica 14', text=x_axis_june_txt)


# Draw the y axis taking into account the axis offset values
def draw_y_axis(canvas):
    x = Y_AXIS_OFFSET
    y1 = X_AXIS_OFFSET
    y2 = CANVAS_HEIGHT - X_AXIS_OFFSET
    canvas.create_line(x, y1, x, y2, width=2)

    # Draw the y-axis label
    label_x = Y_AXIS_OFFSET/4
    y_axis_txt = "% change in visits"
    canvas.create_text(label_x, 300, anchor='c', font='Helvetica 18 bold', text=y_axis_txt, angle=90)


# Draw grid lines and their labels so users can easily read the graph
def draw_gridlines(canvas):

    # Define starting and end coordinates
    y_start = X_AXIS_OFFSET
    y_end = CANVAS_HEIGHT - X_AXIS_OFFSET
    x1 = Y_AXIS_OFFSET
    x2 = CANVAS_WIDTH - Y_AXIS_OFFSET

    # Set how many grid lines you want and calculate increments for the Y axis
    grid_lines = 8
    increment = (y_end - y_start) / grid_lines

    # Leave out the first and last lines and iterate over the rest of them
    for i in range(1, grid_lines):
        # Increment the Y coordinate by i times from the starting point
        y_line = y_start + i * increment

        # If grid_line is at the centre, make the color black and add a 'Baseline' label
        # else, draw a dashed line
        if i == (grid_lines / 2):
            canvas.create_line(x1, y_line, x2, y_line, fill='black', width=1)
            canvas.create_text(x2 - 30, y_line - 10, anchor='c', font='Helvetica 14', text="Baseline", fill='dark grey')
        else:
            canvas.create_line(x1, y_line, x2, y_line, fill='#D3D3D3', dash=(4, 4), width=1)

        # Add percentage labels against the grid lines
        percent = int(MAX_PERC_CHG - (((MAX_PERC_CHG - MIN_PERC_CHG) / grid_lines) * i))
        perc_text = str(percent) + '%'
        canvas.create_text(x1 - 20, y_line, anchor='c', font='Helvetica 14', text=perc_text, fill='dark grey')


# Draw header to show the country the data is being displayed for and the context around the plot
def draw_header(canvas, key, track_country):
    # Pull out h1 and h2 descriptions of each plot
    h1_text = DEFINITIONS[key]['h1']
    h2_text = DEFINITIONS[key]['h2']

    canvas.create_text(Y_AXIS_OFFSET, X_AXIS_OFFSET * 0.6, anchor='nw', font='Helvetica 18 bold', text=h1_text)
    canvas.create_text(Y_AXIS_OFFSET, X_AXIS_OFFSET * 0.8, anchor='nw', font='Helvetica 14', text=h2_text)
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, X_AXIS_OFFSET/2, fill='light yellow', outline='')
    x_head = CANVAS_WIDTH / 2
    y_head = X_AXIS_OFFSET / 4
    canvas.create_text(x_head, y_head, font='Helvetica 18 bold', text='Mobility trends - ' + track_country)


# Draw the footer to display attributions
def draw_footer(canvas):
    text_1 = 'Source: Google LLC "Google COVID-19 Community Mobility Reports". ' \
             'https://www.google.com/covid19/mobility/ Accessed: 12 June 2020.'
    text_2 = 'Visualisation by: Pramod R'

    x = CANVAS_WIDTH / 2
    y1 = CANVAS_HEIGHT - X_AXIS_OFFSET / 5
    y2 = CANVAS_HEIGHT - X_AXIS_OFFSET / 12
    canvas.create_text(x, y1, anchor='c', font='Helvetica 10', text=text_1, fill='grey')
    canvas.create_text(x, y2, anchor='c', font='Helvetica 10', text=text_2, fill='grey')


# Helper function to create a canvas
def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas


if __name__ == '__main__':
    main()
