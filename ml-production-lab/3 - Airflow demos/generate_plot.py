import matplotlib.pyplot as plt
import pandas as pd
import os


def load_results() -> (pd.Series, pd.Series):
    """
    Load the prediction and the last datapoints which this is based on
    """

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_outputs')

    last_X = pd.read_csv(os.path.join(output_dir, 'last_X.csv'), index_col=0)
    preds = pd.read_csv(os.path.join(output_dir, 'preds.csv'), index_col=0)

    return last_X, preds


def generate_plot(last_X: pd.Series, preds: pd.Series):

    # Draw the plot
    plt.plot(last_X, label='actual')
    plt.plot(preds, label='preds')

    # Change the x-axis tick labels
    xticklabels = [''] * (len(last_X) + len(preds))
    xticklabels[0] = last_X.index[0]
    xticklabels[len(last_X)] = last_X.index[-1]
    plt.xticks(xticklabels)

    # Add a legend and a title
    plt.legend()
    plt.title(f'Hourly temperature for {last_X.index[-1]} with 6 hour forecast')

    # Save it to the output directory
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    filename = f'{preds.index[0].split(":")[0]}.png'

    plt.savefig(os.path.join(output_dir, filename))


if __name__ == '__main__':

    last_X, preds = load_results()

    generate_plot(last_X, preds)
