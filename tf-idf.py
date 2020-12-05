












#################### Note!!!!!  ################################################
# This file currently is for testing file transmission of the automation script
# The content needs to be changed to the actual analytic code once its done


import findspark
findspark.init() 
from pyspark.sql import SparkSession

# https://spark.apache.org/docs/latest/sql-getting-started.html
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

df = spark.read.json("/dbproject/meta_kindle_store_update.json")
# Displays the content of the DataFrame to stdout
df.show()

asin_price = df.select('asin', 'price')
asin_price.show()

#df.write.format("parquet").save("meta_kindle_store_update.parquet", format="parquet")
print(type(df))


df_reviews = spark.read.load("/dbproject/kindle_reviews_update.csv", format="csv", sep=",", header="true")

#df_reviews = spark.read.option("header",True).csv(r'reviews_spillover_removed.csv')
df_reviews = df_reviews.filter(df_reviews.review_text.isNotNull())
df_reviews.show()

f = open("sample_output.csv", "a")
f.write("Now the file has more content!")
f.close()