wget https://dbproject.s3.amazonaws.com/kindle_reviews_update.zip
wget https://dbproject.s3.amazonaws.com/meta_kindle_store_update.zip

unzip kindle_reviews_update.zip
unzip meta_kindle_store_update.zip


sudo yum update
sudo yum install python-pip -y
sudo pip install numpy
python -m pip --no-cache-dir install pyspark --user 
sudo pip install findspark

hdfs dfs -mkdir -p /dbproject

hdfs dfs -put kindle_reviews_update.csv /dbproject
hdfs dfs -put meta_kindle_store_update.json /dbproject

python tf-idf.py
python pearson_correlation.py