import matplotlib.pyplot as plt
import pickle
import glob

def plot_data():

    file_list = []
    for name in glob.glob('*.pickle'):
        file_list.append(name)
    print(f"Loading pickles: {file_list}")




    # Create a figure and axis
    fig, ax1 = plt.subplots()

    # Plot precision data
    ax = ax1

    color_list = ['r', 'g', 'b', 'c', 'm', 'y', 'b']
    for file, color in zip(file_list, color_list):
        sv_detector_name = file.split('.')[0]
        print(f"Processing: {sv_detector_name}")

        with open(file, 'rb') as handle:
            [axis_recall, axis_precision] = pickle.load(handle)

        ax.plot(axis_recall, axis_precision, color, label=sv_detector_name)
        ax.set_xlabel('Recall')
        ax.set_ylabel('Precision')
        ax.tick_params('y')
    lines, labels = ax.get_legend_handles_labels()
    ax1.legend(lines, labels, loc='upper right')

    # Set the title
    plt.title('Precision and Recall')

    # Save the plot to a PDF file
    formats = ['png', 'svg', 'pdf']
    for format in formats:
        plot_file = f"precision_recall_plot.{format}"
        print(f"Saving plot to {plot_file}")
        plt.savefig(plot_file, format=format)
