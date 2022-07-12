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


    def plot_likert_scales(self, rows, scale, outfile, row_labels=None, title=None):
        import plot_likert
        # Uses Nathan Malkin's plot-likert library to plot likert scales

        assert len(rows) > 0, "can't plot nothingness"
        assert type(rows) is list
        assert type(rows[0]) is list
        assert type(rows[0][0]) is str

        num_questions = len(rows[0])
        num_answers = len(rows)

        # Standardize capitalization to match scale
        for i in range(num_answers):

            # Also make sure that every data row is the same length
            assert len(rows[i]) == num_questions

            for j in range(num_questions):

                # Fix capitalization differences from the displayed scale
                if rows[i][j] not in scale:
                    for k in range(len(scale)):
                        if type(rows[i][j]) is not str:
                            rows[i][j] = str(rows[i][j])
                        if type(scale[k]) is not str:
                            scale[k] = str(scale[k])
                        if rows[i][j].lower() == scale[k].lower():
                            rows[i][j] = scale[k]
                            break

        if row_labels == None:
            row_labels = ("Q" + str(i+1) for i in range(num_questions))

        df = pd.DataFrame(
            rows, 
            columns=row_labels
        )

        plot_likert.plot_likert(
                df, 
                plot_scale=scale
            )

        if title is not None:
            plt.title(title)

        # Expects questions as column names, and answers as cells
        self._write_plot_to_file(
            outfile
        )
    
    
    # cat_name -> {opt1 -> cnt1, opt2 -> ...}
    def plot_categorical_breakdown_latex_table(self, data, title, category_override = None):
        
        categories = list(data.keys())

        headers = "\\textbf{" + "} & \\testbf{".join(["category        ", "count", "percent"]) + "} \\\\"

        tabular_rows = []
        total = sum(list(data[categories[0]].values()))

        i = 0
        for category, options in data.items():
            
            tabular_row = " "*12 + f"\\textbf{{{category:20}}}" + " "*34
            if category_override is not None:
                tabular_row = " "*12 + f"\\textbf{{{category_override[i] + '}':40}"  + " "*14

            tabular_rows.append(tabular_row)
            i += 1

            # Sort the options  
            # The hope is 50% of the time this is the sort you want :)
            option_names = sorted(list(set(options.keys())), key = lambda a: int(a) if a.isdigit() else -1*options[a])

            
            for option in option_names:
                cnt = options[option]
                tabular_rows.append(" "*12 + f"{option:25} & {cnt:14} & {round(cnt/total * 100,2):14}\\% ")
                

        body = "\\\\\n".join(tabular_rows)

        return \
f"""
\\begin{{table}}
    \\begin{{center}}
        \\begin{{tabular}}{{|l|c|c|}}
            {headers}
            \\midrule
{body}\\\\
        \\end{{tabular}}
        \\caption{{\\textbf{{{title}}}--\\\\
        }}
        \\label{{table:{title.replace(" ", "-").lower()}}}
    \\end{{center}}
\\end{{table}}
"""



    def _write_plot_to_file(self, fn):
        plt.savefig(fn, bbox_inches='tight', metadata={})
        
        # Remove references to matplotlib, etc in image file
        if fn[-4:] in [".png", ".jpg"]:
            image = Image.open(fn)
            image_clean = Image.new(image.mode, image.size)
            image_clean.putdata(list(image.getdata()))
            image_clean.save(fn)