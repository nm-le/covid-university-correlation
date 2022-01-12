# covid-university-correlation
**Determining the correlation between the impact of universities' social media announcements and COVID cases through statistical analysis**

*The final project to University of Toronto's CSC110H1 course - with final result of 95.5%.*

*Built by Shaan Purewal, [Minh Le](https://github.com/nm-le), Tony Kim, [Kurtis Law](https://github.com/kurtislaw) after pulling 2 all-nighters :)*

## Abstract
![screenshot of project pdf](https://i.imgur.com/YmzZQ0i.png)

> As of October 29th 2021, nearly 40% of all COVID-19 cases in Canada are linked to university-aged people (19-29 years old) [[1]](https://health-infobase.canada.ca/covid-19/epidemiological-summary-covid-19-cases.html). 

> The public health unit covering Kingston, Ont., said that over 70 per cent of all COVID-19 cases in its jurisdiction were linked to the neighbourhoods around Queen’s University [[2]](https://globalnews.ca/news/7757102/covid-19-canadian-university-students/). 

Universities are major sources of outbreaks. Thankfully, they took to their own way of responding to this pandemic, announcing on social media their policy changes, resource distribution, switch to online lessons, etc. 

Since different universities had different plans in place at different times, we thought they would serve as interesting semi-isolated data points to cross compare COVID-related announcements to different changes in COVID-19 cases. Hence, using data, we explored the correlation between universities' COVID-19 announcements and local cases. In other words, **how the change in intensity of COVID-19 policies relates to the change in COVID cases in the surrounding neighborhoods of that respective university.**


## Datasets
Provincial COVID cases were collected from the Government of Ontario, with each case having its exact location and thus can be attributed to be a 'local case' (within a 5km radius) of a specific university. 

Social media posts are collected using scrapers and assigned an 'impact score' based on its intensity.


## Usage
1. Clone the repo and `cd` into its direcotry
2. Run `pip install -r requirements.txt` to install required libraries
3. Run `python3 main.py` if you are on MacOS and `python main.py` if you are on Windows.

## Results
For our discussion of collected results and conclusions, please view the [project report](https://github.com/kurtislaw/covid-university-correlation/blob/main/project_report.pdf) directly for more!
