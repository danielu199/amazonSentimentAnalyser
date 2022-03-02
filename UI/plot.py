import matplotlib.pyplot as plt
import numpy as np

def main(df, arg, productID):

    df = sorted(df.items(), key=lambda x: x[1], reverse = True)
    colors = []
    words = []
    values = []



    for key,value in df:
        words.append(key)
        values.append(value)
        if value < 0:
            colors.append("red")
        else:
            colors.append("green")


    plt.rcdefaults()
    fig, ax = plt.subplots()
    if arg == 1:
        fig.canvas.set_window_title(str(productID))
    elif arg == 0:
        fig.canvas.set_window_title("Leider keine gültige Product ID eingegeben: " + str(productID))
    y_pos = np.arange(len(values))
    ax.barh(y_pos, values, align='center',
            color=colors, ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(words)
    ax.invert_yaxis()  # labels von oben nach unten
    ax.set_xlabel('Polarität')
    if arg ==1:
        ax.set_title('Review Analyser')
    elif arg == 0:
        ax.set_title('Leider keine gültige Product ID eingegeben: ' + str(productID))
    plt.show()


if __name__ == "__main__":
    df = {'quality': -0.5, 'general': 0.16450996197718656, 'picture': 0.30390870626525646,
     'speakers': 0.17954208588957024, 'features': -0.3, 'setting': -0.14617153846153846,
     'warranty': 0.19403800000000004, 'sound': 0.21175568022440364, 'screen': 0.2043399109792281,
     'for': 0.3427076923076923, 'TV': 0.3006433510638297, 'Roku': -0.21105720164609043, 'TCL': 0.18489234234234225,
     'set': 0.22382235294117642, 'one': 0.12211382113821141}
    main(df)




















