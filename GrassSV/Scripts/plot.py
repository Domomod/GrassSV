import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pickle
import glob
import numpy as np
from collections import Counter
from pprint import pprint

def load_pickled_data(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)
import numpy as np
import matplotlib.pyplot as plt

series1   = ['(Were)\nDeletions', '(Were)\nInversions', '(Were)\nDuplications', '(Were)\nInsertions', '(Were)\nTranslocations', 'False Positive']
series2   = ['Deletions', 'Inversions', 'Duplications', 'Insertions', 'Translocations', 'BND',
            '(Misclassified as)\nDeletions', '(Misclassified as)\nInversions', '(Misclassified as)\nDuplications', '(Misclassified as)\nInsertions', '(Misclassified as)\nTranslocations',
            'False Negative']
series = series1 + series2

style_scheme = {     
    'Deletions':                            {'color': '#de4035', 'hatch': None , 'edgecolor': '#f5b0ab',     'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    'Inversions':                           {'color': '#fce54e', 'hatch': None , 'edgecolor': '#fff5cc',     'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    'Duplications':                         {'color': '#2c83db', 'hatch': None , 'edgecolor': '#a8c6f3',     'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    'Insertions':                           {'color': '#58db2c', 'hatch': None , 'edgecolor': '#b3ec9f',     'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    'Translocations':                       {'color': '#be2cdb', 'hatch': None , 'edgecolor': '#e6b3f2',     'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    'BND':                                  {'color': '#a36424', 'hatch': None , 'edgecolor': '#d6b999',     'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    'False Negative':                       {'color': '#333333', 'hatch': None , 'edgecolor': '#999999',     'textcolor' : 'white', 'textformat' : '', 'textposition' : -4,    'textalways' : True},
    '(Misclassified as)\nDeletions':        {'color': '#de4035', 'hatch': '\\\\\\', 'edgecolor': '#f5b0ab',  'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    '(Misclassified as)\nInversions':       {'color': '#fce54e', 'hatch': '\\\\\\', 'edgecolor': '#fff5cc',  'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    '(Misclassified as)\nDuplications':     {'color': '#2c83db', 'hatch': '\\\\\\', 'edgecolor': '#a8c6f3',  'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    '(Misclassified as)\nInsertions':       {'color': '#58db2c', 'hatch': '\\\\\\', 'edgecolor': '#b3ec9f',  'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    '(Misclassified as)\nTranslocations':   {'color': '#be2cdb', 'hatch': '\\\\\\', 'edgecolor': '#e6b3f2',  'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    '(Were)\nDeletions':                    {'color': '#de4035', 'hatch': '///', 'edgecolor': '#f5b0ab',     'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    '(Were)\nInversions':                   {'color': '#fce54e', 'hatch': '///', 'edgecolor': '#fff5cc',     'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    '(Were)\nDuplications':                 {'color': '#2c83db', 'hatch': '///', 'edgecolor': '#a8c6f3',     'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    '(Were)\nInsertions':                   {'color': '#58db2c', 'hatch': '///', 'edgecolor': '#b3ec9f',     'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    '(Were)\nTranslocations':               {'color': '#be2cdb', 'hatch': '///', 'edgecolor': '#e6b3f2',     'textcolor' : 'black', 'textformat' : '', 'textposition' : -4,    'textalways' : False},
    'False Positive':                       {'color': '#db8686', 'hatch': '///' , 'edgecolor': '#999999',     'textcolor' : 'black', 'textformat' : 'FP=', 'textposition' : +5, 'textalways' : True}
}

legend1 = {
    'Deletions':                            {'color': '#de4035', 'hatch': None , 'edgecolor': '#f5b0ab'},
    'Inversions':                           {'color': '#fce54e', 'hatch': None , 'edgecolor': '#fff5cc'},
    'Duplications':                         {'color': '#2c83db', 'hatch': None , 'edgecolor': '#a8c6f3'},
    'Insertions':                           {'color': '#58db2c', 'hatch': None , 'edgecolor': '#b3ec9f'},
    'Translocations':                       {'color': '#be2cdb', 'hatch': None , 'edgecolor': '#e6b3f2'},
    'BND':                                  {'color': '#a36424', 'hatch': None , 'edgecolor': '#d6b999'},
}

legend2 = {
    'False Positive':                       {'color': '#db8686', 'hatch': '///' , 'edgecolor': '#999999'},
    '(Wrong classification)':                   {'color': '#999999', 'hatch': "///" , 'edgecolor': '#333333'},
    'False Negative':                       {'color': '#333333', 'hatch': None , 'edgecolor': '#999999'},
    '(Detected, but missclassified)':               {'color': '#999999', 'hatch': '\\\\\\' , 'edgecolor': '#333333'},
}

legend3 = {
}

def extract_data2(entries):
    sv_types = ['DEL', 'INV', 'DUP', 'INS', 'TRN', 'BND']
    type_map = {'DEL': 'Deletions', 'INV': 'Inversions', 'DUP': 'Duplications', 'INS': 'Insertions', 'TRN': 'Translocations', 'BND':'BND'}

    data = {'Deletions': {}, 'Inversions': {}, 'Duplications': {}, 'Insertions': {}, 'Translocations': {}}
    for dictionary in data.values():
        for category in series:
            dictionary[category] = 0

    for entry in entries:
        sv_type = entry.type.strip()
        sv_label = type_map[sv_type]

        entry_values = {'DEL' : entry.deletions, 'INV' : entry.inversions, 'DUP' : entry.duplications, 'INS' : entry.insertions, 'TRN' : entry.translocations}
        pprint(entry)

        sanitize_func = lambda x : int(x) if x != ' X ' else 0

        for entry_type, value in entry_values.items():
            label = type_map[entry_type]
            if sv_label == 'BND':
                data[label]['BND'] = sanitize_func(value)
            elif label == sv_label: #
                data[sv_label][label] = sanitize_func(value)
            else:
                sanitized_value = sanitize_func(value)
                if sanitized_value != 0:
                    data[label]['(Misclassified as)\n'+sv_label] = (value)
                    data[sv_label]['(Were)\n'+label] = (value)

        if sv_label != 'BND':
            data[sv_label]['False Positive'] += sanitize_func(entry.false_positive)

    for dictionary in data.values():
        pprint(dictionary)
        dictionary['False Negative'] = 100 - sum([dictionary[key] for key in series2])

    # pprint(data)
    return data
    
    
width = 0.08
spacing = 0.12
def draw_subplot(ax, series, caller_data_dict, x):
    for i, caller in enumerate(caller_data_dict):
        positions = x + i * (width + spacing) - (width + spacing) * (len(caller_data_dict) - 1) / 2
        cumulative = np.zeros(len(x))
        pprint(cumulative)
        pprint(caller_data_dict[caller].keys())
        for category in series:
            if category in style_scheme:
                style = style_scheme[category]
            else:
                style = {'color': '#999999', 'hatch': None, 'edgecolor': '#cccccc'}
            bar_values_array = []
            # pprint(sv_type)
            for dictionary in caller_data_dict[caller].values():
                # pprint(dictionary)
                bar_values_array.append(dictionary[category])
            pprint(bar_values_array)
            bars = ax.bar(
                positions, bar_values_array, width, label=f"{caller} - {category}", bottom=cumulative,
                color=style['color'], hatch=style['hatch'], edgecolor=style['edgecolor']
            )
            cumulative += bar_values_array

            for bar in bars:
                yval = bar.get_height()
                if yval > 5 or style['textalways']:
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + yval + style['textposition'], f"{style['textformat']}{int(yval)}", va='center', ha='center', fontsize=8, rotation=0, color=style['textcolor'])


def create_legend(legend_dict, ax, **args):
    legend_patches = []
    for label, style in legend_dict.items():
        patch = mpatches.Patch(facecolor=style['color'], hatch=style['hatch'], edgecolor=style['edgecolor'], label=label)
        legend_patches.append(patch)

    plot_legend = ax.legend(handles=legend_patches, **args)
    return plot_legend


def create_grouped_stacked_bar_diagram(data_dict, title):
    labels, misclassified_labels = [], []

    caller_data_dict = {}
    for caller, data in data_dict.items():
        caller_data_dict[caller] = extract_data2(data)
        labels = caller_data_dict[caller].keys()
    caller_labels = data_dict.keys()


    pprint(caller_data_dict)

    x = np.arange(len(labels))
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [25, 10]}, sharex=True)
    draw_subplot(ax1, series1, caller_data_dict, x)
    draw_subplot(ax2, series2, caller_data_dict, x)

    # Add SV caller names below the corresponding bars
    for i, caller in enumerate(data_dict.keys()):
        for j in range(len(labels)):
            positions = x[j] + i * (width + spacing) - (width + spacing) * (len(data_dict) - 1) / 2
            ax2.text(positions, -27, caller, rotation=90, ha='center')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax2.set_xlabel('Generated SV (100 of each type)')
    ax1.set_ylabel('Number of mistakes')
    ax2.set_ylabel('Number of detected SVs')
    ax1.set_title(title, y=1.1)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=0, ha='center')
    ax2.tick_params(axis='x', pad=60)  # Move the x-tick labels down

    # # Add SV caller names below the corresponding bars
    # for i, caller in enumerate(caller_labels):
    #     for j in range(len(labels)):
    #         positions = x[j] + i * (width + spacing) - (width + spacing) * (len(data_dict) - 1) / 2
    #         ax2.text(positions, -35, caller, rotation=90, ha='center')

    # Create legend entries
    plot_legend1 = create_legend(legend1, ax1, **{'ncol' : 6, 'bbox_to_anchor' :(0.5, 1.08), 'loc' : 'upper center'})
    # plot_legend2 = create_legend(legend2 + legend3, ax2, **{'ncol' : 3, 'loc' : 'upper right'})
    plot_legend3 = create_legend(legend2, ax2, **{'ncol' : 4, 'bbox_to_anchor' :(0.5, 1.2), 'loc' : 'upper center'})
    # ax1.add_artist(plot_legend1)


    # Add horizontal lines every 100 units
    ax1.set_yticks(np.arange(0, 252, 50))
    ax1.grid(axis='y', linestyle='--', linewidth=0.7)
    ax2.set_yticks(np.arange(0, 101, 25))
    ax2.grid(axis='y', linestyle='--', linewidth=0.7)

    # Add vertical dotted lines between SV types
    for pos in range(len(labels) -1):
        ax1.axvline(0.5125 + pos * len(caller_labels) * (width + spacing+ 0.05125), color='gray', linestyle='solid', linewidth=1)
        ax2.axvline(0.5125 + pos * len(caller_labels) * (width + spacing+ 0.05125), color='gray', linestyle='solid', linewidth=1)

    fig.tight_layout()
    plt.show()

    formats = ['png', 'svg', 'pdf']
    for format in formats:
        plot_file = f"bar_diagram_plot.{format}"
        print(f"Saving plot to {plot_file}")
        plt.savefig(plot_file, format=format)


def plot_bar_diagram():
    # Path to the pickle file for margin 70
    pickle_files = {
        'grass_sv': 'sv_analysis_margin_70.grass_sv.pkl',
        'gridss': 'sv_analysis_margin_70.gridss.pkl',
        'lumpy': 'sv_analysis_margin_70.lumpy.pkl',
        'pindel': 'sv_analysis_margin_70.pindel.pkl'
    }    
    # Load the pickled collected_data for each caller
    collected_data = {caller: load_pickled_data(file) for caller, file in pickle_files.items()}
    
    # Create a grouped stacked bar diagram
    create_grouped_stacked_bar_diagram(collected_data, 'Comparison of annotated regions reports for [Margin 70] by SV Caller')

def plot_precision_recall():

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

def plot_data():
    plot_bar_diagram()
    plot_precision_recall()