FROM python:latest

# Create working directory for the app
WORKDIR /app

# Copy all files from the working directory and install requirements (must include a kaggle.json file)
COPY . .
RUN mkdir datasets
RUN pip install --no-cache-dir -r requirements.txt

# Make a .kaggle directory and copy the kaggle.json file
RUN mkdir ~/.kaggle
RUN cp kaggle.json ~/.kaggle/kaggle.json

# Download the dataset
RUN ./marketanalysis.sh download_data

# Run the web application to analyze the data
CMD [ "uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--reload"]