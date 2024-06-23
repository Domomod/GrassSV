import matplotlib.pyplot as plt
import pickle
import glob

def plot_data():

    file_list = []
    for name in glob.glob('*.pickle'):
        file_list.append(name)
    print(f"Loading pickles: {file_list}")

    # Create a figure and axis for precision-recall plot
    fig, ax1 = plt.subplots(figsize=(7, 7))

    # Plot precision-recall data
    color_list = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    for file, color in zip(file_list, color_list):
        sv_detector_name = file.split('.')[0]
        print(f"Processing: {sv_detector_name}")

        with open(file, 'rb') as handle:
            [axis_recall, axis_precision] = pickle.load(handle)

        margins = range(1, 300, 10)  # Assuming margins are in this range

        ax1.plot(axis_recall, axis_precision, color, label=sv_detector_name)
        ax1.set_xlabel('Recall', fontsize=12)
        ax1.set_ylabel('Precision', fontsize=12)
        ax1.tick_params('y')

    # Add legends
    lines, labels = ax1.get_legend_handles_labels()
    ax1.legend(lines, labels, loc='upper left')

    # Set title for the main plot
    ax1.set_title('Precision & Recall in function of margin', fontsize=20)

    # Set axis limits and ticks
    ax1.set_xlim([0, 100])
    ax1.set_ylim([0, 100])
    ax1.set_xticks(range(0, 101, 10))
    ax1.set_yticks(range(0, 101, 10))
    ax1.grid(which='both', linestyle='--', linewidth=0.5)

    # Create inset axes for Recall vs Margin
    ax_inset_recall = fig.add_axes([0.65, 0.36, 0.3, 0.12])  # Adjust the size and position
    for file, color in zip(file_list, color_list):
        sv_detector_name = file.split('.')[0]
        with open(file, 'rb') as handle:
            [axis_recall, axis_precision] = pickle.load(handle)
        margins = range(1, 300, 10)  # Assuming margins are in this range
        ax_inset_recall.plot(margins, axis_recall, color, label=sv_detector_name)
    ax_inset_recall.set_ylim([0, 100])
    ax_inset_recall.set_xlim([0, 300])
    ax_inset_recall.set_title('Recall vs Margin', fontsize=12)
    ax_inset_recall.set_xlabel('Margin', fontsize=10)
    ax_inset_recall.set_ylabel('Recall', fontsize=10)
    ax_inset_recall.tick_params(axis='both', which='major', labelsize=8)

    # Create another inset axes for Precision vs Margin
    ax_inset_precision = fig.add_axes([0.65, 0.15, 0.3, 0.12])  # Adjust the size and position
    for file, color in zip(file_list, color_list):
        sv_detector_name = file.split('.')[0]
        with open(file, 'rb') as handle:
            [axis_recall, axis_precision] = pickle.load(handle)
        margins = range(1, 300, 10)  # Assuming margins are in this range
        ax_inset_precision.plot(margins, axis_precision, color, label=sv_detector_name)
    ax_inset_precision.set_ylim([0, 100])
    ax_inset_precision.set_xlim([0, 300])
    ax_inset_precision.set_title('Precision vs Margin', fontsize=12)
    ax_inset_precision.set_xlabel('Margin', fontsize=10)
    ax_inset_precision.set_ylabel('Precision', fontsize=10)
    ax_inset_precision.tick_params(axis='both', which='major', labelsize=8)

    # Adjust layout and save the plot to files
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Add padding on the top
    formats = ['png', 'svg', 'pdf']
    for format in formats:
        plot_file = f"precision_recall_margin_plot.{format}"
        print(f"Saving plot to {plot_file}")
        plt.savefig(plot_file, format=format)

# Call the function to plot the data
plot_data()
