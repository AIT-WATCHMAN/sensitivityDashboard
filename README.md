# Sensitivity App
Shows a view of an arbitrary detector sensitivity under two
different statistical assumptions. Here we will use:
```
Z = Sensitivity in units of σ
s = Signal rate
b = Background rate
t = time (units matching s and b)
σ = Background rate fractional uncertainty
```
#### Discovery
This is the sensitivity to reject a non-zero hypothesis:

<a href="https://www.codecogs.com/eqnedit.php?latex=\bg_white&space;Z&space;=&space;\frac{st}{\sqrt{bt&plus;(\sigma&space;bt)^2}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\bg_white&space;Z&space;=&space;\frac{st}{\sqrt{bt&plus;(\sigma&space;bt)^2}}" title="Z = \frac{st}{\sqrt{bt+(\sigma bt)^2}}" /></a>

#### Measurement
This is the sensitivity to measure the value of `s` for a given signal rate:

<a href="https://www.codecogs.com/eqnedit.php?latex=\bg_white&space;Z&space;=&space;\frac{st}{\sqrt{bt&plus;st&plus;(\sigma&space;bt)^2}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\bg_white&space;Z&space;=&space;\frac{st}{\sqrt{bt&plus;st&plus;(\sigma&space;bt)^2}}" title="Z = \frac{st}{\sqrt{bt+st+(\sigma bt)^2}}" /></a>
## How to run
It is recommended to run in a new virtual environment:
```bash
python3 -m venv sdash
source sdash/bin/activate
```
Install the requirements
```bash
pip install -r requirements.txt
```
Run the app
```bash
python app.py
```
Open a browser at http://127.0.0.1:8050
