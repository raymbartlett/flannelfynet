"""Code for generating the scorecard given by the ShareResults button."""
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image, ImageDraw, ImageFont
matplotlib.use('Agg')


def generate_bar_chart(labels, values):
    """Generate the bar chart for scores distribution on the scorecard."""
    fig = plt.figure(facecolor='black')
    plt.set_loglevel('WARNING')
    axes = fig.add_axes([.06, .06, .94, .94])

    # colors
    axes.set_facecolor('black')
    axes.spines['left'].set_color('#f1ef80')
    axes.spines['bottom'].set_color('#f1ef80')
    axes.tick_params(axis='x', colors='#f1ef80')
    axes.tick_params(axis='y', colors='#f1ef80')

    axes.bar(labels, values, color = '#f1ef80')

    fig.canvas.draw()
    return Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())


def generate_card(score_path, labels, values, general, average):
    """Compile multiple elements into a scorecard."""
    background = Image.new('RGB', (1080, 1920), (241, 239, 128))
    foreground = Image.new('RGB', ((background.width - 100), (background.height - 100)), (0, 0, 0))

    # paste message to foreground
    message_font = ImageFont.truetype('static/fonts/league_gothic.ttf', 50)
    draw = ImageDraw.Draw(foreground)
    message_offset = ((foreground.width - draw.textlength('find your fantano score', font=message_font)) // 2, foreground.height - 130)
    draw.text(message_offset, 'find your fantano score', fill=(241, 239, 128), font=message_font)

    # paste link to foreground
    link_font = ImageFont.truetype('static/fonts/league_gothic.ttf', 50)
    draw = ImageDraw.Draw(foreground)
    link_offset = ((foreground.width - draw.textlength('flannelfy.net', font=link_font)) // 2, foreground.height - 75)
    draw.text(link_offset, 'flannelfy.net', fill=(241, 239, 128), font=link_font)

    # resize score png to leave left and right buffers
    score_png = Image.open('static/scores/' + score_path)
    MAX_SIZE = (foreground.width - 100, 1920)
    score_png.thumbnail(MAX_SIZE)

    # paste score to foreground
    score_offset = ((foreground.width - score_png.width) // 2, 0)
    foreground.paste(score_png, score_offset, mask=score_png)

    # paste general info to foreground
    general_font = ImageFont.truetype('static/fonts/league_gothic.ttf', 38)
    draw = ImageDraw.Draw(foreground)
    general_offset = ((foreground.width - draw.textlength(general, font=general_font)) // 2, score_png.height)
    draw.text(general_offset, general, fill=(241, 239, 128), font=general_font)

    # paste average score to foreground
    average_font = ImageFont.truetype('static/fonts/league_gothic.ttf', 60)
    draw = ImageDraw.Draw(foreground)
    average_text = 'average score: ' + str(average)
    average_offset = ((foreground.width - draw.textlength(average_text, font=average_font)) // 2, score_png.height + 75)
    draw.text(average_offset, average_text, fill=(241, 239, 128), font=average_font)

    # paste bar chart to foreground
    bar_chart = generate_bar_chart(labels, values)
    bar_chart_offset = ((foreground.width - bar_chart.width) // 2, score_png.height + 250)
    foreground.paste(bar_chart, bar_chart_offset)

    # paste foreground to background
    foreground_offset = ((background.width - foreground.width) // 2, (background.height - foreground.height) // 2)
    background.paste(foreground, foreground_offset)

    data = io.BytesIO()
    background.save(data, 'JPEG')
    encoded_img_data = base64.b64encode(data.getvalue())
    return encoded_img_data
