import os

app_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(app_dir, 'src')
static_dir = os.path.join(app_dir, 'static')
data_dir = os.path.join(app_dir, 'data')
temp_dir = os.path.join(data_dir, 'temp')
output_dir = os.path.join(data_dir, 'output')

# Create dirs if they do not exist
for dir in [data_dir, temp_dir, output_dir]:
    if not os.path.exists(dir):
        os.makedirs(dir)

