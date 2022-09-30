"""Code for generating the scorecard given by the ShareResults button."""
import io
import base64
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")


def generate_bar_chart(labels, values):
    """Generate the bar chart for scores distribution on the scorecard."""
    fig = plt.figure(facecolor='black')
    plt.set_loglevel('WARNING')
    ax = fig.add_axes([.06, .06, .94, .94])

    # colors
    ax.set_facecolor('black')
    ax.spines['left'].set_color('#f1ef80')
    ax.spines['bottom'].set_color('#f1ef80')
    ax.tick_params(axis='x', colors='#f1ef80')
    ax.tick_params(axis='y', colors='#f1ef80')

    ax.bar(labels, values, color=('#f1ef80'))

    fig.canvas.draw()
    return Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())


def generate_card(score_path, labels, values, general, average):
    """Compile multiple elements into a scorecard."""
    bg = Image.new('RGB', (1080, 1920), (241, 239, 128))
    fg = Image.new('RGB', ((bg.width - 100), (bg.height - 100)), (0, 0, 0))

    # paste message to foreground
    message_font = ImageFont.truetype('static/fonts/league_gothic.ttf', 50)
    draw = ImageDraw.Draw(fg)
    message_offset = ((fg.width - draw.textlength('find your fantano score', font=message_font)) // 2, fg.height - 130)
    draw.text(message_offset, 'find your fantano score', fill=(241, 239, 128), font=message_font)

    # paste link to foreground
    link_font = ImageFont.truetype('static/fonts/league_gothic.ttf', 50)
    draw = ImageDraw.Draw(fg)
    link_offset = ((fg.width - draw.textlength('flannelfy.net', font=link_font)) // 2, fg.height - 75)
    draw.text(link_offset, 'flannelfy.net', fill=(241, 239, 128), font=link_font)

    # resize score png to leave left and right buffers
    score_png = Image.open("static/scores/" + score_path)
    MAX_SIZE = (fg.width - 100, 1920)
    score_png.thumbnail(MAX_SIZE)

    # paste score to foreground
    score_offset = ((fg.width - score_png.width) // 2, 0)
    fg.paste(score_png, score_offset, mask=score_png)

    # paste general info to foreground
    general_font = ImageFont.truetype('static/fonts/league_gothic.ttf', 38)
    draw = ImageDraw.Draw(fg)
    general_offset = ((fg.width - draw.textlength(general, font=general_font)) // 2, score_png.height)
    draw.text(general_offset, general, fill=(241, 239, 128), font=general_font)

    # paste average score to foreground
    average_font = ImageFont.truetype('static/fonts/league_gothic.ttf', 60)
    draw = ImageDraw.Draw(fg)
    average_text = 'average score: ' + str(average)
    average_offset = ((fg.width - draw.textlength(average_text, font=average_font)) // 2, score_png.height + 75)
    draw.text(average_offset, average_text, fill=(241, 239, 128), font=average_font)

    # paste bar chart to foreground
    bar_chart = generate_bar_chart(labels, values)
    bar_chart_offset = ((fg.width - bar_chart.width) // 2, score_png.height + 250)
    fg.paste(bar_chart, bar_chart_offset)

    # paste foreground to background
    fg_offset = ((bg.width - fg.width) // 2, (bg.height - fg.height) // 2)
    bg.paste(fg, fg_offset)

    data = io.BytesIO()
    bg.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())
    return encoded_img_data
