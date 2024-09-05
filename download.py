def downloadstorm(name, year, return_file_names=False):
    from urllib.request import urlopen
    import requests
    import pandas as pd
    from io import StringIO
    import os
    import re

    name = name.lower()
    directory = f'https://www.aoml.noaa.gov/ftp/pub/hrd/data/flightlevel/{year}/{name}/'
    page = requests.get(directory).text
    content = page.split("\n")
    files = []
    for line in content:
        if ".1sec.txt" in line or ".1sec" in line:
            files.append((line.split('"> ')[1]).split("</a>")[0])

    if len(files) < 1:
        import sys
        sys.exit("No valid files found in directory. Exiting.")

    textlist = []
    for ii, file in enumerate(files):
        file_path = f'./Data/{file}'
        if not os.path.isfile(file_path):
            try:
                with urlopen(directory+file) as url:
                    print(f"Downloading file {ii + 1}")
                    urldec = url.read().decode('utf-8')
                    textlist.append(urldec)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(urldec)
            except:
                continue
        else:
            print(f"Reading existing file {ii + 1}")
            with open(file_path, "r") as f:
                textlist.append(f.read())

    dflist = []
    for ii, text in enumerate(textlist):
        print(f"Parsing file {ii + 1}")
        try:
            cleaned_lines = []
            
            for line in text.splitlines():
                fields = line.split()
                if len(fields) > 1 and fields[1] == '0.000' and fields[2] == '0.000':
                    continue

                cleaned_fields = [field for field in fields if not (re.fullmatch(r'\b\d\b', field))]
                cleaned_line = ' '.join(cleaned_fields)
                cleaned_lines.append(cleaned_line)

            cleaned_text = '\n'.join(cleaned_lines)
            df = pd.read_csv(StringIO(cleaned_text), sep="\s+", skiprows=[0, 1, 3], header=0, skipfooter=1, on_bad_lines='warn', engine='python')
            dflist.append(df)

        except Exception as e:
            print(f"Error parsing file {ii + 1}: {e}")
            continue

    if return_file_names:
        return dflist, files
    return dflist

if __name__ == "__main__":
    name = "Allen"
    year = 1980
    downloadstorm(name, year)
