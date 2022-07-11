import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys, os, json
from PIL import Image

class HandyPlotter:

    def __init__(self, *args):
        if len(args) == 0:
            return None
        elif len(args) == 1:
            try:
                with open(args[0]) as config_file:
                    self.config = json.load(config_file) 
            except Exception as err:
                sys.stderr.write("\n")
                raise Exception(f"Failed to load HandyPlotter config file\n({type(err)}): {err}")
        else:
            raise Exception(f"Failed to initialize a HandyPlotter object. Expected 0-1 arguments, got {len(args)}")


    def plot_likert_scales(self, question_text, rows, scale, outfile):
        import plot_likert
        # Uses Nathan Malkin's plot-likert library to plot likert scales

        assert len(rows) > 0, "can't plot nothingness"
        assert type(question_text) is list
        assert type(rows) is list
        assert type(rows[0]) is list
        assert type(rows[0][0]) is str

        num_questions = len(question_text)
        num_answers = len(rows)

        # Standardize capitalization to match scale
        for i in range(len(rows)):
            assert len(rows[i]) == num_questions

            for j in range(len(rows[0])):
                if rows[i][j] not in scale:
                    for k in scale:
                        if rows[i][j].lower() == k.lower():
                            rows[i][j] = k
                            break


        row_labels = ("Q" + str(i+1) for i in range(len(question_text)))

        df = pd.DataFrame(
            rows, 
            columns=row_labels
        )

        #print(df)

        # Expects questions as column names, and answers as cells
        self._write_plot_to_file(
            plot_likert.plot_likert(
                df, 
                plot_scale=scale
            ),    
            outfile
        )


    def _write_plot_to_file(self, p, fn):
        plt.savefig(fn, bbox_inches='tight', metadata={})
        
        # Remove references to matplotlib, etc in image file
        if fn[-4:] in [".png", ".jpg"]:
            image = Image.open(fn)
            image_clean = Image.new(image.mode, image.size)
            image_clean.putdata(list(image.getdata()))
            image_clean.save(fn)